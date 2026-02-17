# Role Layer Design — AI Employee Architecture

> Created: 2026-02-17T20:43:43Z
> Status: Design approved, pending implementation
> Builds on: SDK V1 (87 tests), 4-Layer Architecture

## 1. Vision

A Role is an **AI Employee** — not a wrapper, not middleware. You hire it, give it goals, and it works.

```
Company (AI-native)
├── CEO (human)
│   ├── CRO (AI Role) — owns revenue, reports weekly
│   ├── CMO (AI Role) — owns marketing, collaborates with CRO
│   └── Eng Lead (human)
│       └── DevOps Agent (AI Role)
```

A Role can:
- Respond to conversations
- Receive and decompose tasks
- Pursue goals autonomously
- Report to its manager
- Allocate resources (operators) to get work done
- Learn and evolve over time
- Create new capabilities when needed

## 2. Role Data Model

Everything a Role is and knows lives in a unified **memory filesystem**:

```
/role/{role_id}/
├── /identity/        ← WHO I am (L0)
├── /goals/           ← WHAT I want (L0/L1)
├── /relationships/   ← WHO I know (L0)
├── /knowledge/       ← WHAT I know (L1/L2)
├── /experience/      ← WHAT happened (L2)
├── /references/      ← EXTERNAL resources (L2)
└── /operators/       ← WHAT I can do (L0/L1)
```

Seven directories. One filesystem. The LLM browses and searches. The system extracts structured views. All access is observable.

### 2.1 Identity (`/identity/`)

Soul — who the Role is. Personality, values, communication style.

```
/identity/
└── soul.md        ← "You are the CRO of Vibe. Data-driven, aggressive but measured..."
```

- Always loaded (L0)
- Rarely changes — set at "hire" time
- Plain text, consumed directly by LLM

### 2.2 Goals (`/goals/`)

Recursive GoalTree — framework-agnostic, natural language criteria.

```
/goals/
├── mission.md                    ← permanent mission
├── q3-pipeline/
│   ├── goal.md                   ← "100 qualified leads by March 31"
│   ├── outbound-campaign/        ← project
│   │   ├── project.md
│   │   └── tasks/
│   └── webinar-followup/         ← project
│       ├── project.md
│       └── tasks/
└── q3-conversion/
    └── goal.md
```

Every node is the same shape — **GoalNode**:

```yaml
id: "g-001"
description: "Generate 100 qualified leads by March 31"
success_criteria: "100 leads scored >70 in CRM"    # natural language
timeframe: {start: "2026-01-01", end: "2026-03-31"}
status: in_progress
progress: 0.34                                      # self-assessed
parent: "mission-revenue"
children: ["p-001", "p-002"]
```

**Framework-agnostic:** OKR maps naturally (Objective = Goal, Key Result = Project). V2MOM, SMART, Rocks — any framework works. The tree structure is the same; framework is just labeling.

Optional `framework_metadata` for companies that need structured metrics:

```yaml
framework_metadata:
  type: "key_result"
  metric: "qualified_leads"
  target: 100
  current: 34
```

**Who sets goals:**
- Manager (human/parent Role) sets Mission + top-level Goals
- Role itself decomposes Goals → Projects → Tasks (via S2 Plan)
- Role proposes new Goals when it sees opportunity

### 2.3 Relationships (`/relationships/`)

Natural language descriptions. No type taxonomy.

```
/relationships/
├── ceo.md       ← "My boss. Weekly reports. Prefers data over narrative."
├── cmo.md       ← "Peer. We collaborate on campaigns. Share pipeline data."
├── sdr.md       ← "I manage them. Assign lead qualification tasks."
└── research.md  ← "I can request research from them when needed."
```

- Stored as structured data (target + description) for gateway routing, UI org charts
- Rendered as natural language for LLM consumption
- Relationship type is implicit in the description — the LLM naturally understands "my boss" vs "peer" vs "I manage them"

### 2.4 Knowledge (`/knowledge/`)

Learned principles, domain knowledge, organized by namespace.

```
/knowledge/
├── sales/
│   ├── qualification/
│   │   ├── principles.md    ← "VP sponsor predicts conversion"
│   │   └── scoring-notes.md
│   └── competitors/
│       ├── competitor-x.md
│       └── competitor-y.md
├── product/
│   └── features/
└── market/
    └── trends-2026.md
```

Principles (the "playbook") are not a separate concept — they're files within their domain directory. "VP sponsor predicts conversion" lives in `/knowledge/sales/qualification/`, not in a generic playbook.

### 2.5 Experience (`/experience/`)

Raw event log — what happened, when.

```
/experience/
├── 2026-02/
│   ├── 10-acme-qualified.md
│   ├── 14-webinar-leads.md
│   └── 17-beta-corp-stalled.md
└── 2026-03/
```

Source material for learning. Periodic review extracts patterns → promotes to `/knowledge/` as principles.

### 2.6 References (`/references/`)

External documents — summary + pointer, not full content.

```
/references/
├── q2-report.md        ← summary + pointer to gdrive
├── b2b-article.md      ← summary + pointer to URL
└── product-roadmap.md  ← summary + pointer
```

Role doesn't memorize the book. It remembers what it learned and where to find the original.

### 2.7 Operators (`/operators/`)

What the Role can do — declarative knowledge of its own capabilities.

```
/operators/
├── system/              ← built-in (every Role)
│   ├── think.md
│   ├── research.md
│   ├── plan.md
│   ├── remember.md
│   ├── communicate.md
│   ├── create_operator.md
│   └── ask_help.md
│
├── revenue_ops/         ← assigned at hire time
│   ├── _meta.md         ← "what this does, when to use"
│   ├── qualify.md       ← workflow description + params
│   └── score.md
│
├── content_engine/      ← assigned
│   ├── _meta.md
│   ├── draft.md
│   └── review.md
│
└── lead_scorer/         ← self-created via create_operator
    ├── _meta.md
    ├── score.md
    └── _origin.md       ← "why I created this"
```

Two sides:
- **Filesystem** = declarative (what it does, when to use, usage stats)
- **Runtime** = executable (Python code, LangGraph graphs, tool functions)

Like a human: you know you can drive (declarative), but driving itself is muscle memory (procedural).

Usage tracking for self-improvement:

```yaml
# /operators/revenue_ops/_meta.md
usage:
  total_calls: 47
  success_rate: 0.82
  avg_duration: 45s
  notes:
    - "Works well for inbound leads"
    - "Struggles with partner referrals"
```

### 2.8 SystemOperator

Every Role comes pre-installed with a SystemOperator — basic "employee competence":

| Ability | Sync/Async | Purpose |
|---------|-----------|---------|
| think() | sync | Reason about something (single LLM call) |
| recall() | sync | Search memory filesystem |
| remember() | sync | Store to memory |
| respond() | sync | Generate chat response |
| ask_help() | sync | Escalate to human/role |
| communicate() | sync | Send message, report |
| research() | async | Multi-step investigation |
| plan() | async | Decompose goal into tasks |
| create_operator() | async | Build new operator |
| assess_goals() | sync | Evaluate goal progress |
| periodic_review() | async | Compress experience → knowledge |

SystemOperator uses the same Operator abstraction as domain operators. It benefits from `_RoleAwareLLM` — soul + memory injected into every LLM call.

## 3. Runtime Architecture — Hybrid C

```
┌─────────────────────┐
│  Conversation Layer  │ ← Slack/API/chat (the "mouth")
│  (stateless gateway) │
└──────────┬──────────┘
           │ events
┌──────────▼──────────┐
│  Temporal            │ ← durable execution (the "spine")
│  ├─ task workflows   │
│  ├─ cron (proactive) │
│  └─ long-running     │
└──────────┬──────────┘
           │
┌──────────▼──────────┐
│  Memory Filesystem   │ ← identity + context (the "brain")
│  L0/L1/L2 tiers     │
│  Browse + Search     │
│  Observable access   │
└─────────────────────┘
```

## 4. Cognitive Model — S1/S2 (Kahneman)

Inspired by *Thinking, Fast and Slow*. System 1 always fires. System 2 activates only when S1 can't handle it.

### 4.1 System 1 (Fast)

```
Any input → S1 (small/fast model)
         → loads: L0 context only (soul + active goals + relationships + core knowledge)
         → attempts response
         → self-assesses confidence
         → confident? → respond directly
         → uncertain? → escalate to S2
```

S1's prompt encodes the escalation rule: "If you can answer confidently, respond directly. If this requires planning, research, or multi-step work, respond with `<needs_s2/>` and briefly explain why."

No separate classifier. S1 IS the classifier — like a human, it naturally knows when something is beyond quick intuition.

**S1 handles:** casual chat, simple Q&A, acknowledgements, status from memory, goal updates.

### 4.2 System 2 (Slow) — Plan-Execute-Reflect

Activates only when S1 escalates. Full context, full capabilities.

```
┌──────────────────────────────────────────────┐
│  PLAN (synchronous, seconds)                  │
│  Context: L0 + pull relevant L1              │
│  Tools: sync only (think, recall, browse)    │
│                                              │
│  → Browses /operators/ to discover options   │
│  → Recalls relevant experience/knowledge     │
│  → Produces execution plan:                  │
│    [{op: revenue_ops, wf: qualify, input: X},│
│     {op: content_engine, wf: draft, input: Y}]│
└──────────────────┬───────────────────────────┘
                   │ submit to Temporal
┌──────────────────▼───────────────────────────┐
│  EXECUTE (asynchronous, minutes to hours)     │
│  Temporal runs plan steps durably             │
│  Role brain is NOT active — it's "asleep"    │
│  Each step = operator workflow invocation     │
└──────────────────┬───────────────────────────┘
                   │ execution complete
┌──────────────────▼───────────────────────────┐
│  REFLECT (synchronous, seconds)               │
│  Context: L0 + execution results             │
│  Tools: sync (think, remember, communicate)  │
│                                              │
│  → "What happened? What worked?"             │
│  → Store insights to /experience/            │
│  → Update goal progress                      │
│  → Report results if needed                  │
│  → Maybe trigger new PLAN cycle              │
└──────────────────────────────────────────────┘
```

**Timescale distinction:** `agent_node` (SDK V1) runs a tight ReAct loop in seconds. S2 runs a coarse Plan-Execute-Reflect cycle across minutes to hours. They don't compete — `agent_node` operates INSIDE operator workflows; S2 operates ACROSS operators.

### 4.3 Input Handling

```
Input types and routing:

A: "How's the pipeline?"           → S1 responds from memory
B: "Qualify this lead from Acme"   → S1 escalates → S2 Plan-Execute-Reflect
C: "We got 50 webinar signups"     → S1 recognizes implicit task → S2
D: "What's our conversion rate?"   → S1 answers from knowledge, or escalates if uncertain
E: "Your Q3 target is $500K"       → S1 updates /goals/, acknowledges
F: [Temporal cron fires]            → S2 heartbeat (check goals, act if needed)
```

## 5. Three-Tier Memory Loading

Inspired by OpenViking (ByteDance).

```
┌──────────────────────────────────────────┐
│  L0: Active Context (~2000 tokens)        │
│  Always in prompt (every S1 and S2 call) │
│                                          │
│  /identity/soul.md                       │
│  /goals/ (active goals summary)          │
│  /relationships/ (all)                   │
│  /knowledge/**/principles.md (core)      │
│  /operators/ (capability summary)        │
└────────────────┬─────────────────────────┘
                 │
┌────────────────▼─────────────────────────┐
│  L1: Warm Context                         │
│  Loaded by S2 when relevant to task      │
│                                          │
│  /knowledge/{domain}/ (task-relevant)    │
│  /experience/ (recent, last 7 days)      │
│  /goals/{project}/ (active project)      │
│  /operators/{op}/ (detailed specs)       │
└────────────────┬─────────────────────────┘
                 │
┌────────────────▼─────────────────────────┐
│  L2: Cold Storage                         │
│  Searched on demand via recall()         │
│                                          │
│  /experience/ (older events)             │
│  /references/ (summaries + pointers)     │
│  /knowledge/ (distant domains)           │
│  /goals/ (archived/completed)            │
└──────────────────────────────────────────┘
```

S1 = L0 only. S2 = L0 + selectively pulls L1 + searches L2 on demand.

### 5.1 Access Patterns

**Browse** — agent navigates the filesystem:
```
ls /knowledge/sales/ → [qualification/, competitors/]
read /operators/revenue_ops/_meta.md → capability description
```

**Search** — semantic query, optionally scoped:
```
search("VP sponsor", scope="/knowledge/sales/") → principles.md (0.94)
search("VP sponsor") → searches all /knowledge/ (broader)
```

### 5.2 Observable Retrieval

Every memory access produces a trace:

```yaml
retrieval_trace:
  query: "VP sponsor conversion"
  trigger: "S2 Plan phase"
  steps:
    - action: browse
      path: /knowledge/sales/qualification/
      found: [principles.md, scoring-notes.md]
    - action: semantic_search
      scope: /knowledge/sales/
      results: [{file: principles.md, score: 0.94}]
    - action: load
      file: principles.md
      tokens: 340
  total_time_ms: 120
```

Critical for debugging "why did the agent say/do that?"

## 6. Learning & Evolution

### 6.1 Three Learning Mechanisms

**Reflect (after every S2 execution):**
```
Task completes → S2 Reflect phase
  → "What happened? What worked? What surprised me?"
  → Store to /experience/
```

**Periodic Review (heartbeat/scheduled):**
```
Weekly → scan /experience/ (recent)
  → extract patterns across events
  → patterns confirmed? → write principle to /knowledge/{domain}/
  → old principles invalid? → archive or remove
  → /operators/ usage stats → note what works, what doesn't
```

**Feedback Integration:**
```
Manager says "You're spending too much time on small deals"
  → reflect against /experience/
  → update /knowledge/ principles
  → adjust /goals/ priorities
```

### 6.2 Memory Lifecycle

```
New input (event, doc, feedback)
  → store in /experience/ or /references/

Periodic review:
  → compress events → principle in /knowledge/
  → promote high-value to L0 (core principles)
  → demote low-value from L0 → L1/L2

Decay:
  → memories not recalled in 30 days → lower relevance
  → below threshold → prune

Budget enforcement:
  → L0 exceeds ~2000 tokens? → force review, demote least relevant
```

### 6.3 Capability Evolution

Role creates new operators when existing ones don't fit:

```
Role: "I need a faster way to score partner referrals"
  → create_operator()
  → writes: /operators/partner_scorer/ (declarative)
  → registers: runtime executable (Python + LangGraph)
  → available for future S2 Plan phases
```

Operator usage tracking feeds back into learning:
```
/operators/revenue_ops/ success_rate drops
  → periodic_review notices
  → stores insight: "revenue_ops struggles with partner referrals"
  → may trigger create_operator for specialized handler
```

## 7. Relationship to Existing SDK V1

### What V1 Has (keep)
- `Operator` base class, `@llm_node`, `@agent_node` decorators
- `_RoleAwareLLM` transparent wrapping
- `LLMProvider`, `MemoryProvider` protocols
- `OperatorRuntime` for YAML-config operators

### What V1 Role Becomes
- Current `Role` = identity wrapper → evolves into AI Employee
- Current `RoleRuntime.activate()` = explicit dispatch → becomes S2 execution
- Current `build_system_prompt()` = soul + memory → becomes L0 context assembly

### New Components
- S1/S2 cognitive loop
- Memory filesystem (L0/L1/L2, browse + search, observable)
- GoalTree
- SystemOperator
- Conversation layer integration
- Temporal integration for S2 Execute

### Migration Path
SDK V1 continues to work. The new Role layer builds ON TOP of the existing Operator/node primitives. Operators don't change. The intelligence moves up to the Role level.

## 8. Design Principles

1. **Memory is one concept** — soul, goals, relationships, knowledge, experience are all memory. Separation is for system access needs, not conceptual taxonomy.
2. **Natural language over schemas** — relationship descriptions, success criteria, operator notes. The LLM is the consumer.
3. **Filesystem metaphor** — browse + search, not just search. Agent can navigate its own mind.
4. **S1/S2 Kahneman model** — fast intuition handles routine, slow deliberation handles complexity. Confidence-based escalation, not classification.
5. **Observable everything** — retrieval traces, execution traces. If you can't see why, you can't trust or debug.
6. **Framework-agnostic goals** — GoalNode tree supports OKR, SMART, V2MOM, or custom. Framework is labeling, not structure.
7. **Operators = procedural memory** — SystemOperator for universal abilities, domain operators for job skills, self-created operators for evolved capabilities.
