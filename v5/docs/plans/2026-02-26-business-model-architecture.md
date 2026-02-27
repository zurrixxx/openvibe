---
name: business-model-architecture
status: draft
audience: internal team
created: 2026-02-26T22:34:37Z
updated: 2026-02-26T22:45:00Z
---

# Vibe Business Model Architecture

> Internal alignment doc. How the business is structured, what we sell, to whom, and how the pieces fit together.

---

## 1. The Real Picture

We are NOT a hardware company that also does software. We are NOT a software company that also sells hardware.

**Workspace is the brain. Hardware is the body.**

```
Vibe Workspace (大脑 — agent platform)
         │
    ┌────┼────┬─────────┐
    │    │    │         │
   Bot  Dot  Board   Web/Cloud
   (room AI) (meeting AI) (canvas AI) (no hardware)
```

- Vibe Bot = an AI agent with physical presence in the room
- Vibe Dot = an AI agent in your meetings
- Vibe Board = an AI agent with a canvas
- Web = the same agents, no hardware required

Without Workspace, Bot is a microphone, Dot is a meeting tool, Board is a whiteboard. The hardware's true power comes from the agents running on it.

**Today:** The only agent capability shipped is transcription (the simplest agent). Customers buy hardware; transcription is a feature.

**Tomorrow:** Agents get smarter — summarize, follow up, recommend, execute. Hardware becomes more valuable because the brain gets better. Software updates, not hardware upgrades.

**Analogy:** Tesla model. Car ships first (hardware revenue), Autopilot unlocks over time (software value). Hardware acquires customers, software retains and monetizes.

---

## 2. Company Structure

**Vibe Systems** (vibesystems.com) is the parent entity.

```
Vibe Systems (vibesystems.com — investors)
│
├── Hardware Business (vibe.us)
│   Revenue: device sales
│   Buyer: office managers, IT, educators
│   Products: Board S1, S1 Pro, Bot, Dot
│
└── Software Business (vibe.dev)
    Revenue: subscriptions (future)
    Buyer: ops teams, developers, technical buyers
    Products: Vibe Workspace, open source engine
```

Two legs that reinforce each other. Hardware is distribution, software is value. Both can succeed independently, but together they create a moat no pure-software competitor can match: **AI agents with physical presence.**

---

## 3. Product Line

### Hardware Products (vibe.us)

| Product | What It Is | Workspace Connection |
|---------|-----------|---------------------|
| Vibe Board S1 | Interactive whiteboard (best seller) | Canvas for agent visual output |
| Vibe Board S1 Pro | Premium whiteboard | Same, higher-end |
| Vibe Bot | AI room device | Agent with eyes/ears in the room |
| Vibe Dot | AI meeting device | Agent in every meeting |

### Software on Hardware

| Software | What It Is | Status |
|----------|-----------|--------|
| Vibe Canvas | Whiteboard collaboration app | Active, ships with Board |
| Vibe AI | Transcription + meeting intelligence | Active, bundled free |

**Vibe Plus** — discontinued. Do not reference.

**Vibe AI** is a *feature*, not a product. It makes hardware more valuable. It can be free. Today it does transcription. Over time, it does more — but it's always positioned as "your device got smarter," not as a separate purchase.

### Software Product (vibe.dev)

| Product | What It Is | Status |
|---------|-----------|--------|
| Vibe Workspace | Agentic AI platform — agents, memory, actions | Building |
| Open Source Engine | SDK, runtime, platform, templates | Building |

**Vibe Workspace** is the *independent product*. It must work for someone who has never bought a Vibe Board. But it's also the brain inside every Vibe hardware device.

### The Value Prop Gap

```
What hardware customers buy today:     What Workspace actually is:
──────────────────────────────         ──────────────────────────
Transcription (clear, immediate)       Agentic AI (agents + memory + actions)
100% of hardware buyers understand     ~30% of hardware buyers would care
Feature-level value                    Platform-level value
```

~30% overlap between hardware AI users and potential Workspace buyers. This means hardware upsell is ONE acquisition channel, not THE strategy.

---

## 4. The Strategic Uncertainty: Human-Agent Collaboration UX

### What we know we don't know

Workspace's vision is "Vibe your org" — AI agents as participants in your organization. But three questions are unresolved:

**Q1: Experience — what does human + agent collaboration actually look like?**
- This is a product/UX problem, not a strategy problem
- Nobody in the industry has solved this well yet
- Current products are all Level 1-2 (trigger → summarize)
- Level 3-4 (analyze → recommend → human approves → agent executes) has no established UX pattern

**Q2: Competitive positioning — why not Slack + Notion?**
- Slack = communication layer between humans (adding AI as feature)
- Notion = knowledge organization layer (adding AI agents as feature)
- Workspace = agent execution + human supervision layer (this is a NEW layer)
- Slack and Notion add AI to their existing product forms. Their AI lives inside messages and documents. They won't become an "agent OS" because that conflicts with their core product.

**Q3: Endgame — when UI becomes less important, what's left?**
- If agents become fully autonomous, the "workspace" concept may not matter
- This is an industry-level question nobody can answer today
- Attempting to answer a Deployment-phase question during the Frenzy → Turning Point transition is, by definition, premature

### Current UX Hypothesis

**The forum model.** Neither chat (Slack/Discord) nor code review (GitHub) is right.

Reasoning:
- Human information bandwidth is limited — agents produce far more output than humans can process
- Chat is too linear, real-time, ephemeral — bad for reviewing agent work
- GitHub is too heavyweight, designed for code review, not operational decisions
- Forum structure = organized by topic, asynchronous, persistent, progressive disclosure
- Matches OpenVibe's existing design: progressive disclosure (headline → summary → detail), SOUL escalation rules, approval chains

Current dogfooding pushes toward GitHub (issues, PRs), which is directionally right (structured, async) but not the answer (too code-centric). The real UX is probably somewhere between forum and GitHub — structured enough for agent output review, lightweight enough for daily use.

**This hypothesis needs validation through Bet 1 dogfooding, not further theorizing.**

### Does the UX Even Matter?

This is the deepest strategic question.

```
Possibility A: UX is the product
├── Whoever nails human-agent collaboration UX wins
├── Agent capability is commodity, UX is differentiation
├── Like iPhone — won on experience, not chips
│
Possibility B: UX doesn't matter
├── Agents get autonomous, UI becomes notification layer
├── Value is in agent capabilities + domain knowledge
├── Like Linux — won on servers, nobody cares about its UI
```

**Resolution:** Even if the endgame is B (UX doesn't matter), the path there requires A. Nobody trusts a black-box agent with their $50K budget. Trust is built through transparency. Transparency requires UX.

```
Now ──────────────────────────── Future
Agents are limited              Agents are autonomous
Humans must deeply participate  Humans only review results
UX is critical                  UX fades
     │                              │
     └── Window: trust-building ────┘
              UX earns adoption
```

The forum UX hypothesis doesn't need to be the endgame. It needs to be **good enough for Bet 1-3** — earn trust, prove value, build adoption. Market will tell us how much UX matters by Bet 4-5.

---

## 5. Brand & Domain Architecture

### Primary Domains (independently operated)

| Domain | Role | Audience |
|--------|------|----------|
| **vibesystems.com** | Corporate entity, IR, press | Investors, press |
| **vibe.us** | Hardware store + Vibe AI | Hardware buyers |
| **vibe.dev** | Workspace product + open source + developers | Developers, ops teams |

### Supporting Domains

| Domain | Role | Status |
|--------|------|--------|
| vibe.store | → vibe.us/store/ | Active redirect |
| vibe.partners | Reseller / channel partner portal | Activate when needed |
| vibe.how | Documentation / tutorials | Activate when needed |
| vibe.run | Product dashboard / app entry | Activate when needed |
| vibe.pub | Content / building-in-public blog | Activate when needed |
| vibe.tm | Brand protection | Redirect → vibe.us |
| vibe3.io | TBD | Hold or drop |

**Rule: maximum 3 independently operated sites.** Everything else redirects.

### vibe.us Header

```
Devices | Vibe AI | Solutions | Partners | Pricing | Shop
```

- Devices: Board S1, S1 Pro, Bot, Dot
- Vibe AI: transcription, meeting intelligence (hardware feature)
- Footer: "Developers → vibe.dev" | "Investors → vibesystems.com"

### vibe.dev Header (when activated)

```
Product | Open Source | Docs | Templates | Community | GitHub
```

---

## 6. Revenue Model

| Source | Pricing | Timeline |
|-------|---------|----------|
| Device sales (Board, Bot, Dot) | One-time purchase | Now |
| Vibe AI (transcription) | Free, bundled | Now |
| Vibe Workspace | Subscription (model TBD) | Bet 3+ |
| Enterprise self-host + support | Contract | Bet 4+ |

Hardware acquires customers. Software retains and monetizes (over time).

---

## 7. GTM by Leg

### Hardware: existing channels
Board sales, demo requests, reseller network. Vibe AI is a hardware selling point.

### Software: phased activation

| Phase | Channel | Action |
|-------|---------|--------|
| Bet 1-2 | Internal dogfood | Prove Workspace works on ourselves |
| Bet 3 | Open source launch | GitHub → HN → developer adoption |
| Bet 3 | Hardware cross-sell | ~30% of hardware AI users → Workspace |
| Bet 4 | Content + community | Building-in-public, case studies |
| Bet 5 | Hosted platform | vibe.dev self-serve sign-up |

### Cross-sell (the 30%)

```
Board buyer → uses Vibe AI → "Want more?" → vibe.dev
```

Bonus channel, not primary acquisition.

---

## 8. Naming Cleanup

| Old Name | Action | New Role |
|----------|--------|----------|
| Vibe AI | Keep | Hardware AI feature (transcription) |
| Vibe AI Workspace | Rename → **Vibe Workspace** | Independent software product |
| Vibe Canvas | Keep | Board collaboration software |
| Vibe Plus | Kill | Discontinued |
| OpenVibe | Rename → **Vibe** (on vibe.dev) | Open source project |

**Stop conflating Vibe AI and Vibe Workspace.** Different products, different buyers, different value propositions.

---

## 9. Bet Sequence Mapping

| Bet | Hardware Leg | Software Leg | Key Question Answered |
|-----|-------------|-------------|----------------------|
| 1 (now) | Business as usual | Dogfood daily report 30 days | Does agent output help us? |
| 2 | Business as usual | 3-5 workflows live | Can agents be trusted for recurring ops? |
| 3 | Explore Board + Workspace bundle | Open source launch on vibe.dev | Do others want this? |
| 4 | "The AI workspace you can touch" | Workspace subscription | Will someone pay? |
| 5 | Hardware + software flywheel | Developer ecosystem, templates | Is this a platform? |

### Agent capability rollout on hardware

```
Today:  Bot/Dot/Board → transcription (agent #1)
Bet 1:  Bot/Dot/Board → meeting summary + action items (agent #2)
Bet 2:  Bot/Dot/Board → cross-meeting memory, auto follow-up (agent #3-5)
Bet 3+: Bot/Dot/Board → full agentic workspace (N agents)
```

Each step: hardware stays the same, software gets smarter, customer perceives "my device is learning."

---

## 10. One-Liner Per Audience

| Audience | Message |
|----------|---------|
| Hardware buyer | "The AI-powered whiteboard for modern teams" |
| Workspace buyer | "AI agents that run your business operations" |
| Developer | "Build autonomous agents on your own infrastructure" |
| Investor | "Hardware is the body, software is the brain. Hardware acquires customers, software retains and monetizes." |

---

## 11. Open Questions

### Product
- Vibe Workspace pricing: per-seat, per-agent-hour, or usage-based?
- Human-agent collaboration UX: forum hypothesis needs Bet 1 validation
- Vibe Dot positioning — meeting-first hardware, or standalone AI device?

### Strategy
- When to formally announce Workspace as a separate product?
- K-12 Education vertical (Bet 3 Path C) — Hardware leg, Software leg, or both?
- How much to invest in UX layer vs agent engine? (Answer: wait for Bet 1-2 signal)

### Operations
- vibesystems.com content and launch timing
- vibe.dev activation timing (Bet 3)
- vibe.partners program design

---

## 12. What NOT To Do

- Don't conflate Vibe AI (hardware feature) with Vibe Workspace (software product)
- Don't position hardware as "just a distribution channel" — it's a structural advantage (physical presence)
- Don't try to answer the UX endgame question now — the industry doesn't have the answer
- Don't operate more than 3 websites simultaneously
- Don't launch vibe.dev before Bet 2 is validated
- Don't reference Vibe Plus in any new materials

---

*This is a living document. Update as bets resolve and strategy evolves.*
*Based on brainstorming session 2026-02-26.*
