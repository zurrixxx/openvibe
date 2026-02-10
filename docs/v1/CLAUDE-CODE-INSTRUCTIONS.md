# OpenVibe - Claude Code Instructions

> Reference in Claude Code: `Read docs/CLAUDE-CODE-INSTRUCTIONS.md`

---

## Project Overview

**OpenVibe** = AI Deep Dive team collaboration platform

Core differentiator: Any team member can **deep dive with AI** on any conversation point — AI amplifies their thinking, then the compressed result flows back to the team thread with progressive disclosure.

```
┌─────────────────────────────────────────────────────┐
│            Web UI (Next.js 14)                       │
│         Discord-like + Active Dives Sidebar          │
└─────────────────────┬───────────────────────────────┘
                      │ tRPC + Supabase Realtime
┌─────────────────────▼───────────────────────────────┐
│              Backend (~30 tRPC procedures)           │
└─────────────────────┬───────────────────────────────┘
                      │
       ┌──────────────┼──────────────┐
       ▼              ▼              ▼
   [@Vibe]        [@Coder]       [Humans]
   (deep dive      (code dive
    partner)        partner)
       │              │
       └──────┬───────┘
              ▼
        [Supabase]
   (Postgres + Realtime)
```

> **Important:** Prior docs use "fork/resolve" terminology. Read [`PRODUCT-CORE-REFRAME.md`](design/PRODUCT-CORE-REFRAME.md) to understand why the product is actually about "AI Deep Dive." In the codebase, `fork` = deep dive (technical term kept in DB schema).

---

## Required Reading

### Product Core (Read First)

| Document | Content | Priority |
|----------|---------|----------|
| [`docs/design/PRODUCT-CORE-REFRAME.md`](design/PRODUCT-CORE-REFRAME.md) | Why "fork" became "deep dive" | **Must read** |
| [`docs/INTENT.md`](INTENT.md) | Current goals + Sprint plan | **Every session** |

### Phase 2 Implementation (Current)

| Document | Content | Priority |
|----------|---------|----------|
| [`docs/research/phase-1.5/BDD-IMPLEMENTATION-PLAN.md`](research/phase-1.5/BDD-IMPLEMENTATION-PLAN.md) | Gherkin specs + 8-week plan | **Must read** |
| [`docs/research/phase-1.5/BACKEND-MINIMUM-SCOPE.md`](research/phase-1.5/BACKEND-MINIMUM-SCOPE.md) | 12 tables, ~30 procedures | **Must read** |
| [`docs/research/phase-1.5/FRONTEND-ARCHITECTURE.md`](research/phase-1.5/FRONTEND-ARCHITECTURE.md) | Next.js + Zustand | **Must read** |
| [`docs/research/phase-1.5/THREAD-UX-PROPOSAL.md`](research/phase-1.5/THREAD-UX-PROPOSAL.md) | Deep Dive UX (uses "fork" language) | **Must read** |

### Background Understanding

| Document | Content |
|----------|---------|
| [`docs/research/SYNTHESIS.md`](research/SYNTHESIS.md) | Phase 1 research synthesis |
| [`docs/PRODUCT-REASONING.md`](PRODUCT-REASONING.md) | Product reasoning derivation |
| [`docs/research/phase-1.5/SYSTEM-ARCHITECTURE.md`](research/phase-1.5/SYSTEM-ARCHITECTURE.md) | Complete architecture diagrams |

### Historical Reference (Superseded)

`docs/design/M1-M6` -- Initial designs, updated in Phase 1.5

---

## Current Phase: Phase 2 - Implementation (8 Weeks)

### Sprint Overview

| Week | Epic | Key Deliverables |
|------|------|------------------|
| 1-2 | Foundation | Auth, Workspace, Channel CRUD |
| 3-4 | Thread + Messaging | Realtime messages, streaming |
| 5-6 | **Deep Dive + Publish** | Core differentiator: AI thinking partner + structured dive results |
| 7-8 | Agent Integration | @Vibe (deep dive partner), @Coder |

### Critical Risk

**AI Deep Dive Quality = Load-bearing wall**

Week 5-6 is the validation point. The AI must be a good thinking partner during the dive AND generate good structured results at publish. Resolution prompt validated at 4.45/5 (see [`resolution-prompt.md`](design/resolution-prompt.md)).

---

## Tech Stack

| Layer | Tech | Notes |
|-------|------|-------|
| Frontend | Next.js 14 + shadcn/ui + Zustand | App Router |
| API | tRPC | Type-safe |
| Realtime | Supabase Realtime | postgres_changes |
| Database | PostgreSQL + pgvector | Supabase hosted |
| Agent | Claude SDK | Sonnet 4.5 |
| Infra | Fly.io + Supabase | Single machine for dogfood |

---

## Monorepo Structure (Nx)

```
apps/
  web/                 # Next.js frontend

packages/
  db/                  # Prisma/Drizzle schema
  ui/                  # Shared components
  config/              # Config types
  agent/               # Agent runtime

docs/                  # All documentation
  INTENT.md            # Current goals
  design/              # Product reframe + validation
  research/            # Phase 1 + 1.5 research
```

---

## Implementation Priorities

### Week 1-2: Foundation

```gherkin
Feature: User Signup
Feature: User Login
Feature: Workspace Creation
Feature: Channel CRUD
```

Files to create:
- `apps/web/` - Next.js app
- `packages/db/` - Schema
- Supabase setup

### Week 3-4: Thread + Messaging

```gherkin
Feature: Thread Creation
Feature: Send Message
Feature: Real-time Updates
Feature: Agent Response Streaming
```

### Week 5-6: Deep Dive + Publish (CRITICAL)

```gherkin
Feature: Deep Dive Creation       # User clicks "Deep Dive" on any message
Feature: Active Dives Sidebar     # Shows ongoing dives in thread
Feature: Focus Mode               # Switch between thread view and dive view
Feature: Publish with AI Result   # ← Critical validation: AI generates structured findings
Feature: Discard Dive             # Archive without publishing
```

Note: DB schema uses `forks` table, but user-facing UI says "Deep Dive" / "Publish" / "Discard."

### Week 7-8: Agent Integration

```gherkin
Feature: @Vibe Agent              # Deep dive thinking partner
Feature: @Coder Agent             # Code-focused dive partner
Feature: Task Progress
```

---

## Key Patterns

### Terminology Mapping (Code ↔ Product)

| Codebase | User-Facing | Notes |
|----------|-------------|-------|
| `forks` table | "Deep Dive" | DB schema keeps fork naming |
| `fork.status = 'resolved'` | "Published" | Status value unchanged |
| `fork.status = 'abandoned'` | "Discarded" | Status value unchanged |
| `ForkSidebar` component | "Active Dives" label | Component name can refactor later |
| `useForkStore` | — | Internal, keep as-is |

### State Management (Zustand)

```typescript
// Separate stores per domain
const useChannelStore = create(...)
const useThreadStore = create(...)
const useForkStore = create(...)    // "fork" in code = "deep dive" in UI
const useUIStore = create(...)
```

### Realtime Subscriptions

```typescript
supabase
  .channel(`channel:${channelId}`)
  .on('postgres_changes', {
    event: '*',
    schema: 'public',
    table: 'messages'
  }, handleMessage)
```

### Agent Invocation

```typescript
// Agent = config record, not process
const agent = await db.agentConfigs.findBySlug('vibe');
const response = await claude.complete({
  system: agent.systemPrompt,
  messages: threadHistory,
  stream: true
});
```

---

## Constraints

1. **Dogfood scope only** -- 20 users, single Fly.io machine
2. **No premature optimization** -- Scaling is a Phase 3+ concern
3. **Deep Dive first** -- This is the differentiator; everything else can be simplified
4. **Test with Gherkin** -- BDD specs are defined; test with Playwright

---

## Success Metrics

| Checkpoint | Criteria |
|------------|----------|
| Week 2 | Auth + Workspace + Channel working |
| Week 4 | Realtime messaging + streaming |
| Week 6 | **Deep Dive with AI-generated structured results** |
| Week 8 | Agents working, ready for dogfood |

---

*Updated: 2026-02-07*
*Phase: 2 - Implementation*
