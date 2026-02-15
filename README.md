# OpenVibe

> Cognition is becoming infrastructure.

## V3: Dogfood First

**Core Thesis:** Organizations will be restructured around human+agent teams. We're proving this by transforming Vibe (the company) first, then building the platform others need.

**Current Focus:** Internal dogfooding via [Vibe AI Adoption Project](v3/vibe-ai-adoption/)

---

## The Insight

**What most people believe:**
> "AI is a tool that makes humans more productive"

**What we believe:**
> **Cognition is becoming infrastructure.**
>
> For the first time in history, thinking itself is shifting from a biological process (human brains) to deployable, scalable infrastructure (agents, models, orchestration).

This is not a tool upgrade. This is an ontological shift.

---

## Project Structure

```
openvibe/
├── v3/                      # Current work
│   ├── docs/                # V3 thesis, strategy, design
│   └── vibe-ai-adoption/    # Internal dogfooding project
│       ├── agents/          # CrewAI agent definitions
│       ├── workflows/       # LangGraph workflows
│       ├── infra/           # Temporal + LangSmith
│       └── PROGRESS.md      # Current sprint status
│
├── v2/                      # Archived (2026-02-10)
│   └── docs/                # Product strategy, design docs
│       ├── THESIS.md        # "AI as participant in work"
│       ├── STRATEGY.md      # GTM, pricing, build sequence
│       └── design/          # Agent model, interface, memory
│
└── v1/                      # Archived (2026-02-08)
    ├── docs/                # Research, BDD specs
    └── implementation/      # Nx monorepo, Supabase, Next.js
```

---

## Current Project: Vibe AI Adoption

**Goal:** Replace GTM execution layer with AI agents, achieve 10-25x efficiency gain.

**Stack:**
- **Temporal** (scheduling)
- **LangGraph** (workflow execution)
- **CrewAI** (agent roles & collaboration)

**Timeline:**
| Phase | Weeks | Focus |
|-------|-------|-------|
| 0 | 1-2 | Infrastructure setup |
| 1 | 3-4 | Lead Qualification Agent |
| 2 | 5-8 | Marketing Agents (7) |
| 3 | 9-12 | Sales Agents (6) |
| 4 | 13-16 | CS Agents (6) |

**Project Details:** [v3/vibe-ai-adoption/](v3/vibe-ai-adoption/)

---

## Key Documents

### V3 (Current)
| Document | Content |
|----------|---------|
| [v3/docs/THESIS.md](v3/docs/THESIS.md) | Core insight: Cognition as infrastructure |
| [v3/docs/INITIAL-INTENT.md](v3/docs/INITIAL-INTENT.md) | Strategic logic, dogfood-first approach |
| [v3/vibe-ai-adoption/PROGRESS.md](v3/vibe-ai-adoption/PROGRESS.md) | Current sprint status |
| [v3/docs/VIBE-AI-ADOPTION-EXECUTION-PLAN.md](v3/docs/VIBE-AI-ADOPTION-EXECUTION-PLAN.md) | Full execution plan |
| [v3/docs/VIBE-COGNITION-INFRA-ROADMAP.md](v3/docs/VIBE-COGNITION-INFRA-ROADMAP.md) | Infrastructure roadmap |

### V2 (Archived)
| Document | Content |
|----------|---------|
| [v2/docs/THESIS.md](v2/docs/THESIS.md) | "AI as participant in work" |
| [v2/docs/STRATEGY.md](v2/docs/STRATEGY.md) | Market, GTM, pricing strategy |
| [v2/docs/DESIGN-SYNTHESIS.md](v2/docs/DESIGN-SYNTHESIS.md) | Design decisions, MVP roadmap |

### V1 (Archived)
| Document | Content |
|----------|---------|
| [v1/docs/THESIS.md](v1/docs/THESIS.md) | "AI Deep Dive for team collaboration" |
| [v1/implementation/](v1/implementation/) | Full codebase (Nx + Supabase + Next.js) |

---

## Evolution Timeline

```
2026-02-06  V1 Research      → "Deep Dive/Publish" thread model
2026-02-08  V1 Sprint 0-1    → Implementation complete
2026-02-09  V2 Pivot         → "AI as participant" reframe
2026-02-10  V2 Strategy      → Product strategy complete
2026-02-11  V3 Pivot         → Dogfood-first approach
2026-02-14  V3 Project       → Vibe AI Adoption kickoff
```

**Why the pivots:**
- V1 → V2: Too derivative (Slack replacement), too narrow (deep dive is a feature)
- V2 → V3: Too early for product-first. Dogfood provides validation + learning + proof point

---

## Session Resume Protocol

1. Read [PROGRESS.md](PROGRESS.md) — Current state
2. Read [v3/docs/THESIS.md](v3/docs/THESIS.md) — Core insight
3. Read [v3/vibe-ai-adoption/PROGRESS.md](v3/vibe-ai-adoption/PROGRESS.md) — Sprint status
4. Important milestones → Pause for user confirmation

---

## Philosophy

- **Dogfood before product** — Prove it works internally first
- **Cognition as infrastructure** — Not a tool, an ontological shift
- **Validate through doing** — Build organizational muscle before selling to others
- **Learn what matters** — Real usage reveals what's needed vs nice-to-have

---

*Last updated: 2026-02-15*
