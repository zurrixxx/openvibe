# 4-Layer Architecture Design — OpenVibe Platform

> **Date:** 2026-02-18
> **Status:** Approved
> **Decision:** Restructure within v4/ (not v5)
> **Supersedes:** `proposed/INTER-OPERATOR-COMMS.md`, `proposed/OPERATOR-SDK.md`

---

## 1. Problem: Current Boundary Issues

The SDK (`v4/openvibe-sdk/`) currently mixes concerns across layers:

- `OperatorRuntime` — YAML config loading AND `graph.invoke()` execution — two concerns
- `RoleRuntime` — contains `scheduler: Any = None` (Temporal/platform concern bleeding into SDK)
- `Role` — V1/V2 dual memory compat shim adds ambiguity
- No platform services exist — HumanLoop, Gateway, Workspace are undefined

---

## 2. Decision: 4-Layer Architecture within v4/

```
v4/
├── openvibe-sdk/          # Layer 1 — pure primitives, zero infra deps
├── openvibe-runtime/      # Layer 2 — LangGraph + execution, new package
├── openvibe-platform/     # Layer 3 — deployed services, new package
├── openvibe-cli/          # Layer 4 — multi-instance CLI, new package
├── vibe-ai-adoption/      # dogfooding app — untouched until layers ready
└── docs/                  # design docs
```

**Why not v5?** The folder `v4/` represents the current product generation. Packages have their own semver (`openvibe-sdk v0.2.0`). Adding a `v5/` folder would only add nesting with no benefit.

---

## 3. Layer Definitions

### Layer 1: `openvibe-sdk` (pure primitives)

`pip install openvibe-sdk` — zero infrastructure dependencies. Things you import and subclass.

**Keep:**
- `Role`, `Operator`, `@llm_node`, `@agent_node`
- Data models: `Fact`, `Episode`, `Insight`, `Event`, `RoutingDecision`, `RoleMessage`
- Protocol interfaces: `LLMProvider`, `RoleRegistry`, `RoleTransport`, `MemoryStore`, `EpisodicStore`, `InsightStore`
- Auth models: `AuthorityConfig`, `ClearanceProfile`, `TrustProfile`
- Test utilities: `InMemoryRegistry`, `InMemoryTransport`, `InMemoryXxxStore`
- V3 additions: `WorkspaceConfig`, `RoleTemplate`, `RoleSpec`, `RoleLifecycle`, `TrustProfile`, `Objective`, `KeyResult`

**Move out (to `openvibe-runtime`):**
- `OperatorRuntime` — YAML loading + LangGraph graph execution
- `RoleRuntime` — role instantiation + memory wiring

**Remove:**
- V1 `memory: MemoryProvider` compat path in `Role` — `respond()` uses V2 only
- `scheduler: Any` field from `RoleRuntime` — platform concern

### Layer 2: `openvibe-runtime` (new package)

`pip install openvibe-runtime` — depends on `openvibe-sdk` + `langgraph`. Has external library deps but no deployed services.

**Contains:**
- `OperatorRuntime` (migrated from SDK) — YAML config loading + LangGraph graph execution
- `RoleRuntime` (migrated from SDK, cleaned up) — role instantiation + memory wiring
- `AnthropicProvider` (or keep in SDK — TBD)
- Temporal client thin wrapper (client only, Temporal itself is a platform service)
- **Structured audit log** — every `@llm_node` / `@agent_node` auto-records: tokens in/out, latency, cost, role_id, operator_id. Implemented as decorator instrumentation.
- **Cost tracking** — per-role, per-workspace token cost aggregation from audit log
- **Testing mode** — `RoleRuntime(mode="test")` auto-injects `InMemoryTransport` + mock LLM

### Layer 3: `openvibe-platform` (new deployed service)

Not a library — a deployed application. FastAPI + Temporal + NATS + storage backends.

**Core services (P0 — platform can't run without these):**
- **REST API** (FastAPI) — workspace/role/task/deliverable CRUD; CLI and UI both use this
- **WorkspaceService** — namespace isolation, policy enforcement, workspace CRUD
- **RoleGateway** — routes events to correct Role, `RoleRegistry` real implementation (DB-backed)
- **HumanLoopService** — approval queue + deliverable staging; approvals unblock Temporal workflows

**High-value additions (P1 — build alongside P0):**
- **Webhook ingestion gateway** — HubSpot/Slack/any webhook → standard `Event` → RoleGateway; the bridge between external world and roles
- **File-based MemoryFilesystem** — real filesystem backend; memory survives restarts, debuggable with `cat`/`ls`/`grep`
- **Scheduled reflect()** — Temporal cron triggers weekly `role.reflect()` per active role; agents get smarter automatically

**Deferred (P2+):**
- NATS transport (real cross-process RoleTransport)
- Postgres + pgvector memory backend (file-based first)
- S1/S2 cognitive loop (V4 scope)
- Cross-workspace communication (multi-instance: workspaces are isolated by design)

### Layer 4: `openvibe-cli` (new package)

`pip install openvibe-cli` — talks to `openvibe-platform` REST API.

```
vibe workspace list/create/switch
vibe role list/spawn/inspect
vibe task list/approve/reject
vibe deliverable list/view
vibe logs --role cro --follow        # streaming audit log tail
vibe cost --workspace vibe-team      # token cost breakdown
```

`--host` flag points to different platform instances (multi-instance model: each company self-hosts).

---

## 4. How vibe-ai-adoption Uses This

As a "real user" of the SDK, it only touches three things:

```python
# 1. pip install openvibe-sdk openvibe-runtime
# Define custom operators and roles
class CRORole(Role):
    role_id = "cro"
    soul = "souls/cro.md"
    operators = [RevenueOpsOperator]
    domains = ["revenue", "pipeline"]

# 2. workspace.yaml — declarative config, no code
workspace: vibe-team
owner: charles
roles:
  - role_id: cro
    soul: souls/cro.md
    domains: [revenue, pipeline]
    reports_to: charles
    operator_ids: [revenue_ops]

# 3. Deploy openvibe-platform (self-hosted)
# Platform handles: scheduling, memory, routing, human loop
```

vibe-ai-adoption does NOT import `openvibe-platform` or `openvibe-cli` — it deploys the platform and uses the CLI to operate it.

---

## 5. Human-in-the-Loop Protocol

The mechanism spans layers but each layer has a single, clear responsibility:

```
Role.handle(event)
  → RoutingDecision(action="escalate")      # SDK: declares WHAT
        ↓
RoleGateway (Platform)                      # Platform: receives decision
        ↓
HumanLoopService → creates ApprovalRequest # Platform: manages state
        ↓
REST API → CLI / UI notification            # Interface: surfaces to human
        ↓
Human approve / reject
        ↓
HumanLoopService → signals Temporal         # Platform: resumes workflow
        ↓
Execution continues or cancels
```

SDK only says "I need approval." Platform decides how to ask. UI decides how to show.

**Deliverables follow the same pattern:** Role produces output → Platform stages as `Deliverable` → UI/CLI surfaces for human review.

---

## 6. Communication Model

### Within a workspace (same deployment):
```
CRO.request_role("bdr-apac", "qualify this lead")
  → RoleRegistry.get("vibe-team", "bdr-apac")   # lookup
  → RoleTransport.send(from, to, message)         # deliver
  → same process: InMemoryTransport (SDK, tests)
  → distributed: NATSTransport (Platform, P2)
```

### Cross-workspace:
Workspaces are isolated by design (multi-instance model). Cross-workspace communication is explicitly out of scope. Two separate platform deployments do not communicate.

---

## 7. Feature Priority Summary

| Priority | Package | Feature | Rationale |
|----------|---------|---------|-----------|
| P0 | sdk | V1 shim removal, Layer split | Cleanup enables everything else |
| P0 | sdk | V3: handle, spawn, lifecycle, trust, goals, ambient tools | Already designed, implement |
| P0 | runtime | OperatorRuntime + RoleRuntime migration | Required for layer separation |
| P0 | platform | REST API skeleton + WorkspaceService + RoleGateway + HumanLoopService | Minimum viable platform |
| P1 | runtime | Audit log + cost tracking | One-time addition, permanent value |
| P1 | runtime | Testing mode | DX critical for SDK users |
| P1 | platform | Webhook ingestion gateway | vibe-ai-adoption needs HubSpot/Slack |
| P1 | platform | File-based MemoryFilesystem | Real persistence, debuggability |
| P1 | platform | Scheduled reflect() | Automatic learning loop |
| P2 | cli | Core commands + --host flag | After platform basic APIs exist |
| P3 | platform | NATS transport | After in-process transport proven |
| defer | platform | Postgres/pgvector | File-based memory first |
| defer | sdk | S1/S2 cognitive loop | V4 scope |

---

## 8. What Doesn't Change

- `v4/vibe-ai-adoption/` — untouched until platform Layer 3 has basic APIs ready
- All existing SDK tests (216 passing) — migration must keep green
- V3 Role design (`2026-02-18-sdk-v3-design.md`) — this document builds on top of it, doesn't replace it
- Design principles: SOUL, progressive disclosure, feedback loop, observable everything

---

*Last updated: 2026-02-18*
