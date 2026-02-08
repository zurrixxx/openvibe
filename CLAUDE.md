# OpenVibe

> AI Deep Dive — team conversation platform with AI cognitive amplification

## Quick Start

```
Read docs/design/PRODUCT-CORE-REFRAME.md for product framing.
Read docs/CLAUDE-CODE-INSTRUCTIONS.md for full workflow.
Read docs/INTENT.md for current goals and sprint plan.
```

## Current Focus

**Phase 2**: Implementation (8 weeks, 4 sprints)

Sprint 1-2: Foundation + Thread/Messaging
Sprint 3: Deep Dive + Publish (core differentiator)
Sprint 4: Agent Integration (@Vibe, @Coder)

## Key Docs

| Document | Content |
|----------|---------|
| `docs/design/PRODUCT-CORE-REFRAME.md` | **Why "fork" = "deep dive"** — read first |
| `docs/INTENT.md` | Current goals (must read at every session start) |
| `docs/CLAUDE-CODE-INSTRUCTIONS.md` | Full workflow guide |
| `docs/research/phase-1.5/MVP-DESIGN-SYNTHESIS.md` | MVP blueprint (uses "fork" language — read reframe first) |
| `docs/design/resolution-prompt.md` | AI summary prompt validated at 4.45/5 |

## Terminology

| Codebase | User-Facing | Notes |
|----------|-------------|-------|
| `forks` table | "Deep Dive" | DB schema keeps fork naming |
| `fork.status = 'resolved'` | "Published" | |
| `fork.status = 'abandoned'` | "Discarded" | |
| `ForkSidebar` | "Active Dives" | Component name refactors later |

## Constraints

- Only submit complete implementations (no partial work)
- Do not leave TODOs
- New features must have tests
- Two teammates should not edit the same file simultaneously

## Design Principles

1. **AI as Thinking Partner** - AI amplifies human cognition during deep dives
2. **Progressive Disclosure** - Headline / summary / full for dive results
3. **Memory First** - Accumulated deep dive results = team knowledge base
4. **Configuration over Code** - Configuration-driven agents and workspaces
