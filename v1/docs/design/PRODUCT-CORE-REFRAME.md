# Product Core Reframe: From Fork/Resolve to AI Deep Dive

> Status: Active | Date: 2026-02-07
> Purpose: Correct a concept drift that has been misleading all project documentation
> Authority: This document SUPERSEDES the fork/resolve framing in all prior docs

---

## 1. What Happened

### The Original Thesis (from the founder)

The product idea started from a real daily workflow:

1. Team discusses a topic in Slack
2. Someone (often the founder) needs to think deeper about a point
3. They copy the context to an AI tool, give it additional context, research, iterate
4. They get a result and paste it back to Slack
5. The AI output is too long/dense for the team to read
6. Other team members ALSO copy it to AI to digest
7. Then they respond

**The core insight:** Every topic point needs a place to **deep dive with AI**. This amplifies one person's bandwidth and judgment. But the output is too much for others to consume — so it needs compression and progressive disclosure.

The product should make this entire loop native: `human + AI deep dive → compressed structured output → team thread`.

### How It Drifted

The original PRODUCT-REASONING.md framed collaboration as "Git-like Threads" — branch for exploration, merge conclusions. This was a reasonable analogy.

R1 research then explored Git semantics literally (branch/merge/checkout/diff) and concluded they were overengineered. The simplification was: **fork** (create side-conversation) + **resolve** (AI summarizes back). Good simplification.

But "fork" carried connotations from Git and from general usage: **a divergence point where multiple people go in a different direction**. Over 19+ documents and 1,450+ references, the product narrative shifted from:

- **Original:** "One person deep dives with AI on a point, posts compressed result to team"
- **Drifted to:** "Multiple people branch into a side-discussion, AI summarizes at the end"

These are fundamentally different products:

| Dimension | Original Thesis (Deep Dive) | Drifted Thesis (Fork/Resolve) |
|-----------|---------------------------|------------------------------|
| **Primary actor** | 1 human + AI | Multiple humans in side-thread |
| **AI role** | Thinking partner during the dive | Summarizer at the end |
| **Value creation** | AI amplifies human cognition | AI saves reading time |
| **When AI is involved** | Throughout the deep dive | Only at resolution |
| **Core experience** | Private research with AI → publish findings | Group side-discussion → AI summarizes |
| **Competitive moat** | Cognitive amplification (nobody else does this) | Thread summaries (everyone is doing this) |

The THREAD-UX-PROPOSAL actually got this right in its opening: *"Fork/Resolve is not about 'branching discussions between humans.' It is about making the AI research loop a first-class part of the conversation."* But this insight didn't propagate — the rest of the docs kept treating forks as side-discussions.

### Why This Matters

If we build the drifted version, we get "Slack with AI summaries" — a crowded, undifferentiated market (see Slack AI, Notion AI, every "AI meeting notes" startup). The slack-pain-ranking analysis showed that auto-summary + drift nudge solve 80% of Slack pain with 20% of effort. Fork-as-side-discussion is priority #4.

If we build the original version, we get something genuinely new: a tool where **AI is your thinking partner inside the conversation context**, and the team benefits from your amplified output without having to consume the raw process. This is not a crowded market.

---

## 2. The Restored Core

### One Sentence

**OpenVibe is a team conversation platform where any participant can deep dive with AI on any point, and the AI-compressed output flows back to the team at the right level of detail.**

### The Flow (What the User Actually Does)

```
Thread: "We need to decide on pricing for the new SaaS tier"
    │
    ├── Alice: "I think we should look at competitor pricing"
    │
    ├── Bob: "What about the kiosk mode bundling?"
    │
    ├── Alice clicks [Deep Dive] on Bob's message
    │       │
    │       └── Deep Dive context (Alice + AI):
    │           Alice: "Help me think through kiosk mode bundling options"
    │           AI: analyzes pricing models, competitor data, margin implications
    │           Alice: "What about the enterprise tier?"
    │           AI: models 3 scenarios with ARR projections
    │           Alice: "OK I think Option B is strongest. Let me post this."
    │
    │           Alice clicks [Publish to Thread]
    │           AI generates: headline + bullets + full analysis
    │           Alice reviews, edits headline, publishes
    │
    ├── [AI Deep Dive Result - Alice]
    │   "Kiosk bundling: Option B (usage-based) projects 23% higher ARR"
    │   ▸ 3 bullets summarizing key findings
    │   ▸ [Expand full analysis]
    │
    ├── Bob: "Good analysis. The margin assumption might be off though..."
    │
    └── Bob clicks [Deep Dive] on the result
            │
            └── Bob + AI re-examine Alice's assumptions...
```

### What's Different From the Drifted Version

1. **The deep dive is primarily 1 human + AI.** Not a group side-discussion. Others can join (it's not private by default), but the mental model is "I need to think deeper about this with AI help."

2. **AI is active during the dive, not just at the end.** The AI is your research partner throughout — helping you think, analyze, model, draft. It's not waiting to summarize after humans finish talking.

3. **The output is the deep diver's conclusion, not a meeting summary.** When Alice publishes, it's *her* finding aided by AI — not a neutral summary of what multiple people said. This is closer to "posting a research brief" than "closing a side-thread."

4. **Progressive disclosure is the core UX, not a nice-to-have.** The deep dive produces 10x more content than the team needs. The headline/summary/full structure is what makes this work for the team. Without it, deep dives would flood the thread.

5. **The value scales with deep dive quality, not with thread count.** The drifted version's value proposition was "organize conversations better." The real value proposition is "amplify each person's thinking." One excellent deep dive that changes a $100K decision is worth more than summarizing 100 threads.

---

## 3. Terminology

### The "Fork" Problem

"Fork" implies:
- A divergence (two paths from one point)
- Multiple people going different directions
- Git semantics (branch, merge, conflict)
- Permanence (a fork is a split)

None of these match the actual interaction: one person + AI going deeper, then bringing a compressed result back.

### Proposed Vocabulary

| Old Term | New Term | Why |
|----------|----------|-----|
| Fork | **Deep Dive** (or just "Dive") | Captures the intent: going deeper on a point |
| Resolve | **Publish** | You're publishing your findings, not resolving a discussion |
| Abandon | **Discard** | Cleaner than "abandon" |
| Fork sidebar | **Active Dives** | Shows ongoing deep dives in the thread |
| Fork description | **Dive topic** | What you're exploring |
| Resolution summary | **Dive result** | What came out of the deep dive |

**Note on codebase:** The internal data model can keep `fork` as a technical term (it's accurate for the DB schema — a fork in the message tree). But the user-facing language and product narrative should use "deep dive" / "dive."

### Why "Deep Dive" Over Other Options

| Candidate | Problem |
|-----------|---------|
| Research | Too academic, implies desk research only |
| Explore | Too vague, could mean browsing |
| Amplify | Not a natural verb for the action ("let me amplify this point"?) |
| Branch | Same problem as fork — implies divergence |
| Sidebar | Implies a minor tangent, not depth |
| **Deep Dive** | Natural language ("let me deep dive on this"), captures depth + AI partnership, already used in business contexts |

---

## 4. What Changes

### Product Narrative

**Before:** "OpenVibe is a fork/resolve thread platform — users fork side-discussions from any message, explore with AI agents, then resolve back."

**After:** "OpenVibe is a team workspace where anyone can deep dive with AI on any conversation point. The AI amplifies your thinking, and the compressed result flows back to the team — headline first, details on demand."

### UX Implications

| Aspect | Old (Fork) | New (Deep Dive) |
|--------|-----------|-----------------|
| Entry point | "Fork this message" button | "Deep Dive" button (or keyboard shortcut) |
| Mental model | "Start a side-discussion" | "I need to think deeper about this" |
| Default participants | Fork creator + anyone who joins | Deep diver + AI (others can observe) |
| AI behavior during dive | Responds when @mentioned | Active partner — proactively helps, suggests angles, asks clarifying questions |
| AI behavior at publish | Generates summary of discussion | Generates structured findings (headline + bullets + full) |
| Compose box prompt | (same as thread) | "What do you want to explore?" or context-aware prompt |
| Result in main thread | "Fork resolved: [summary]" | "Deep Dive by Alice: [headline]" with expand |

### AI Role Shift

This is the biggest change. In the fork model, the AI was primarily a **summarizer** (the "Fork Resolver" agent). In the deep dive model, the AI is primarily a **thinking partner**:

| Phase | AI Role (Old: Fork Resolver) | AI Role (New: Deep Dive Partner) |
|-------|----------------------------|----------------------------------|
| **Start** | Auto-generates fork description | Helps frame the question: "You're exploring [X]. Want me to pull context from [Y]?" |
| **During** | Passive — responds only when @mentioned | Active — suggests angles, challenges assumptions, brings relevant data, models scenarios |
| **Pre-publish** | Generates summary of all messages | Generates structured findings from the deep dive |
| **Publish** | Posts resolution card | Posts deep dive result card with progressive disclosure |

### Agent Architecture Impact

| Agent | Old Role | New Role |
|-------|---------|----------|
| @Vibe | General assistant in threads | Deep dive partner — the AI you think with |
| @Coder | Code assistant | Deep dive partner for code/technical topics |
| Fork Resolver | Summarize fork at resolution | **Merged into @Vibe** — the "publish" step is just one capability of the dive partner |

The separate "Fork Resolver" agent no longer makes sense. The AI that helps you think during the dive is the same AI that helps you compress your findings for the team. This simplifies the agent architecture from 3 agents to 2.

---

## 5. What Stays the Same

Not everything changes. The mechanism is similar; the framing is different.

| Stays | Why |
|-------|-----|
| Thread as the core unit | Threads are where teams discuss. Deep dives branch from threads. |
| Side-context creation | You still create a separate context for deep work. The DB model (parent_message_id → fork messages) is fine. |
| AI-generated structured output | The resolution prompt (validated at 4.45/5) still works — it summarizes the dive. |
| Progressive disclosure (headline/summary/full) | This is even MORE important in the deep dive model. |
| Channel/workspace structure | Organizational structure is orthogonal to the dive mechanism. |
| Tech stack | No infrastructure changes needed. |
| Supabase + Fly.io deployment | Same. |
| BDD test structure | Scenarios need language updates but structure is sound. |

The resolution prompt (validated at 4.45/5) works well for deep dive results too — a dive between a human and AI produces decisions, findings, and action items just like a multi-human fork would. The prompt may need minor tweaks to reflect that the "participants" include AI as a thinking partner, not just as a summarizer.

---

## 6. What This Means for Pain Point Solutions

From the [Slack Pain Ranking](slack-pain-ranking.md), the deep dive model changes the solution priority:

| Pain Point | Fork Solution | Deep Dive Solution |
|------------|--------------|-------------------|
| P1: No explicit outcomes | Fork forces closure | Deep dive produces structured findings by design (the whole point is to produce a publishable result) |
| P2: Topic drift | Fork isolates sub-topics | Deep dive lets individuals go deep WITHOUT derailing the thread |
| P3: Context fragmentation | N/A | Deep dive with AI can hydrate context from linked tools |
| P4: No structured output | Resolution summary | Dive results ARE structured output |
| P5: Async-sync gap | N/A | Deep dives can process meeting transcripts, not just chat |

**Key insight:** The deep dive model naturally addresses P1, P2, and P4 simultaneously — because the output is structured by design, topics don't drift in the main thread (you go deep separately), and every dive produces an explicit conclusion.

The slack-pain-ranking recommendation of "Option 3: complementary layers" still holds, but reframed:

- Layer 1: Every thread gets AI summary capability (auto-summary + on-demand)
- Layer 2: Drift nudge suggests "deep dive on this?" instead of "fork this"
- Layer 3: Deep dive for individuals who need to think deeper with AI
- Layer 4: Dive result posted back with progressive disclosure

---

## 7. Competitive Position

### What We're NOT Competing With

- Slack AI / Notion AI / "AI meeting notes" bots (thread summarizers)
- ChatGPT / Claude chat (solo AI conversation)
- Linear / Notion (project management with AI)

### What We ARE

A workspace where **AI is your cognitive amplifier inside team conversations**. No one else has this:

- ChatGPT lets you deep dive with AI — but disconnected from your team context
- Slack lets you discuss with your team — but without AI as a thinking partner
- OpenVibe combines both: deep dive with AI inside the team thread, compressed output for the team

### The Moat (Restated)

- **Behavioral:** Team builds the habit of "deep dive before you respond" — this changes decision quality
- **Data:** Accumulated deep dive results become the team's knowledge base
- **Network:** The more people deep dive, the richer the thread context for future dives

---

## 8. Documents Affected

~1,450 references to "fork" across 21 of 23 project documents. Not all need updating — the DB model and internal architecture can keep "fork" as a technical term. But these documents need reframing:

### Critical (Narrative-Setting)

| Document | What Needs Changing |
|----------|-------------------|
| `docs/INTENT.md` | Sprint plan language, success criteria |
| `docs/research/SYNTHESIS.md` | Executive summary, Finding #1 |
| `docs/research/phase-1.5/MVP-DESIGN-SYNTHESIS.md` | Executive summary, core user flows, product definition |
| `docs/research/phase-1.5/THREAD-UX-PROPOSAL.md` | Already has the right insight — needs consistent language throughout |
| `docs/research/R1-THREAD-MODEL.md` | Framing of the recommended model |
| `docs/PRODUCT-REASONING.md` | Derivation 1 language |

### Important (Specification)

| Document | What Needs Changing |
|----------|-------------------|
| `docs/research/phase-1.5/BACKEND-MINIMUM-SCOPE.md` | Table names are fine (forks table), but descriptions need updating |
| `docs/research/phase-1.5/FRONTEND-ARCHITECTURE.md` | Component naming, store naming |
| `docs/research/phase-1.5/BDD-IMPLEMENTATION-PLAN.md` | Feature and scenario language |
| `docs/research/phase-1.5/AGENT-DEFINITION-MODEL.md` | Fork Resolver → merged into @Vibe |

### Low Priority (Technical / Internal)

- `docs/design/M1-THREAD-ENGINE.md` — Already superseded by Phase 1.5
- `docs/research/R3-AGENT-LIFECYCLE.md` — Minor fork references
- `docs/architecture/` files — DB schema can keep `forks` table name

### Approach

Rather than doing a mass search-and-replace (which would break 21 docs), each critical document gets a **reframe notice** at the top pointing to this document. The language updates happen incrementally during Sprint 1-2 implementation.

---

## 9. For the Reader: TL;DR

1. **The product was originally about AI cognitive amplification**, not conversation management
2. **"Fork/resolve" drifted from Git metaphor research** and became the wrong frame
3. **The mechanism is similar** (side-context → structured output → main thread), but the **purpose, mental model, and AI role are fundamentally different**
4. **Deep dive = 1 human + AI thinking together**. Not a group side-discussion.
5. **The AI is a thinking partner throughout**, not a summarizer at the end
6. **This is a more defensible product** — "cognitive amplifier inside team conversations" is a new category; "Slack with AI summaries" is a crowded market
7. **All prior documents should be read through this lens** — when they say "fork," think "deep dive"

---

*Created: 2026-02-07*
*Reason: Founder identified concept drift from original thesis*
*Impact: Reframes product narrative, UX language, AI role, and competitive positioning*
