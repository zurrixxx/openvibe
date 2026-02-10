# Adoption Wedge Analysis

> Status: Draft | Date: 2026-02-07
> Purpose: Identify which Slack conversations shift easiest to Vibe AI Workspace
> Dependency: fork-necessity-analysis.md (same dataset, 1,097 threads)

> **REFRAME NOTICE (2026-02-07):** This analysis was conducted before the product reframe from "Fork/Resolve"
> to "AI Deep Dive." The findings about which conversations benefit most from structured side-context + AI
> compression still apply. Where this doc says "fork/resolve threads," read "deep dive with AI."
> See [`PRODUCT-CORE-REFRAME.md`](PRODUCT-CORE-REFRAME.md).

---

## 1. The Question

Assuming Vibe AI Workspace ships with fork/resolve threads — which conversations
should we target first for dogfood? We need a scenario that is:

1. **High pain** — Slack clearly fails at it (low resolution rate)
2. **High frequency** — Happens often enough to build habit
3. **Low switching cost** — Doesn't require the whole company to move
4. **Self-contained** — Doesn't depend heavily on external tools (Figma, GitHub, Intercom)
5. **Fork value is obvious** — The first use immediately shows the benefit

---

## 2. Frequency Analysis

From 1,097 threads over 3 months (Oct 2025 – Jan 2026):

### By category (monthly rate)

| Category | Total | /month | /week | Resolution Rate | Pain |
|----------|-------|--------|-------|-----------------|------|
| Operations/logistics | 288 | 96 | 24 | 65% | Low |
| Product/design review | 285 | 95 | 24 | 37% | **High** |
| Support & troubleshooting | 193 | 64 | 16 | 27% | High |
| Make decision/align | 193 | 64 | 16 | 43% | **Medium-High** |
| Request review/feedback | 225 | 75 | 19 | 32% | **High** |
| Planning & coordination | 125 | 42 | 10 | 22% | **Highest** |
| Marketing/GTM | 80 | 27 | 7 | 39% | Medium |
| Fix/troubleshoot | 153 | 51 | 13 | 31% | High |
| Plan work/scope | 38 | 13 | 3 | 18% | Highest |

### The frequency × pain matrix

```
                    HIGH FREQUENCY (>15/week)          LOW FREQUENCY (<10/week)
              ┌─────────────────────────────────┬──────────────────────────────┐
  HIGH PAIN   │ Product/design review (24/wk)   │ Planning & coordination      │
  (< 35%      │ Request review/feedback (19/wk) │   (10/wk, 22% resolved)      │
   resolved)  │ Support & troubleshoot (16/wk)  │ Plan work/scope              │
              │ Fix/troubleshoot (13/wk)        │   (3/wk, 18% resolved)       │
              │                                 │                              │
              │        ★ SWEET SPOT ★           │   Pain is real but too       │
              │                                 │   infrequent to build habit  │
              ├─────────────────────────────────┼──────────────────────────────┤
  LOW PAIN    │ Operations/logistics (24/wk)    │ Marketing/GTM (7/wk)         │
  (> 50%      │ Coordinate execution (10/wk)    │ Admin/policy (3/wk)          │
   resolved)  │ Share status/FYI (8/wk)         │ Data/metrics (2/wk)          │
              │                                 │                              │
              │   Slack already works fine.      │   No reason to switch.       │
              │   No reason to switch.           │                              │
              └─────────────────────────────────┴──────────────────────────────┘
```

**Sweet spot: Product/design review + decision-making + review/feedback.**
Combined: ~60 threads/week, resolution rate 32-43%.

---

## 3. External Tool Dependency (the hidden filter)

Not all high-pain, high-frequency discussions can shift. Many depend on external tools
that Slack integrates with. From the top linked domains:

| Domain | Links | Implies |
|--------|-------|---------|
| app.intercom.com | 353 | Support threads → need Intercom integration |
| figma.com | 248 | Design review → need Figma preview/embed |
| github.com | 190 | Dev discussions → need code context |
| app.hubspot.com | 180 | Sales/marketing → CRM dependency |
| docs.google.com | 171 | Cross-functional → link sharing sufficient |
| drive.google.com | 128 | File sharing → link sharing sufficient |
| mixpanel.com | 86 | Data discussions → need dashboard access |

**What this means for each category:**

| Category | Tool Dependency | Can shift without integrations? |
|----------|----------------|-------------------------------|
| Product/design review | Figma (heavy) | **Partially** — the DISCUSSION can shift, the visual review can't |
| Decision-making | Docs (moderate) | **Yes** — decisions are mostly text-based, links suffice |
| Review/feedback | Figma + Docs | **Partially** — depends on what's being reviewed |
| Support/troubleshoot | Intercom (heavy) | **No** — needs customer context in-tool |
| Fix/troubleshoot | GitHub (heavy) | **No** — needs code context |
| Planning | Docs (light) | **Yes** — planning is mostly conversational |
| Operations | Multiple | **No** — operational threads touch many systems |

**After filtering for tool dependency:**
- **Decision-making / alignment** — shifts cleanly, text-based
- **Planning** — shifts cleanly, but low frequency
- **Product direction discussions** (subset of product/design) — the strategic part, not the pixel review
- **Review/feedback on docs/proposals** — when reviewing text, not visual design

---

## 4. Candidate Scenarios (ranked)

### Scenario A: Product Direction Decisions
**Examples from data:** SaaS offering strategy, kiosk mode pivot, Bot PDP roadmap,
Canvas pen feature response, thread vs space architecture debate

| Dimension | Assessment |
|-----------|-----------|
| Frequency | ~15-20/week (subset of product/design + decision categories) |
| Pain | High — 37-43% resolution, frequent topic drift |
| Switching cost | **Very low** — the dogfood team IS this group (Charles, Sean, Stan, Jiulong, etc.) |
| Tool dependency | Low — these are text/strategy discussions, links to docs suffice |
| Fork value | **Immediately obvious** — our 5 test cases were exactly this type |
| Group size | 3-5 people (matches dogfood team size) |

**Why it's the best entry point:**
- The people making these decisions are the people building the product
- They've already experienced the pain (the test conversations prove this)
- Fork/resolve directly addresses their #1 problem (tangled multi-topic threads)
- Zero switching cost — they don't need to convince anyone else to join
- Resolution summaries become the team's decision record

**Risk:** Frequency might be lower than estimated for the dogfood group specifically.
Vibe has ~20 people, but the dogfood group might be 5-8. At 5-8 people, they might
generate 5-8 product direction threads per week, not 15-20.

### Scenario B: Cross-functional Alignment
**Examples:** "Hey @PM @Eng @Design, what should we do about X?"

| Dimension | Assessment |
|-----------|-----------|
| Frequency | ~10-15/week |
| Pain | Medium-high — 43% resolution for decision threads |
| Switching cost | Low-medium — needs 2-3 functions to participate |
| Tool dependency | Low — mostly text discussion with doc links |
| Fork value | High — different functions = different sub-topics = natural fork points |
| Group size | 3-5 people |

**Why it works:** Cross-functional threads have natural fork points ("let me check with eng"
→ fork). But requires slightly more people to adopt simultaneously.

### Scenario C: Meeting Follow-up / Async Continuation
**Examples:** Post-huddle action items, decisions that need async input after a meeting

| Dimension | Assessment |
|-----------|-----------|
| Frequency | ~10-15/week (estimated from meeting-related threads) |
| Pain | Very high — these are the "55% partial" threads that move to meetings and never come back |
| Switching cost | Low — starts from a meeting artifact, not from Slack |
| Tool dependency | Low — meeting notes + discussion |
| Fork value | Moderate — the main value is forced closure, not necessarily forking |
| Group size | 3-6 people |

**Why it's interesting:** This addresses the "moved to meeting" problem directly.
After a huddle, instead of "someone should write up the decision in Slack," the team
forks each action item in Vibe AI and resolves them. The resolution becomes the
meeting record.

**Risk:** Requires a behavior change at the meeting → async transition point. Harder
than "just start discussing in Vibe AI."

### Scenario D: Design Feedback (text portion)
**Examples:** "Should we use clone or browse model?" "What's the trash behavior?"

| Dimension | Assessment |
|-----------|-----------|
| Frequency | ~24/week (but only ~40% is text-based, rest needs Figma) |
| Pain | High — 37% resolution, 32% for review/feedback |
| Switching cost | Medium — needs designer + eng + PM |
| Tool dependency | **Medium-high** — even "text" design discussions often reference Figma |
| Fork value | High — design reviews naturally split into sub-concerns |
| Group size | 2-4 people |

**Why it's risky as entry point:** Even when the discussion is text-based, designers
want to reference their Figma. Without Figma embed/preview, they'll stay in Slack
where they can paste Figma links and get auto-previews.

---

## 5. Adoption Dynamics

### The Slack gravity problem

Slack is already open. It's muscle memory. The switching cost isn't "learning a new tool" —
it's "remembering to open a different tool when you want to discuss something."

This means the entry point needs to be:
1. **A moment of pain** — "This Slack thread is getting messy" is the trigger
2. **Lower friction than the alternative** — "Fork this" must be easier than "start a new Slack thread and re-explain the context"
3. **Immediate payoff** — The resolution summary must feel like magic the first time

### Who adopts first?

| Who | Why they'd switch | Why they wouldn't |
|-----|------------------|-------------------|
| Charles (CEO) | Experiences tangled threads daily. Needs decision records. | Might not have time for new tool adoption. |
| Sean (Product) | Reviews and alignment threads are his #1 pain. | Heavy Figma dependency for design review. |
| Jiulong (Eng Lead) | Technical decisions need structured resolution. | GitHub + code context dependency. |
| Stan (PM) | Planning threads have 18% resolution rate. | HubSpot + Intercom dependency for GTM. |

**Charles is the ideal first adopter.** He initiates the most product direction threads,
experiences the most pain from tangled discussions, and his adoption signals to the team
that this is the real tool.

### Frequency threshold for habit formation

Research suggests ~3x/week minimum to build a tool habit. The dogfood group (5-8 people)
needs to generate at least 3 threads/week in Vibe AI to make it sticky.

Given the data: product direction + decision threads ≈ 5-8/week for a group this size.
This clears the threshold, but barely. If adoption is partial (only 2-3 people
actually use it), frequency drops below 3/week and the tool dies.

**Implication:** The ENTIRE dogfood group needs to commit, not just 1-2 champions.

---

## 6. Recommended Entry Scenario

### Primary: "Product Direction Decisions"

**What:** When the leadership/product team needs to make a strategic or product
direction decision, start it in Vibe AI instead of Slack.

**Trigger moment:** Anytime someone would type a message like:
- "@Sean @Stan 关于 X 的策略是什么"
- "对于 Y 我们有几个选择..."
- "看了 Z 之后我觉得我们需要重新想一下..."

**Why this specific scenario:**
1. Already ~5-8x/week for the dogfood group
2. 100% text-based, zero tool dependency
3. Fork/resolve value is immediately clear (from our test data)
4. The dogfood team IS the user group — no adoption dependency on others
5. Resolution summaries become the team's decision log (new value Slack can't provide)

**NOT this scenario (initially):**
- Design review (needs Figma)
- Bug discussion (needs GitHub)
- Customer issues (needs Intercom)
- Operations (Slack works fine for this)

### Secondary: "Meeting Follow-up"

After huddles/meetings, post the meeting summary in Vibe AI and fork each action item
for async follow-up. This naturally brings the team into the tool at a predictable
cadence (after every meeting).

### What success looks like (Week 1-2)

| Metric | Target |
|--------|--------|
| Threads started in Vibe AI | 3-5/week |
| Forks created | 5-10/week |
| Forks resolved | 3-5/week |
| Active users | 4+ of 5-8 dogfood members |
| "Went back to Slack for this" incidents | Track but don't penalize |

---

## 7. What Could Go Wrong

| Risk | Likelihood | Mitigation |
|------|-----------|------------|
| Frequency too low to build habit | Medium | Combine with meeting follow-up scenario |
| Slack gravity wins — people forget to use Vibe AI | High | Charles needs to lead by example consistently |
| "I'll just paste the Figma link in Slack" | High | Accept this — don't fight tool dependency early |
| Fork/resolve feels like overhead vs. just chatting | Medium | Onboarding: show resolution summary value first |
| One person doesn't adopt, breaks the group | Medium | Start with voluntary, don't force |

**The #1 risk is Slack gravity.** The tool needs to feel SO MUCH BETTER for this
specific scenario that the dogfood team actively chooses it. If it's "about the same,"
Slack wins by default.

---

## 8. Honest Limitations

- **All frequency estimates are from Vibe's FULL team (~20 people), not the dogfood group (5-8).** Actual frequency for the dogfood group will be lower.
- **"Easiest to shift" is a judgment call**, not a data-derived conclusion. We're combining resolution rate data (objective) with tool dependency and switching cost assessments (subjective).
- **We don't know if the dogfood team actually PERCEIVES the pain.** They might think Slack works fine. The data says otherwise, but perception drives adoption, not data.
- **Scenario A (product direction) is also the HARDEST to get wrong.** If the CEO's strategic decisions are summarized poorly by the AI, trust evaporates immediately. High stakes for the resolution prompt to perform.

---

*Analyzed: 2026-02-07*
*Data: Same 1,097-thread dataset as fork-necessity-analysis.md*
*Estimates: Monthly/weekly rates computed from 3-month observation period*
