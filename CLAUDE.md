# OpenVibe

> Agent Organization OS — 让 Agent 融入公司组织的操作系统

## 🎯 V2 DIRECTION CONFIRMED

**Read first:** `docs/V2-VISION.md`

**核心定位:** 让 Agent 像员工一样被信任、被管理、自主工作

**护城河:** 组织层 (Trust & Governance)，不是智能层

**核心体验:**
1. Trust Level 体系 (L1-L4)
2. Agent as Employee (招聘 → 自主工作 → Review)
3. 完整 Audit Trail

---

## Quick Start

```
Read docs/V2-VISION.md for confirmed direction.
Read docs/design/AGENT-ORCHESTRATION-REFERENCE.md for technical reference (Voxyz/KSimback).
```

## Current Focus

**Phase 2**: V2 Design & Implementation

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
