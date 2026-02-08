# OpenVibe - Current Intent

> **Updated 2026-02-08:** Terminology changed from Fork/Resolve to Deep Dive/Publish per PRODUCT-CORE-REFRAME.md

> This file defines the current working objectives. Read this at the start of every session.
>
> **Start here:** [`docs/design/PRODUCT-CORE-REFRAME.md`](design/PRODUCT-CORE-REFRAME.md) — the product core is **AI Deep Dive**, not "Fork/Resolve."

---

## Roadmap

```
Phase 1: Research ──────── ✅ Complete (R1-R7 + SYNTHESIS)
Phase 1.5: Design Deep Dive ✅ Complete (Architecture, UX, BDD)
Phase 2: Implementation ─── 🔄 NOW (8 weeks)
Phase 3: Dogfood ────────── Pending
Phase 4+: ───────────────── TBD based on dogfood
```

| Phase | Input | Output | Status |
|-------|------|------|--------|
| **1. Research** | Existing design docs + external research | R1-R7 + SYNTHESIS.md | ✅ Done |
| **1.5. Design** | SYNTHESIS.md | Architecture, UX, BDD specs | ✅ Done |
| **2. Implementation** | Phase 1.5 docs | A runnable dogfood product | 🔄 Next |
| **3. Dogfood** | Runnable product | Real feedback + iteration direction | Pending |

---

## Current Goal

**Phase 2: Implementation (8 Weeks)**

Build the dogfood MVP based on Phase 1.5 designs.

### Sprint Plan

| Week | Epic | Key Deliverables |
|------|------|------------------|
| 1-2 | Foundation | Auth, Workspace, Channel CRUD |
| 3-4 | Thread + Messaging | Realtime messages, streaming |
| 5-6 | **Deep Dive + Publish** | Core differentiator: AI as thinking partner, structured dive results |
| 7-8 | Agent Integration | @Vibe (deep dive partner), @Coder |

Detailed Gherkin specs: [`docs/research/phase-1.5/BDD-IMPLEMENTATION-PLAN.md`](research/phase-1.5/BDD-IMPLEMENTATION-PLAN.md)

### Critical Risk

**AI Deep Dive Quality = Load-bearing wall**

The deep dive model depends on AI being a good thinking partner during the dive AND generating good structured results at publish. Weeks 5-6 are the validation point. Dive result prompt validated at 4.45/5 (see [`resolution-prompt.md`](design/resolution-prompt.md)).

---

## Key Documents

### Product Core (Read First)

| Doc | Purpose | Priority |
|-----|---------|----------|
| [`PRODUCT-CORE-REFRAME.md`](design/PRODUCT-CORE-REFRAME.md) | Why "fork" became "deep dive" — the real product thesis | **Must read** |
| [`slack-pain-ranking.md`](design/slack-pain-ranking.md) | Solution-agnostic pain ranking + AI solution evaluation | Reference |

### Phase 1.5 Design Docs (Implementation Reference)

| Doc | Purpose | Priority |
|-----|---------|----------|
| [`BDD-IMPLEMENTATION-PLAN.md`](research/phase-1.5/BDD-IMPLEMENTATION-PLAN.md) | Sprint plan + Gherkin specs | **Must read** |
| [`BACKEND-MINIMUM-SCOPE.md`](research/phase-1.5/BACKEND-MINIMUM-SCOPE.md) | 12 tables, ~30 tRPC procedures | **Must read** |
| [`FRONTEND-ARCHITECTURE.md`](research/phase-1.5/FRONTEND-ARCHITECTURE.md) | Next.js + Zustand structure | **Must read** |
| [`THREAD-UX-PROPOSAL.md`](research/phase-1.5/THREAD-UX-PROPOSAL.md) | Deep Dive UX design | **Must read** |
| [`AGENT-DEFINITION-MODEL.md`](research/phase-1.5/AGENT-DEFINITION-MODEL.md) | Agent config model (@Vibe is both general assistant and deep dive partner) | Week 7-8 |
| [`SYSTEM-ARCHITECTURE.md`](research/phase-1.5/SYSTEM-ARCHITECTURE.md) | Infrastructure diagrams | Reference |

### Phase 1 Research (Background Understanding)

| Doc | Purpose |
|-----|---------|
| [`SYNTHESIS.md`](research/SYNTHESIS.md) | Phase 1 comprehensive conclusions |
| [`R1-THREAD-MODEL.md`](research/R1-THREAD-MODEL.md) | Thread model derivation (fork from Git simplification) |
| [`R3-AGENT-LIFECYCLE.md`](research/R3-AGENT-LIFECYCLE.md) | Task lifecycle |
| [`R7-CONTEXT-UNIFICATION.md`](research/R7-CONTEXT-UNIFICATION.md) | Cross-runtime context (long-term) |

### Validation

| Doc | Result |
|-----|--------|
| [`resolution-prompt.md`](design/resolution-prompt.md) | AI summary prompt: **4.45/5 (89%)** across 5 real conversations |
| [`fork-necessity-analysis.md`](design/fork-necessity-analysis.md) | 1,097 threads: 55% partial resolution, topic drift = 22pt drop |
| [`adoption-wedge-analysis.md`](design/adoption-wedge-analysis.md) | Product direction decisions = best entry point |

### Original Designs (Superseded by Phase 1.5)

`docs/design/M1-M6` -- Retained as historical reference; actual implementation follows Phase 1.5.

---

## Dogfood Context

- **First user**: Vibe team (20 people)
- **Replaces**: Slack
- **Latency requirement**: ~500ms is sufficient (forum mode)
- **Cost budget**: ~$640-940/month (infra) + ~$600-900/month (LLM)

---

## Tech Stack

| Layer | Tech |
|-------|------|
| Frontend | Next.js 14 + shadcn/ui + Zustand |
| API | tRPC |
| Realtime | Supabase Realtime |
| Database | PostgreSQL (Supabase) + pgvector |
| Agent | Claude SDK + MCP |
| Infra | Fly.io + Supabase |

---

## Success Criteria

### Week 2 Checkpoint
- [ ] Auth working (signup/login/OAuth)
- [ ] Workspace + Channel CRUD
- [ ] Basic UI shell (Discord-like layout)

### Week 4 Checkpoint
- [ ] Realtime messaging
- [ ] Thread creation and listing
- [ ] Agent response streaming

### Week 6 Checkpoint (Critical)
- [ ] Deep dive creation from any message
- [ ] **Deep dive publish with AI-generated structured result** — Core validation
- [ ] Focus mode switching between thread and Active Dives

### Week 8 Checkpoint
- [ ] @Vibe agent working (deep dive thinking partner)
- [ ] @Coder agent working
- [ ] Ready for internal dogfood

---

*Updated: 2026-02-07*
*Status: Phase 2 - Implementation*
