# OpenVibe V2: Strategy

> Created: 2026-02-10
> Status: Active
> Prerequisites: Read `THESIS.md` first

---

## Executive Summary

OpenVibe is the AI workspace layer for Vibe's 40K interactive whiteboards + web/mobile.

**Strategy**: Build web-first AI workspace (6 months), light up existing boards via firmware update with 90-day free trial, convert at $149/month/board.

**GTM**: Partner-led distribution through professional services firms (consulting, accounting, MSPs). 120 partners → 11,500 workspaces in 18 months.

**Moat**: Distribution speed (partner network) + Institutional memory (context accumulation) + Open infrastructure (structural differentiation).

---

## Market Context

### The Transition Is Happening (Q1 2026)

5,000-15,000 organizations worldwide already operate with "few humans + many agents" in daily workflow.

| Event | Date | Impact |
|-------|------|--------|
| Anthropic Cowork | Jan 2026 | Agent-as-colleague for non-developers. Triggered $285B SaaS selloff. |
| OpenAI Frontier | Feb 2026 | Enterprise agent management. HP, Oracle, Uber signed day one. |
| CrewAI at scale | Q1 2026 | 10M+ agents/month, ~50% Fortune 500 using. |

Growth: 50K+ orgs by Q3-Q4 2026, 100K+ by Q1-Q3 2027, mainstream (500K+) by 2028.

**The bottleneck is NOT better models. It's management infrastructure** — how to onboard, configure, supervise, and improve agents as a team.

### Competitive Landscape

| Competitor | Product | Threat Level | Weakness |
|------------|---------|-------------|----------|
| **Anthropic Cowork** | Personal agent workspace | VERY HIGH | Individual-first, no team context, proprietary |
| **OpenAI Frontier** | Enterprise agent mgmt | HIGH | Platform for developers, not workspace for teams |
| **Microsoft Copilot** | Agent in Office/Teams | HIGH | Bolted-on, not agent-native. "Free" with E5 license. |
| **Slack AI** | Agent features in Slack | MEDIUM | Architecturally constrained (agents = second-class) |

**Biggest threat**: Anthropic ships team Cowork before us. Gap between "I have an AI colleague" and "my team has AI colleagues who share context" is OpenVibe's wedge. If Anthropic ships team features Q3 2026, window closes.

**Microsoft window**: 12-18 months before Copilot ships comparable meeting room AI features.

### Why OpenVibe Can Win

**Structural advantages**:
1. **Open source + multi-model** - Anthropic won't do (violates business model)
2. **Partner-led GTM** - Anthropic won't seriously do (channel conflict)
3. **40K boards in meeting rooms** - Physical presence = activation surface
4. **150-person company** - Not a 2-person startup, not enterprise bureaucracy
5. **Existing relationships** - IT already provisioned, SSO configured

**Not relying on**: Product features (will converge), UI patterns (will be copied), or AI capabilities (models improve for everyone).

---

## Strategic Decisions

### 1. Web First, Board Second

All competitive analysis reached same conclusion: board is consumption surface for value created in async work.

**The aha moment is NOT "agent in the board meeting." It's "the board room got smarter between meetings."**

Build sequence:
- Month 1-4: Web workspace (agents, feedback, memory)
- Month 5: Board MVP (channel summary, @mention, agent response cards)
- Month 6: GA (firmware push to all 40K boards)

### 2. Partner-Led Distribution

**Not direct sales. Partner-led.**

Professional services firms (consulting, accounting, MSPs) serve 20-200 clients each. Sell to one firm → reach hundreds of end customers.

**HubSpot precedent**: Targeted marketing agencies (not end customers). Each agency deployed HubSpot for 30-100 clients. Result: exponential growth through partners.

**OpenVibe model**:
- Sell to consulting firms, accounting firms, MSPs
- They deploy OpenVibe for their client engagements
- Each partner = 50-200 end customer workspaces

**Partner vertical sequencing**:
1. **Management Consulting** (Month 1-6): 10 firms, existing Vibe relationships
2. **Accounting Firms** (Month 7-12): 20 firms, highest viral coefficient (200+ clients/firm)
3. **MSPs** (Month 13-18): 40 firms, tech-forward, strong lock-in
4. **Marketing Agencies** (Month 19-24): 50 firms, HubSpot-validated playbook

**18-month projection**: 120 partners → 11,500 end customers → 34,500 boards → $61M ARR.

**Why this works**:
- 25x faster than direct sales (partner-sourced = 93% of revenue by Month 24)
- Partners become sales force (trained, certified, revenue-dependent)
- Industry-specific deployments (partner knows customer's business)

### 3. Pricing: $149/month/board

**Why $149**:
- Under $2K/year = room owner can expense without VP approval
- Covers LLM costs ($30-50/month estimated) with margin
- Anchors against Copilot ($30/user × 5 participants = $150/month)
- "Less than one person-hour of meeting follow-up saved per week"

**90-day free trial** on all 40K boards at GA. No credit card required.

**Partner pricing**: Wholesale model (not revenue share). Partners buy at $79-99, sell at $149-199. Recurring revenue = $60-120/board/month. A partner with 50 clients × 3 boards × $60 margin = **$9K/month recurring**.

### 4. Build Sequence: 7 Sprints, 24 Weeks

**Alpha** (Month 1-2): Vibe internal + 3-5 consulting firms (co-development)
**Beta** (Month 3-5): 10 partners → 50-100 client deployments
**GA** (Month 6): Firmware push to all 40K boards + partner recruitment opens

**Sprints**:
- Sprint 2 (Week 1-4): @mention, SOUL, progressive disclosure
- Sprint 3 (Week 5-8): Feedback, deep dives, publish flow
- Sprint 4 (Week 9-12): Episodic memory, long tasks, Slack bridge (read)
- Sprint 5 (Week 13-16): Board MVP, trust levels, admin panel
- Sprint 6 (Week 17-20): Proactive agents, knowledge base, meeting summary
- Sprint 7 (Week 21-24): Multi-agent, mobile web, Slack write-back, search

**Engineering allocation**: 70% core/web, 20% board, 10% connectors. Never less than 70% on core.

**Architecture**: Monolith (packages/core + apps/web + apps/board). No debate at 5-10 engineers.

---

## Moats (Time-Layered)

| Year | Moat | Why Durable |
|------|------|-------------|
| **Year 1-2** | Distribution speed + Partner network | 6-month ship vs Microsoft 12-18 months. 120 partners vs direct sales. |
| **Year 2-3** | Partner ecosystem lock-in | Partners trained, certified, revenue-dependent. Switching cost = retrain team, rebuild methodology. |
| **Year 3-5** | Institutional memory | 18 months of context = switching cost. Feedback-shaped behavior non-transferable. Knowledge bases compound. |

**The durable moat is the shared context layer** (SOUL configs, episodic memory, knowledge base, feedback history), not the UI. UI will evolve or be absorbed by 2028-2030. Context layer is the asset.

Hardware adds physical lock-in:
- Room-level institutional memory (board "knows" room's decision history)
- IT infrastructure entrenchment (security review already passed)
- Workflow gravity (can't switch web without switching board)
- Physical proof of value (CEO walks past board showing agent work → renewal safe)

---

## Critical Metrics

### Month 3 (Dogfood + Alpha)

| Metric | Target | Kill Signal |
|--------|--------|------------|
| @mentions per person per day | > 2 | < 0.5 = agents not useful |
| Agent acceptance rate | >= 60% | < 40% = output broken |
| Deep dives per week | >= 5 | 0 = feature not valued |
| Dive publish rate | >= 30% | < 20% = quality insufficient |

### Month 6 (Beta + Board)

| Metric | Target | Kill Signal |
|--------|--------|------------|
| **Acceptance rate delta (M6 - M3)** | **> 0** | **= 0 means feedback loop broken** |
| Room return rate (3+ meetings/2 weeks) | >= 50% | < 30% = not habitual |
| Board meetings using workspace | >= 3/week | 0 = board not needed |
| "Would miss it if gone" (dogfood team) | >= 60% | < 30% = product not essential |

**The single most important metric**: Acceptance rate delta. If workspace is getting smarter (rate improving M3 → M6), thesis works. If flatlined, feedback loop is broken.

### Partner Health (Ongoing)

| Metric | Target | Kill Signal |
|--------|--------|------------|
| Client deployments per partner | >= 20 within 12 months | < 5 after 12 months = wrong partners |
| Time to first client deployment | < 30 days | > 90 days = enablement insufficient |
| Partner-sourced revenue % | > 50% by Month 12 | < 30% = direct model still dominant |

---

## Key Risks

### #1: Agent output quality (existential)

Default to passive. Agents listen and prepare, but do NOT speak unless asked. Between meetings, agents draft but do NOT send. Humans approve everything in V1.

Mitigation: Streaming via progressive disclosure. Instrument `buildContextForAgent()` — log and review 10 invocations/day in first 4 weeks.

### #2: Anthropic ships team Cowork before us

6-9 month window (not 12-18). "Team collaboration" wedge disappears Q3 2026.

Mitigation: Defense must be structural (open source, partner ecosystem), not features. Accelerate GA to Month 5 if needed.

### #3: Partners don't deploy to clients

Partners sign up but don't actually deploy OpenVibe to client engagements.

Mitigation:
- Co-development in Alpha (partners design deployment methodology)
- Hands-on support for first 5 client deployments
- Partner Success KPI = client deployments, not partner sign-ups

### #4: Microsoft catches up

12-18 month window before Copilot ships comparable meeting room AI.

Mitigation: Move fast. Alpha in 8 weeks, GA in 6 months. Accumulate context depth that late entrants can't replicate.

### #5: Board SDK constraints

If SDK can't support live-updating cards, touch-to-dive, real-time rendering → blocked at Sprint 5.

Mitigation: Board SDK feasibility spike in Sprint 3 (2 engineers, 1 week). Validate before committing. Web-only is acceptable fallback.

---

## The Endgame (3-5 Year View)

| Year | What Happens | Moat |
|------|-------------|------|
| **Year 1** | AI workspace launches. 10 consulting partners → 500 end customers. Direct: 1,600-2,400 boards. | Partner network + distribution speed |
| **Year 2** | Partner network scales. 120 partners → 11,500 end customers. Partner-sourced = 93% of revenue. | Partner ecosystem lock-in + institutional memory |
| **Year 3** | Purpose-built AI board launches ($3-5K, workspace built in). Industry-specific agent packs. | Partner lock-in + vertical specialization + purpose-built hardware |
| **Year 4-5** | Workspace becomes platform. Third-party agents. Partner marketplace. Board = "AI room." | Partner ecosystem + institutional memory + platform effects |

**The endgame is not a whiteboard company that added AI. It's an AI workspace company with partner-led distribution and physical presence in every professional services firm's client engagement.**

---

## Document Index

```
THESIS.md                    ← Mother thesis (read first)
DESIGN-SYNTHESIS.md          ← Thesis → design decisions
STRATEGY.md                  ← THIS FILE: market, competitive, execution
  |
  +-- go-to-market/
  |     BRAND-ARCHITECTURE.md        (3-layer website strategy)
  |     QUICK-REFERENCE.md           (1-page GTM summary)
  |     STRATEGIC-ANALYSIS.md        (8-agent competitive analysis)
  |     NARRATIVE-OPTIONS.md         (Storytelling approaches)
  |     GITHUB-ORG-SETUP.md          (GitHub org structure)
  |
  +-- design/
        AGENT-IN-CONVERSATION.md
        PERSISTENT-CONTEXT.md
        FEEDBACK-LOOP.md
        AGENT-MODEL.md
```

---

*For execution details (sprint plans, partner program, metrics framework), see `go-to-market/` folder.*
