"""Role -- identity layer (WHO the agent is)."""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Any

from openvibe_sdk.llm import LLMProvider, LLMResponse
from openvibe_sdk.memory.access import ClearanceProfile
from openvibe_sdk.memory.agent_memory import AgentMemory
from openvibe_sdk.memory.assembler import MemoryAssembler
from openvibe_sdk.memory.filesystem import MemoryFilesystem
from openvibe_sdk.memory.types import Episode, Insight
from openvibe_sdk.models import (
    AuthorityConfig, Event, Objective, RoleLifecycle, TrustProfile,
)
from openvibe_sdk.operator import Operator


class _RoleAwareLLM:
    """LLM wrapper that injects Role identity and memory into every call."""

    def __init__(self, role: Role, inner: LLMProvider) -> None:
        self._role = role
        self._inner = inner

    def call(
        self, *, system: str, messages: list[dict], **kwargs: Any
    ) -> LLMResponse:
        context = ""
        if messages:
            first_content = messages[0].get("content", "")
            context = (
                first_content
                if isinstance(first_content, str)
                else str(first_content)
            )
        augmented_system = self._role.build_system_prompt(system, context)
        return self._inner.call(
            system=augmented_system, messages=messages, **kwargs
        )


class Role:
    """Identity layer -- WHO the agent is.

    Subclass and set role_id, soul, and operators.
    V2 adds: authority, clearance, agent_memory.
    """

    role_id: str = ""
    soul: str = ""
    operators: list[type[Operator]] = []
    authority: AuthorityConfig | None = None
    clearance: ClearanceProfile | None = None

    # V3 identity fields
    workspace: str = ""
    domains: list[str] = []
    reports_to: str = ""

    def __init_subclass__(cls, **kwargs: Any) -> None:
        super().__init_subclass__(**kwargs)
        if "operators" not in cls.__dict__:
            cls.operators = []

    def __init__(
        self,
        llm: LLMProvider | None = None,
        agent_memory: AgentMemory | None = None,
        config: dict | None = None,
        lifecycle: RoleLifecycle | None = None,
        trust: TrustProfile | None = None,
        goals: list[Objective] | None = None,
    ) -> None:
        self.llm = llm
        self.agent_memory = agent_memory
        self.config = config or {}
        self._operator_instances: dict[str, Operator] = {}
        self._memory_fs: MemoryFilesystem | None = None
        self.lifecycle = lifecycle
        self.trust = trust
        self.goals = goals or []

    def can_act(self, action: str) -> str:
        """Check authority for an action.

        Returns: 'autonomous' | 'needs_approval' | 'forbidden'.
        If no authority config, everything is autonomous.
        """
        if not self.authority:
            return "autonomous"
        return self.authority.can_act(action)

    def respond(self, message: str, context: str = "") -> LLMResponse:
        """Respond to a message with soul + memory context (V2 only)."""
        if not self.llm:
            raise ValueError(f"Role '{self.role_id}' has no LLM configured")

        parts: list[str] = []
        soul_text = self._load_soul()
        if soul_text:
            parts.append(soul_text)

        if self.agent_memory:
            insights = self.agent_memory.recall_insights(query=message, limit=5)
            if insights:
                lines = [f"- {i.content}" for i in insights]
                parts.append("## Knowledge\n" + "\n".join(lines))

        system = "\n\n".join(parts)
        response = self.llm.call(
            system=system,
            messages=[{"role": "user", "content": message}],
        )

        if self.agent_memory:
            self.agent_memory.record_episode(Episode(
                id=str(uuid.uuid4()),
                agent_id=self.role_id,
                operator_id="",
                node_name="respond",
                timestamp=datetime.now(timezone.utc),
                action="respond",
                input_summary=message[:200],
                output_summary=(response.content or "")[:200],
                outcome={},
                duration_ms=0,
                tokens_in=getattr(response, "tokens_in", 0),
                tokens_out=getattr(response, "tokens_out", 0),
            ))

        return response

    @property
    def memory_fs(self) -> MemoryFilesystem | None:
        """Virtual filesystem over this Role's memory. None if no agent_memory."""
        if not self.agent_memory:
            return None
        if self._memory_fs is None:
            self._memory_fs = MemoryFilesystem(
                role_id=self.role_id,
                agent_memory=self.agent_memory,
                soul=self._load_soul(),
            )
        return self._memory_fs

    def reflect(self) -> list[Insight]:
        """Compress recent episodes into insights via LLM."""
        if not self.agent_memory or not self.llm:
            return []
        return self.agent_memory.reflect(self.llm)

    def list_operators(self) -> list[str]:
        """List operator IDs this Role can use."""
        return [op.operator_id for op in self.operators]

    def get_operator(self, operator_id: str) -> Operator:
        """Get or create an Operator instance with Role-aware LLM."""
        if operator_id not in self._operator_instances:
            for op_class in self.operators:
                if op_class.operator_id == operator_id:
                    wrapped_llm = (
                        _RoleAwareLLM(self, self.llm) if self.llm else None
                    )

                    # V2: build memory assembler when agent_memory exists
                    assembler = None
                    if self.agent_memory:
                        clearance = self.clearance or ClearanceProfile(
                            agent_id=self.role_id,
                            domain_clearance={},
                        )
                        assembler = MemoryAssembler(
                            self.agent_memory, clearance
                        )

                    op = op_class(
                        llm=wrapped_llm, memory_assembler=assembler
                    )

                    # V2: wire up episode recorder
                    if self.agent_memory:
                        op._episode_recorder = self.agent_memory.record_episode

                    self._operator_instances[operator_id] = op
                    break
            else:
                raise ValueError(
                    f"Role '{self.role_id}' has no operator '{operator_id}'"
                )
        return self._operator_instances[operator_id]

    def build_system_prompt(self, base_prompt: str, context: str = "") -> str:
        """Augment system prompt with soul."""
        soul_text = self._load_soul()
        parts = [p for p in [soul_text, base_prompt] if p]
        return "\n\n".join(parts)

    # V3 communication
    _registry: "Any" = None
    _transport: "Any" = None
    _last_spawned_spec: "Any" = None  # for testing introspection

    def spawn(self, template: "Any", params: dict[str, str]) -> str:
        """Create child Role from template. Returns new role_id."""
        from openvibe_sdk.models import RoleSpec, TrustProfile
        from openvibe_sdk.registry import Participant

        if self.role_id not in template.allowed_spawners:
            raise PermissionError(
                f"Role '{self.role_id}' is not in allowed_spawners for "
                f"template '{template.template_id}'"
            )

        new_role_id = template.name_pattern.format(**params).lower().replace(" ", "-")
        soul = template.soul_template.format(**params)

        spec = RoleSpec(
            role_id=new_role_id,
            workspace=self.workspace,
            soul=soul,
            domains=template.domains,
            authority=template.authority,
            operator_ids=template.operator_ids,
            reports_to=self.role_id,
            parent_role_id=self.role_id,
            trust=TrustProfile(default=template.default_trust),
            ttl=template.ttl,
        )
        self._last_spawned_spec = spec

        if self._registry is not None:
            self._registry.register_participant(
                Participant(id=new_role_id, type="role", domains=template.domains),
                workspace=self.workspace,
            )

        return new_role_id

    def request_role(self, target_id: str, content: str, payload: dict | None = None) -> "Any":
        """Send request to another role. Returns None if no transport."""
        if not self._transport:
            return None
        from openvibe_sdk.models import RoleMessage
        import uuid
        from datetime import datetime, timezone
        msg = RoleMessage(
            id=str(uuid.uuid4()), type="request",
            from_id=self.role_id, to_id=target_id,
            content=content, payload=payload or {},
            timestamp=datetime.now(timezone.utc),
        )
        self._transport.send(self.role_id, target_id, msg)
        return msg

    def notify_role(self, target_id: str, content: str) -> None:
        """Fire-and-forget notification."""
        if not self._transport:
            return
        from openvibe_sdk.models import RoleMessage
        import uuid
        from datetime import datetime, timezone
        msg = RoleMessage(
            id=str(uuid.uuid4()), type="notification",
            from_id=self.role_id, to_id=target_id,
            content=content,
            timestamp=datetime.now(timezone.utc),
        )
        self._transport.send(self.role_id, target_id, msg)

    def handle(self, event: "Event") -> "RoutingDecision":
        """Receive event, decide action. Deterministic — no LLM call."""
        from openvibe_sdk.models import RoutingDecision, RoleStatus

        # 1. Lifecycle gate
        if self.lifecycle is not None:
            active_statuses = (RoleStatus.ACTIVE, RoleStatus.TESTING)
            if self.lifecycle.status not in active_statuses:
                return RoutingDecision(
                    action="ignore",
                    reason=f"Role is {self.lifecycle.status}",
                )

        # 2. Domain check
        if self.domains and event.domain not in self.domains:
            return RoutingDecision(
                action="forward",
                reason=f"Domain '{event.domain}' not in {self.domains}",
            )

        # 3. Authority check
        authority_result = self.can_act(event.type)
        if authority_result == "forbidden":
            return RoutingDecision(
                action="escalate",
                reason=f"Action '{event.type}' is forbidden",
                target_role_id=self.reports_to,
                message=f"Forbidden action attempted: {event.type}",
            )

        # 4. Match operator
        operator_id, trigger_id = self._match_operator(event)
        if operator_id:
            if authority_result == "needs_approval":
                return RoutingDecision(
                    action="escalate",
                    reason=f"Action '{event.type}' needs approval",
                    target_role_id=self.reports_to,
                    operator_id=operator_id,
                    trigger_id=trigger_id,
                    input_data=event.payload,
                )
            return RoutingDecision(
                action="delegate",
                reason=f"Matched operator '{operator_id}'",
                operator_id=operator_id,
                trigger_id=trigger_id,
                input_data=event.payload,
            )

        # 5. No operator match — escalate
        return RoutingDecision(
            action="escalate",
            reason=f"No operator matched event type '{event.type}'",
            target_role_id=self.reports_to,
        )

    def _match_operator(self, event: "Event") -> tuple[str | None, str | None]:
        """Override in subclasses to map event.type -> (operator_id, trigger_id)."""
        return None, None

    def active_goals(self) -> list["Objective"]:
        """Return goals with status='active'."""
        return [g for g in self.goals if g.status == "active"]

    def goal_context(self) -> str:
        """Format active goals as string for LLM prompt injection."""
        active = self.active_goals()
        if not active:
            return ""
        lines = ["## Current Goals"]
        for obj in active:
            lines.append(f"- {obj.description} [{obj.status}]")
            for kr in obj.key_results:
                pct = int(kr.progress * 100)
                lines.append(f"  • {kr.description}: {kr.current}/{kr.target} {kr.unit} ({pct}%)")
        return "\n".join(lines)

    def _load_soul(self) -> str:
        if not self.soul:
            return ""
        if self.soul.endswith((".md", ".yaml", ".txt")):
            from openvibe_sdk.config import load_prompt

            try:
                return load_prompt(self.soul)
            except FileNotFoundError:
                raise FileNotFoundError(
                    f"Soul file not found: {self.soul} "
                    f"(role '{self.role_id}')"
                )
        return self.soul
