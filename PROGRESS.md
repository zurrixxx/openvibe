# OpenVibe Progress

> Read this first at session start, then follow Session Resume Protocol in CLAUDE.md.

---

## Current State

**Version:** V5 — Platform Prototype
**Phase:** D2C Phase 1 complete (D2C Growth role live)

| Package | Path | Version | Tests |
|---------|------|---------|-------|
| openvibe-sdk | `v5/openvibe-sdk/` | v1.0.0 | 279 |
| openvibe-runtime | `v5/openvibe-runtime/` | v1.0.0 | 28 |
| openvibe-platform | `v5/openvibe-platform/` | v1.0.0 | 60 |
| openvibe-cli | `v5/openvibe-cli/` | v1.0.0 | 15 |
| vibe-inc | `v5/vibe-inc/` | v0.1.0 | 51 |

**Total: 433 tests passing, 2 skipped (real API)**

## What's Built

### Infrastructure (Phases 0-2)

**SDK v1.0.0:**
- `TenantContext`, `TemplateConfig`, `RoleInstance` models
- `TemplateRegistry` — register + instantiate role templates
- System roles: `Coordinator`, `Archivist`, `Auditor`
- 13 role templates as YAML (GTM × 4, Product Dev × 3, Astrocrest × 6)

**Platform v1.0.0:**
- `TenantStore` + `tenants.yaml` (vibe-inc, astrocrest)
- `/tenants` routes: list, get
- Tenant-scoped routes with isolation: workspaces, roles, approvals, deliverables
- Per-tenant service instances in `app.state`

**CLI v1.0.0:**
- `--tenant` / `-t` flag (default: vibe-inc)

### D2C Phase 1: D2C Growth (complete)

**D2CGrowth role** — first fully wired role on V5 SDK:
- Soul with Net New CAC principles + escalation rules
- 2 operators, 6 agent_node methods, 6 LangGraph workflows

**AdOps operator:**
- `campaign_create` — Meta Ads campaign/adset/ad creation (PAUSED for review)
- `daily_optimize` — bid adjustment ≤20% autonomous, CPA >2x auto-pause, budget >$500 escalate
- `weekly_report` — Net New CAC vs Known CAC by product, progressive disclosure format

**CROps operator:**
- `experiment_analyze` — GA4 variant comparison, statistical significance checks
- `funnel_diagnose` — full funnel drop-off analysis, traffic quality by source
- `page_optimize` — Shopify page read/update with human approval gate

**API tools:**
- `meta_ads` — read (campaign/adset/ad), create (campaign+adset+ad), update (status/budget/bid)
- `ga4` — read with metrics/dimensions/filters, funnel event support
- `shopify` — page read + update
- `shared_memory` — YAML read/write helpers

**Shared memory YAML:**
- Messaging frameworks: Bot ("The room that remembers"), Dot ("Your brain is for thinking"), Board ("Thoughts deserve to be seen")
- ICP definitions: Bot (SMB managers), Dot (knowledge workers), Board (K-12 admins)
- CAC benchmarks: Bot $400, Dot $300, Board N/A

**Applications scaffolded:**
- `v5/vibe-inc/` — src layout, hatchling build, full test suite
- `v5/astrocrest/` — soul.yaml + roles.yaml + scoring.yaml (6 roles, not yet implemented)

## Key Docs

- `v5/docs/THESIS.md` — two-customer cognition OS thesis
- `v5/docs/DESIGN.md` — multi-tenant Role SDK architecture
- `v5/docs/ROADMAP.md` — phased execution plan
- `v5/docs/strategy/ASTROCREST.md` — Astrocrest principles
- `v5/docs/plans/2026-02-18-v5-implementation.md` — V5 platform implementation (complete)
- `v5/docs/plans/2026-02-19-d2c-marketing-adoption.md` — D2C marketing design (3-role architecture)
- `v5/docs/plans/2026-02-19-d2c-phase1-implementation.md` — D2C Phase 1 plan (17 tasks, complete)

## Not Yet Done

- **No real API calls yet** — tools implemented with mock tests only, no live credentials tested
- **D2C Content + D2C Strategy** — D2C design has 3 roles, only D2C Growth built
- **Phase 3 gate not passed** — needs 3 Vibe Inc roles live + 1 end-to-end workflow with real APIs
- **Known debt** (documented in DESIGN.md §6-7):
  - Model duality: V3 RoleTemplate/RoleSpec coexists with V5 TemplateConfig/RoleInstance
  - YAML templates not connected to TemplateRegistry
  - System roles not injected into workspaces

## Rules

- Important milestone complete → pause for user confirmation
- No external calls without confirmation
- UI direction unclear → pause for user sketch

---

*Updated: 2026-02-19 — D2C Phase 1 complete, D2C Growth role live with 51 tests*
