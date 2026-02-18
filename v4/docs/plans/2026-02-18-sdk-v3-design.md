# SDK V3 Design — Autonomous Roles

> **Date:** 2026-02-18
> **Status:** Draft (approved for doc write-up)
> **Depends on:** SDK V2 (v0.2.0, 216 tests, complete)
> **Version target:** 0.3.0

---

## 1. V3 Scope

SDK V3 makes a Role a fully autonomous agent: it can receive events, decide what to do, communicate with peers, know its objectives, spawn child Roles, and manage trust.

**SDK decides, gateway delivers.** The SDK gives a Role everything it needs to function as an autonomous agent. How events arrive, how decisions get executed, how messages get transported, how spaces render — all gateway concerns.

---

## 2. Role Object — Current State (V2)

### A. Identity — "我是谁"

| Field | Type | Purpose | Validation |
|---|---|---|---|
| `role_id` | `str` | Unique identifier | Tested |
| `soul` | `str` | Persona description or .md file path | Tested, no real soul files used |
| `authority` | `AuthorityConfig` | 3-level: autonomous / needs_approval / forbidden | Tested, `can_act()` is pure logic |
| `clearance` | `ClearanceProfile` | Info access by domain x classification | Tested, filters Facts |

### B. Capabilities — "我能用什么"

| Field/Method | Purpose | Validation |
|---|---|---|
| `operators` | List of Operator types this Role can invoke | Tested |
| `list_operators()` | Returns operator_id list | Trivial |
| `get_operator(id)` | Creates Operator instance with Role-aware LLM + MemoryAssembler | Tested, core seam |
| `_RoleAwareLLM` | Wraps LLM, auto-injects soul + memory on every call | Tested |

### C. Cognition — "我怎么想"

| Method | Purpose | Validation |
|---|---|---|
| `respond(message)` | LLM conversation with soul + memory context, auto-records episode | Tested (mock LLM only) |
| `build_system_prompt()` | Assembles: soul + V1 memory or V2 insights + base prompt | Tested |
| `reflect()` | Compresses episodes → insights via LLM analysis | Tested (mock LLM only) |

### D. Memory — "我知道什么"

| Field/Method | Purpose | Validation |
|---|---|---|
| `memory` | V1 simple KV memory (MemoryProvider) | Tested, superseded by V2 |
| `agent_memory` | V2: episodes(L2) + insights(L3) + workspace ref | Tested, all in-memory |
| `memory_fs` (property) | Virtual filesystem view (.directory index) | Tested |
| `AgentMemory.record_episode()` | Records operation history | Auto-triggered |
| `AgentMemory.recall_insights()` | Recalls by domain/tags/query | Tested |
| `AgentMemory.reflect()` | L2 → L3 distillation | Tested (mock LLM) |
| `AgentMemory.publish_to_workspace()` | High-confidence insights → workspace facts | Tested |

### E. Infrastructure (injected at runtime)

| Field | Purpose |
|---|---|
| `llm` | LLMProvider protocol |
| `config` | Extra config dict |

---

## 3. Honest Assessment — What's Real vs Placeholder

### Solid (pattern proven, logic sound):
- Operator + @llm_node + @agent_node decorator pattern
- Role wrapping LLM (_RoleAwareLLM auto-injects soul)
- Authority 3-level permission check
- Memory 3-tier (Fact/Episode/Insight) + distillation pipeline
- MemoryFilesystem .directory navigation
- ClearanceProfile access filtering logic

### Placeholder (code + tests exist, but no real-world validation):
- `respond()` — only tested with mock LLM, no real CRO conversations
- `reflect()` — requires LLM to output specific JSON, never run against real model
- `ClearanceProfile` — filtering works, but info isolation never tested in multi-agent scenario
- `publish_to_workspace()` — never used in agent A → agent B flow
- `build_system_prompt()` — assembly logic works, prompt quality under real LLM unknown

### Completely Missing (V3 scope):
- Role has no `domains` — doesn't know what it's responsible for
- Role has no `handle(event)` — can't receive events or make routing decisions
- Role has no `reports_to` — doesn't know who to escalate to
- Roles can't communicate — no registry, transport, message model
- Role has no goals — doesn't know what OKRs it's pursuing
- Role has no tools at respond() level — can't introspect memory/goals during conversation
- Role has no lifecycle — no states, no trust tracking
- Role can't spawn child Roles — no templates, no creation process
- No Workspace concept — no namespace, no isolation boundary

---

## 4. V3 Design — What to Add

### 4.1 Workspace

Workspace is the namespace + isolation boundary + policy container. Every Role belongs to a Workspace.

```python
@dataclass
class WorkspaceConfig:
    id: str                     # "vibe-team"
    name: str                   # "Vibe AI Team"
    owner: str                  # human_id — ultimate authority
    policy: WorkspacePolicy
    role_templates: dict[str, RoleTemplate] = {}

@dataclass
class WorkspacePolicy:
    max_roles: int = 100
    default_trust: float = 0.3
    spawn_requires_approval: bool = False
    memory_isolation: str = "strict"  # "strict" | "shared_read"
```

Roles within a Workspace can communicate and share memory. Cross-Workspace is default-isolated, handled by gateway.

### 4.2 Event Model

Standard event type that Roles receive from gateway layer.

```python
@dataclass
class Event:
    id: str
    type: str              # "lead.created", "deal.stalled", "directive.spawn"
    source: str            # "hubspot", "slack", "temporal", "charles"
    domain: str            # "revenue", "marketing", "product"
    payload: dict          # event-specific data
    timestamp: datetime
    metadata: dict = {}    # optional: priority, correlation_id, etc.
```

- `domain` is explicit on the Event, tagged by gateway before dispatch.
- `type` uses dot-notation namespacing.
- Flat data object, no inheritance.

### 4.3 Routing Decision + Role.handle()

```python
@dataclass
class RoutingDecision:
    action: str            # "delegate" | "escalate" | "forward" | "ignore"
    reason: str            # human-readable explanation

    # For "delegate"
    operator_id: str | None = None
    trigger_id: str | None = None
    input_data: dict | None = None

    # For "escalate" / "forward"
    target_role_id: str | None = None
    message: str | None = None
```

Role gains:

```python
class Role:
    # V3 class fields
    workspace: str = ""
    domains: list[str] = []
    reports_to: str = ""       # role_id or human_id — SDK doesn't care

    def handle(self, event: Event) -> RoutingDecision:
        """Receive event, decide what to do."""
        # Step 1: Domain check — is this mine?
        if not self._is_my_domain(event):
            owners = self._registry.find_by_domain(self.workspace, event.domain)
            if owners:
                return RoutingDecision(action="forward", target_role_id=owners[0].id, ...)
            return RoutingDecision(action="ignore", ...)

        # Step 2: Authority check — am I allowed?
        authority = self.can_act(event.type)
        if authority == "forbidden":
            return RoutingDecision(action="escalate", target_role_id=self.reports_to, ...)

        # Step 3: Route to operator via _match_operator()
        operator_id, trigger_id = self._match_operator(event)
        if operator_id:
            if authority == "needs_approval":
                return RoutingDecision(action="escalate", target_role_id=self.reports_to, ...)
            return RoutingDecision(action="delegate", operator_id=operator_id, ...)

        # Step 4: Escalate if no match
        return RoutingDecision(action="escalate", target_role_id=self.reports_to, ...)

    def _match_operator(self, event: Event) -> tuple[str | None, str | None]:
        """Subclass overrides to define event -> operator mapping."""
        return None, None
```

Key decisions:
- `handle()` is deterministic, no LLM call. Pure routing logic. Fast.
- `_match_operator()` is a hook for subclasses.
- `reports_to` is a plain string ID. Could be agent or human. SDK doesn't distinguish — gateway resolves delivery.
- `needs_approval` events produce an "escalate" decision so gateway can queue for approval.

### 4.4 Inter-Role Protocol

```python
@dataclass
class Participant:
    id: str
    type: str              # "role" | "human"
    name: str = ""
    domains: list[str] = []
    metadata: dict = {}    # gateway-specific: slack_id, email, etc.

class RoleRegistry(Protocol):
    def get(self, workspace: str, role_id: str) -> Participant | None: ...
    def list_roles(self, workspace: str) -> list[Participant]: ...
    def find_by_domain(self, workspace: str, domain: str) -> list[Participant]: ...
    def register(self, spec: RoleSpec) -> str: ...
    def remove(self, workspace: str, role_id: str) -> None: ...
    def queue_spawn(self, spec: RoleSpec) -> str: ...

class RoleTransport(Protocol):
    def send(self, from_id: str, to_id: str, message: RoleMessage) -> None: ...
    def request(self, from_id: str, to_id: str, message: RoleMessage) -> RoleMessage: ...

@dataclass
class RoleMessage:
    id: str
    type: str              # "request" | "response" | "notification"
    from_id: str
    to_id: str
    content: str
    payload: dict = {}
    correlation_id: str = ""
    timestamp: datetime = None
```

Role gains:

```python
class Role:
    _registry: RoleRegistry | None = None
    _transport: RoleTransport | None = None

    def request_role(self, target_id: str, message: str, payload: dict = {}) -> RoleMessage:
        """Send request to another Role (or human). Blocking."""

    def notify_role(self, target_id: str, message: str) -> None:
        """Fire-and-forget notification."""
```

SDK ships:
- `InMemoryRegistry` — dict-based, for tests
- `InMemoryTransport` — direct function call, for tests

Key decisions:
- `request()` is synchronous at SDK level. Async is gateway concern.
- Registry and Transport are protocols. Gateway provides real implementations.
- `find_by_domain()` enables "forward" action in `handle()`.
- Registry is scoped per workspace.

### 4.5 Goal Model

```python
@dataclass
class Objective:
    id: str
    description: str           # "Grow Q1 pipeline to $2M"
    key_results: list[KeyResult]
    status: str = "active"     # "active" | "achieved" | "at_risk" | "abandoned"
    owner_id: str = ""

@dataclass
class KeyResult:
    id: str
    description: str           # "Qualify 200 leads per month"
    target: float              # 200
    current: float = 0         # 142
    unit: str = ""             # "leads", "$", "%"

    @property
    def progress(self) -> float:
        if self.target == 0:
            return 0.0
        return min(self.current / self.target, 1.0)
```

Role gains:

```python
class Role:
    goals: list[Objective] = []

    def active_goals(self) -> list[Objective]: ...
    def goal_context(self) -> str:
        """Format goals for LLM prompt injection."""
```

Key decisions:
- Goals are plain data, not an engine. No auto-decomposition.
- `goal_context()` returns string for prompt injection.
- Goals set externally by human. Role doesn't create its own goals in V3.
- `handle()` does NOT use goals in V3. Goals inform LLM calls only.

### 4.6 Tools — Ambient vs Domain

Two categories of tools, living at different layers:

| Tool Type | Layer | Examples |
|---|---|---|
| **Ambient tools** (introspection) | Role | Recall memory, check goals, lookup registry, check authority |
| **Domain tools** (external actions) | Operator | HubSpot API, Slack messaging, database queries |

Current state: `@agent_node(tools=[...])` provides domain tools at Operator level. But `Role.respond()` is a bare LLM call with no tools.

V3 adds ambient tools to Role:

```python
class Role:
    def _ambient_tools(self) -> list[Callable]:
        """Tools always available during respond() — introspection only."""
        tools = []
        if self.agent_memory:
            tools.append(self._tool_recall_memory)
        if self.goals:
            tools.append(self._tool_check_goals)
        if self._registry:
            tools.append(self._tool_lookup_role)
        return tools

    def respond(self, message: str, context: str = "") -> LLMResponse:
        """V3: upgraded to agent loop with ambient tools.
        Role can introspect its own memory, goals, and registry during conversation."""
```

Key decisions:
- Ambient tools are auto-provided. Developer doesn't configure them.
- Domain tools stay on Operator (`@agent_node`). Role.respond() never calls HubSpot directly.
- When Role needs external data, it delegates to an Operator.
- `respond()` becomes an agent loop (like `@agent_node`) instead of a single LLM call.

### 4.7 Role Lifecycle + State

Roles have a lifecycle state machine:

```
draft → testing → active → suspended → terminated
                    ↑          ↓
                    └──────────┘  (resume)
```

```python
class RoleStatus(str, Enum):
    DRAFT = "draft"              # Being configured, doesn't accept events
    TESTING = "testing"          # Sandbox mode — handle() works, transport is mock
    ACTIVE = "active"            # Fully operational
    SUSPENDED = "suspended"      # Paused — no new events, memory preserved
    TERMINATED = "terminated"    # Done — memory archived, removed from registry

@dataclass
class RoleLifecycle:
    status: RoleStatus
    created_at: datetime
    created_by: str              # parent role_id or human_id
    activated_at: datetime | None = None
    terminated_at: datetime | None = None
    termination_reason: str = ""  # "task_complete" | "human_decision" | "parent_terminated"
    memory_policy: str = "archive"  # "archive" | "merge_to_parent" | "delete"
```

Role gains:

```python
class Role:
    lifecycle: RoleLifecycle | None = None

    def handle(self, event: Event) -> RoutingDecision:
        # V3: check lifecycle first
        if self.lifecycle and self.lifecycle.status not in (RoleStatus.ACTIVE, RoleStatus.TESTING):
            return RoutingDecision(action="ignore", reason=f"Role is {self.lifecycle.status}")
        # ... rest of routing logic
```

Key decisions:
- `handle()` checks lifecycle status before any routing.
- `testing` status runs real logic but gateway provides sandbox transport/tools.
- On termination, `memory_policy` controls what happens to accumulated knowledge.
- `merge_to_parent` is critical for task-bound Roles — insights flow back to parent.

### 4.8 Trust — Per-Capability Confidence

Authority says "you're allowed to do X". Trust says "we believe you'll do X well."

```python
@dataclass
class TrustProfile:
    """Per-capability trust scores, earned through track record."""
    scores: dict[str, float] = {}     # capability -> 0.0-1.0
    default: float = 0.3              # default for new capabilities

    def trust_for(self, capability: str) -> float:
        return self.scores.get(capability, self.default)
```

Trust affects monitoring level, not permission:

| Trust | Behavior |
|---|---|
| < 0.3 | Every execution needs human review (effectively needs_approval) |
| 0.3 - 0.7 | Execute then report, human reviews async |
| > 0.7 | Silent execution, log only |

Trust updates from episode outcomes:

```python
def update_trust(trust: TrustProfile, episode: Episode, feedback: str | None):
    if feedback == "good" or episode.outcome.get("success"):
        trust.scores[episode.action] = min(1.0, trust.trust_for(episode.action) + 0.05)
    elif feedback == "bad":
        trust.scores[episode.action] = max(0.0, trust.trust_for(episode.action) - 0.15)
```

Asymmetric: trust builds slowly (+0.05), breaks fast (-0.15).

Role gains:

```python
class Role:
    trust: TrustProfile | None = None
```

### 4.9 Role Creation — Templates + Spawning

#### The Bootstrap Problem

Every system needs a starting point. Three creation paths:

```
Path 1: Bootstrap — Human creates Root Roles via config (system init)
Path 2: Directed spawn — Human tells Role to spawn from existing template
Path 3: Design new role — Human asks Role to design a new template
Path 4: Self-discovered — Role.reflect() detects spawn signals
```

#### RoleTemplate — Human-Defined, Agent-Parameterized

```python
@dataclass
class RoleTemplate:
    """Human-defined template. Agent fills parameters, can't change structure."""
    template_id: str
    name_pattern: str                  # "BDR - {territory}"
    soul_template: str                 # "You are a BDR covering {territory}. ..."
    domains: list[str]                 # fixed by template
    authority: AuthorityConfig         # fixed — ceiling, not floor
    operator_ids: list[str]            # which operators this role can use
    default_trust: float = 0.3
    ttl: str | None = None             # "task" | "90d" | None (permanent)
    parameters: list[str] = []         # ["territory", "focus_vertical"]
    allowed_spawners: list[str] = []   # which role_ids can use this template
    spawn_signals: list[SpawnSignal] = []  # auto-detection conditions
```

Key constraint: **Human controls structure (soul template, authority ceiling, domains). Agent only fills parameters.**

#### RoleSpec — Concrete Instance Definition

```python
@dataclass
class RoleSpec:
    """Concrete Role definition — either from config (root) or from spawn."""
    role_id: str
    workspace: str
    soul: str                          # filled-in soul (not template)
    domains: list[str]
    reports_to: str
    operator_ids: list[str]
    authority: AuthorityConfig
    clearance: ClearanceProfile | None = None
    goals: list[Objective] = []
    trust: TrustProfile | None = None
    parent_role_id: str = ""           # who spawned me (empty for root Roles)
    created_by: str = ""               # human_id or role_id
    ttl: str | None = None
    memory_policy: str = "archive"     # on termination
```

#### SpawnSignal — When to Auto-Detect Spawn Needs

```python
@dataclass
class SpawnSignal:
    """Human-defined conditions for when a Role should consider spawning."""
    id: str
    description: str
    conditions: list[SpawnCondition]
    extract_params: dict[str, str] = {}  # how to auto-fill template params

@dataclass
class SpawnCondition:
    metric: str          # "episodes_by_tag" | "time_share" | "unique_entities" | "payload_field"
    threshold: float
    window_days: int = 30
    tag_field: str = ""
    field: str = ""
    min_value: float = 0
```

#### Path 1: Bootstrap — Human Creates Root Roles

```yaml
# workspace config (YAML)
workspace: vibe-team
owner: charles
policy:
  max_roles: 100
  spawn_requires_approval: false

roles:
  - role_id: cro
    soul: souls/cro.md
    domains: [revenue, pipeline, deals]
    reports_to: charles
    operator_ids: [revenue_ops, company_intel]
    authority:
      autonomous: [qualify_lead, trigger_nurture, generate_report]
      needs_approval: [commit_deal_terms, change_pricing]
      forbidden: [sign_contracts, modify_own_authority]

role_templates:
  bdr:
    name_pattern: "BDR - {territory}"
    soul_template: |
      You are a BDR covering {territory}.
      Qualify inbound leads, do outbound prospecting.
    domains: [revenue]
    authority:
      autonomous: [qualify_lead, send_outreach]
      needs_approval: [schedule_demo]
      forbidden: [negotiate_price]
    operator_ids: [revenue_ops]
    parameters: [territory]
    allowed_spawners: [cro]
    spawn_signals:
      - id: volume_threshold
        description: "Lead volume in territory exceeds capacity"
        conditions:
          - metric: episodes_by_tag
            tag_field: territory
            threshold: 50
            window_days: 30
```

#### Path 2: Directed Spawn — Human Tells Role to Spawn

Human sends a directive event:

```python
Event(type="directive.spawn", source="charles", domain="revenue",
      payload={"template_id": "bdr", "params": {"territory": "APAC"}})
```

CRO's `handle()` recognizes `directive.spawn` and executes `spawn()`.

#### Path 3: Design New Role — Human Asks Role to Create Template

When no template exists for what's needed:

```python
class Role:
    def design_role(self, intent: str) -> RoleTemplateDraft:
        """Human describes need. Role uses LLM + domain knowledge to design template.
        Output is a draft — MUST be approved by human before it becomes usable."""
        templates = self._workspace.get_templates(self.role_id)
        insights = self.agent_memory.recall_insights(query=intent, limit=10)

        response = self.llm.call(
            system=self._build_design_prompt(templates, insights),
            messages=[{"role": "user", "content": intent}],
            tools=self._ambient_tools(),
        )

        return RoleTemplateDraft(
            proposed_by=self.role_id,
            intent=intent,
            template=self._parse_template(response),
            reasoning=response.content,
            status="pending_review",
        )

@dataclass
class RoleTemplateDraft:
    """Role-proposed template. Must be human-approved to become active."""
    proposed_by: str
    intent: str
    template: RoleTemplate
    reasoning: str
    status: str = "pending_review"    # pending_review -> approved -> active
                                      #                -> rejected
```

Flow: Human intent -> Role designs draft -> Human reviews -> Approved template added to workspace -> Spawn from template.

#### Path 4: Self-Discovered — reflect() Detects Spawn Signals

```python
class Role:
    def reflect(self) -> list[Insight]:
        """V2: compress episodes -> insights.
           V3: additionally detect spawn signals."""
        insights = self.agent_memory.reflect(self.llm)
        spawn_recs = self._detect_spawn_needs(insights)
        return insights

    def _detect_spawn_needs(self, insights: list[Insight]) -> list[SpawnRecommendation]:
        """Check each template's spawn_signals against recent episodes/insights."""
        recommendations = []
        for template in self._workspace.get_templates(self.role_id):
            for signal in template.spawn_signals:
                if signal.matches(insights, self.agent_memory):
                    recommendations.append(SpawnRecommendation(
                        template_id=template.template_id,
                        reason=signal.description,
                        confidence=signal.evaluate(insights),
                        suggested_params=signal.extract_params(insights),
                    ))
        return recommendations
```

Spawn signals are **human-defined, quantitative conditions** on templates. Role doesn't invent what kind of child it needs — it discovers when pre-defined conditions are met.

#### The spawn() Method

```python
class Role:
    def spawn(self, template_id: str, params: dict) -> str:
        """Create child Role from template. Returns new role_id."""
        # 1. Find template
        template = self._workspace.get_template(template_id)

        # 2. Permission check: am I an allowed spawner?
        if self.role_id not in template.allowed_spawners:
            raise PermissionError(...)

        # 3. Fill params -> RoleSpec
        spec = RoleSpec(
            role_id=template.name_pattern.format(**params).lower().replace(" ", "-"),
            workspace=self.workspace,
            soul=template.soul_template.format(**params),
            domains=template.domains,
            authority=template.authority,
            operator_ids=template.operator_ids,
            reports_to=self.role_id,
            parent_role_id=self.role_id,
            trust=TrustProfile(default=template.default_trust),
            ttl=template.ttl,
        )

        # 4. Workspace policy check
        if self._workspace.policy.spawn_requires_approval:
            return self._registry.queue_spawn(spec)

        # 5. Register
        new_role_id = self._registry.register(spec)

        # 6. Inherit relevant memory (confidence * 0.7)
        if self.agent_memory:
            relevant = self.agent_memory.recall_insights(
                domain=template.domains[0], tags=list(params.values()), limit=20,
            )
            child_memory = self._registry.get_memory(new_role_id)
            for insight in relevant:
                inherited = Insight(
                    ...insight,
                    confidence=insight.confidence * 0.7,
                    tags=[*insight.tags, "inherited"],
                )
                child_memory.store_insight(inherited)

        return new_role_id
```

Key constraints:

| Rule | Reason |
|---|---|
| Agent cannot write RoleTemplate from scratch | Prevents authority inflation |
| Only allowed_spawners can use a template | Human controls who spawns what |
| Template authority is a ceiling | Child Role permissions <= template <= parent Role |
| Inherited memory discounted at 0.7x | Inherited knowledge must be self-verified |
| Workspace policy can require approval | High-security environments need human sign-off |
| design_role() output is always a draft | New templates always require human approval |

#### Summary: Four Creation Paths

| Path | Initiated by | Designed by | Approved by | Template required |
|---|---|---|---|---|
| Bootstrap | Human | Human | — | Human writes config |
| Directed spawn | Human (directive) | Template + Role fills params | Optional | Must exist |
| Design new role | Human (intent) | Role (LLM + domain knowledge) | Human must approve draft | Role creates draft |
| Self-discovered | Role (reflect) | Template + Role fills params | Optional | Must exist |

---

## 5. Role Object — Full V3 Map

```
Role
├── Identity (我是谁)
│   ├── role_id             V1
│   ├── soul                V1
│   ├── workspace           V3 — namespace
│   ├── domains             V3 — what I'm responsible for
│   └── reports_to          V3 — who I escalate to (agent or human)
│
├── Authority (我能做什么)
│   ├── authority            V2 — autonomous / needs_approval / forbidden
│   ├── clearance            V2 — info access by domain x classification
│   └── trust               V3 — per-capability trust scores, affects monitoring
│
├── Capabilities (我有什么能力)
│   ├── operators            V1 — Operator types I can invoke
│   ├── ambient_tools        V3 — introspection: memory, goals, registry
│   ├── get_operator()       V1
│   └── list_operators()     V1
│
├── Cognition (我怎么想)
│   ├── respond()            V2 → V3 upgraded to agent loop with ambient tools
│   ├── handle(event)        V3 — event routing: domain → authority → delegate/escalate
│   ├── reflect()            V2 → V3 extended with spawn signal detection
│   ├── design_role(intent)  V3 — design new RoleTemplate draft from human intent
│   └── build_system_prompt() V2
│
├── Memory (我知道什么)
│   ├── agent_memory         V2 — episodes + insights + workspace
│   ├── memory_fs            V2 — virtual filesystem
│   └── memory (V1 compat)   V1
│
├── Communication (我怎么跟别人沟通)
│   ├── request_role()       V3 — send request, get response
│   ├── notify_role()        V3 — fire-and-forget
│   ├── _registry            V3 — discover peers
│   └── _transport           V3 — message delivery
│
├── Goals (我在追什么目标)
│   ├── goals                V3 — OKRs
│   ├── active_goals()       V3
│   └── goal_context()       V3 — format for prompt injection
│
├── Creation (我怎么来的 / 我能创建谁)
│   ├── spawn(template, params) V3 — create child Role from template
│   ├── design_role(intent)  V3 — propose new template (needs human approval)
│   ├── parent_role_id       V3
│   └── _workspace           V3 — templates + policy
│
├── Lifecycle (我现在什么状态)
│   ├── lifecycle            V3 — draft/testing/active/suspended/terminated
│   ├── trust                V3 — per-capability trust profile
│   └── memory_policy        V3 — what happens to memory on termination
│
└── Infrastructure (注入的依赖)
    ├── llm                  V1
    └── config               V1
```

---

## 6. New Public API Summary

### New Types (~20 exports)

```python
# Workspace
WorkspaceConfig, WorkspacePolicy,

# Event + Routing
Event, RoutingDecision,

# Inter-Role
Participant, RoleRegistry, RoleTransport, RoleMessage,
InMemoryRegistry, InMemoryTransport,

# Goals
Objective, KeyResult,

# Lifecycle + Trust
RoleStatus, RoleLifecycle, TrustProfile,

# Creation
RoleTemplate, RoleSpec, RoleTemplateDraft, SpawnSignal, SpawnRecommendation,
```

### New Role Surface

| Category | Method/Field |
|---|---|
| Identity | `workspace`, `domains`, `reports_to` |
| Authority | `trust: TrustProfile` |
| Cognition | `handle(event)`, `_match_operator(event)`, `design_role(intent)` |
| Cognition | `respond()` upgraded with ambient tools |
| Cognition | `reflect()` extended with spawn detection |
| Communication | `request_role()`, `notify_role()` |
| Goals | `goals`, `active_goals()`, `goal_context()` |
| Creation | `spawn(template_id, params)` |
| Lifecycle | `lifecycle: RoleLifecycle` |

---

## 7. Design Boundary

**SDK decides, gateway delivers.**

| SDK Responsibility | Gateway Responsibility |
|---|---|
| Routing logic (handle) | Event dispatch (webhooks, NATS, cron) |
| Authority + trust checks | Approval UI, notification delivery |
| Spawn validation (template, permissions) | Process/resource allocation for new Roles |
| Memory inheritance rules | Persistence (Postgres, S3) |
| Lifecycle state machine | State transitions (timers, GC) |
| Registry protocol | Registry implementation (DB-backed) |
| Transport protocol | Transport implementation (NATS, HTTP) |
| Ambient tools (introspection) | Domain tools infrastructure (API keys, rate limits) |
| Collaboration spaces: NOT in SDK | Spaces, rendering, message history |

---

## 8. Explicitly Out of Scope (deferred)

- Confidence/impact matrix (V4 — needs S1/S2 cognitive loop)
- Autonomous sub-goal generation (V4)
- Real Postgres/pgvector stores (separate package)
- Collaboration spaces (gateway layer)
- Daily prioritization engine (V4)
- S1/S2 fast/slow cognition paths (V4)
- Cross-workspace communication protocol (gateway)

---

*Last updated: 2026-02-18T03:53Z*
