"""Config models for operators, workflows, nodes, and triggers."""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class TriggerType(str, Enum):
    CRON = "cron"
    WEBHOOK = "webhook"
    ON_DEMAND = "on_demand"
    EVENT = "event"


class NodeType(str, Enum):
    LOGIC = "logic"
    LLM = "llm"


class TriggerConfig(BaseModel):
    id: str
    type: TriggerType
    schedule: str | None = None
    source: str | None = None
    workflow: str
    description: str = ""


class NodeConfig(BaseModel):
    id: str
    type: NodeType = NodeType.LOGIC
    model: str | None = None
    prompt_file: str | None = None


class WorkflowConfig(BaseModel):
    id: str
    description: str = ""
    nodes: list[NodeConfig]
    checkpointed: bool = True
    durable: bool = False
    max_duration_days: int | None = None
    timeout_minutes: int = 5


class OperatorConfig(BaseModel):
    id: str
    name: str
    owner: str = ""
    description: str = ""
    output_channels: list[str] = Field(default_factory=list)
    state_schema: str = ""
    triggers: list[TriggerConfig]
    workflows: list[WorkflowConfig]
    enabled: bool = True


class AuthorityConfig(BaseModel):
    """Defines what actions a Role can take autonomously."""

    autonomous: list[str] = Field(default_factory=list)
    needs_approval: list[str] = Field(default_factory=list)
    forbidden: list[str] = Field(default_factory=list)

    def can_act(self, action: str) -> str:
        """Returns: 'autonomous' | 'needs_approval' | 'forbidden'."""
        if action in self.forbidden:
            return "forbidden"
        if action in self.needs_approval:
            return "needs_approval"
        if action in self.autonomous:
            return "autonomous"
        return "needs_approval"  # default: cautious


# ── V3 Event + Routing ─────────────────────────────────────────

class Event(BaseModel):
    id: str
    type: str              # "lead.created", "deal.stalled"
    source: str            # "hubspot", "slack", "temporal", human id
    domain: str            # "revenue", "marketing"
    payload: dict[str, Any]
    timestamp: datetime
    metadata: dict[str, Any] = Field(default_factory=dict)


class RoutingDecision(BaseModel):
    action: str            # "delegate" | "escalate" | "forward" | "ignore"
    reason: str
    operator_id: str | None = None
    trigger_id: str | None = None
    input_data: dict[str, Any] | None = None
    target_role_id: str | None = None
    message: str | None = None


# ── V3 Inter-Role ──────────────────────────────────────────────

class RoleMessage(BaseModel):
    id: str
    type: str              # "request" | "response" | "notification"
    from_id: str
    to_id: str
    content: str
    payload: dict[str, Any] = Field(default_factory=dict)
    correlation_id: str = ""
    timestamp: datetime | None = None


# ── V3 Workspace ───────────────────────────────────────────────

class WorkspacePolicy(BaseModel):
    max_roles: int = 100
    default_trust: float = 0.3
    spawn_requires_approval: bool = False
    memory_isolation: str = "strict"


class WorkspaceConfig(BaseModel):
    id: str
    name: str
    owner: str
    policy: WorkspacePolicy
    role_templates: dict[str, Any] = Field(default_factory=dict)


# ── V3 Lifecycle + Trust ───────────────────────────────────────

class RoleStatus(str, Enum):
    DRAFT = "draft"
    TESTING = "testing"
    ACTIVE = "active"
    SUSPENDED = "suspended"
    TERMINATED = "terminated"


class RoleLifecycle(BaseModel):
    status: RoleStatus
    created_at: datetime
    created_by: str
    activated_at: datetime | None = None
    terminated_at: datetime | None = None
    termination_reason: str = ""
    memory_policy: str = "archive"   # "archive" | "merge_to_parent" | "delete"


class TrustProfile(BaseModel):
    scores: dict[str, float] = Field(default_factory=dict)
    default: float = 0.3

    def trust_for(self, capability: str) -> float:
        return self.scores.get(capability, self.default)


# ── V3 Goals ──────────────────────────────────────────────────

class KeyResult(BaseModel):
    id: str
    description: str
    target: float
    current: float = 0.0
    unit: str = ""

    @property
    def progress(self) -> float:
        if self.target == 0:
            return 0.0
        return min(self.current / self.target, 1.0)


class Objective(BaseModel):
    id: str
    description: str
    key_results: list[KeyResult] = Field(default_factory=list)
    status: str = "active"   # "active" | "achieved" | "at_risk" | "abandoned"
    owner_id: str = ""


# ── V3 Role Templates + Specs ──────────────────────────────────

class RoleTemplate(BaseModel):
    template_id: str
    name_pattern: str
    soul_template: str
    domains: list[str]
    authority: AuthorityConfig | None = None
    operator_ids: list[str] = Field(default_factory=list)
    default_trust: float = 0.3
    ttl: str | None = None
    parameters: list[str] = Field(default_factory=list)
    allowed_spawners: list[str] = Field(default_factory=list)


class RoleSpec(BaseModel):
    role_id: str
    workspace: str
    soul: str
    domains: list[str]
    reports_to: str
    operator_ids: list[str]
    authority: AuthorityConfig | None = None
    goals: list[Objective] = Field(default_factory=list)
    trust: TrustProfile | None = None
    parent_role_id: str = ""
    created_by: str = ""
    ttl: str | None = None
    memory_policy: str = "archive"
