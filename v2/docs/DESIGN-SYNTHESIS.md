# OpenVibe V2 Design Synthesis

> Created: 2026-02-09
> Status: Draft
> Starts from: `THESIS.md` (read that first)

---

## How to Read V2 Docs

```
THESIS.md                    <- Mother thesis: start here
  |
DESIGN-SYNTHESIS.md          <- THIS FILE: thesis -> design decisions
  |
STRATEGY.md                  <- Market, competitive, GTM, pricing, build sequence, KPIs
  |
  +-- design/
  |     AGENT-IN-CONVERSATION.md   <- Layer 1: Interface + Space
  |     PERSISTENT-CONTEXT.md      <- Layer 2: Space (memory & knowledge)
  |     FEEDBACK-LOOP.md           <- Layer 3: Interface (judgment -> behavior)
  |     [TODO] TRUST-SYSTEM.md     <- Protocol (L1-L4 mechanics)
  |     [TODO] ORCHESTRATION.md    <- Protocol (Proposal -> Mission -> Steps)
  |     [TODO] NOTIFICATION.md     <- Interface (attention management)
  |
  +-- reference/
        V1-INSIGHT-AUDIT.md        <- What survived from V1
        AGENT-ORCHESTRATION-REFERENCE.md  <- External references (Voxyz, KSimback, Yangyi)
        V2-VISION.md               <- Historical: first V2 framing (superseded by THESIS.md)
```

---

## From Thesis to Design

The thesis says: **Human+Agent collaboration needs a new medium.** That medium needs three layers:

| Layer | Serves | V2 Design Docs |
|-------|--------|---------------|
| **Protocol** | Agents | TRUST-SYSTEM (TODO), ORCHESTRATION (TODO) |
| **Interface** | Humans | AGENT-IN-CONVERSATION, FEEDBACK-LOOP, NOTIFICATION (TODO) |
| **Space** | Both | PERSISTENT-CONTEXT |

The three core properties from the thesis map to design:

| Property | Design Implication |
|----------|-------------------|
| **Agent is in the conversation** | Layer 1: @mention invocation, messages as universal interface, progressive disclosure |
| **Workspace gets smarter over time** | Layer 2: episodic memory, knowledge accumulation, the flywheel |
| **Output is worth reading** | Layer 3: feedback shapes behavior, quality compounds |

---

## What V2 Keeps From V1

V1's IM foundation is the **shared space** substrate. V2 builds on it.

| V1 Asset | V2 Role |
|----------|---------|
| Channels + messaging | Shared context space |
| Thread model | Context boundary for human+agent work |
| Deep dive concept | Multi-turn thinking sessions |
| Resolution prompt (4.45/5) | Template for structured agent output |
| Progressive disclosure (3-layer) | Standard for all agent messages |
| Supabase + Next.js + tRPC | Tech stack unchanged |
| Forum mode (~500ms OK) | Agents are inherently async |

Full audit: `reference/V1-INSIGHT-AUDIT.md` (8 must-carry, 7 blind spots, 10 reusable assets).

---

## Layer 1: Agent in Conversation

> Full doc: `design/AGENT-IN-CONVERSATION.md`

**Key decisions:**

1. **Quiet by default.** No auto-triggering. @mention, proactive (L3+), or system-triggered only.
2. **Messages = universal interface.** Every agent action = a message. No hidden dashboards.
3. **Progressive disclosure mandatory.** >1000 chars = headline + bullets + expandable.
4. **Long tasks = Voxyz pattern.** >30s gets plan + live progress. Cancel/redirect mid-task.
5. **Agents don't talk to each other in channels.** Multi-agent = orchestration layer, consolidated output.
6. **Three invocation modes:** Reactive (@mention, L1+), Proactive (SOUL triggers, L3+), System (events, L2+).

---

## Layer 2: Persistent Context

> Full doc: `design/PERSISTENT-CONTEXT.md`

**Key decisions:**

1. **MVP = working memory + episodic memory.** Knowledge base deferred to Sprint 5+.
2. **Structure at decision points, not every message.** Publishing = creating structure.
3. **Context budget by task type:** 8K (quick) / 15K (thread) / 30K (deep dive).
4. **Priority stack:** SOUL > Task > Feedback > Knowledge > Channel > Dives > Episodes.
5. **No cross-channel context in MVP.** Knowledge base enables it later.
6. **Knowledge pipeline:** Conversation -> Dive -> Publish -> Pin to Knowledge.
7. **The flywheel:** Each cycle, the workspace gets smarter. This is the data moat.

---

## Layer 3: Feedback Loop

> Full doc: `design/FEEDBACK-LOOP.md`

**Key decisions:**

1. **3 seconds or it won't happen.** Thumbs = 1s. Tag = 3s. Correction = 15s.
2. **Three persistence levels:** Immediate (thread) -> Episodic (remembered) -> Structural (SOUL).
3. **Human decides blast radius.** No auto-promotion. "Apply always" = explicit choice.
4. **Behavioral signals -> admin dashboard, not agent.** Misinterpretation risk too high.
5. **Silence is ambiguous.** Track engagement, don't interpret.
6. **Agents don't ask "was this useful?"** One exception: after high-effort tasks.
7. **Conflict = always human.** Admin decides, system surfaces.
8. **Visible improvement:** Acceptance rate + corrections trend chart.

---

## V1 Blind Spots to Address

| Blind Spot | When |
|-----------|------|
| Output quality framework | Sprint 3 |
| Context overflow strategy | Sprint 4 |
| Notification model | Sprint 3 |
| Review convergence | Sprint 5 |
| Searchable agent history | Sprint 6 |
| Agent-to-agent comms | Sprint 5 |
| Moat durability analysis | Pre-launch |

---

## Day 1 MVP (Dogfood)

Aha moment: **"I didn't leave this space to use AI, and it remembered what I said last time."**

### Must Have

| # | Feature | Sprint |
|---|---------|--------|
| 1 | @mention agent invocation | 2 |
| 2 | Progressive disclosure on agent output | 2 |
| 3 | Thread-based multi-turn with agent | 2 |
| 4 | SOUL-based agent identity | 2 |
| 5 | Working memory (SOUL + thread) | 2 |
| 6 | Thumbs up/down on agent messages | 3 |
| 7 | Episodic memory (feedback persists) | 3-4 |
| 8 | Deep dive with agent | 3 |
| 9 | Publish flow (dive -> thread) | 3 |
| 10 | Long-running task with progress | 4 |

### Later

| # | Feature | Sprint |
|---|---------|--------|
| 11-15 | Proactive agents, inline correction, agent profile, admin SOUL editor, trust levels | 4-5 |
| 16-20 | Knowledge base, semantic search, multi-agent orchestration, performance review | 5-6 |

---

## Open Questions

### Before Sprint 2

1. **Agent roster for dogfood.** Start with 1 pre-configured @Vibe, or ship "hire agent" flow?
2. **Visual design direction.** Agent message styling — need mockup/direction.

### Before Sprint 3

3. **Deep dive initiation.** L3+ agents self-initiate, or always human?
4. **Notification rules.** Proactive messages: silent or push?

### Before Sprint 5

5. **Agent coordination model.** Private thread vs orchestration-only?
6. **Knowledge entry UI.** Sidebar vs inline vs admin-only?

---

## The Bet

1. Agent workforce is inevitable
2. The workspace matters
3. Context compounds
4. Feedback is the moat
5. Slack has debt

Kill signals: `reference/V1-INSIGHT-AUDIT.md` Section 1.6.
