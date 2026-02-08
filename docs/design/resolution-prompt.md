# Deep Dive Resolution Prompt Design

> Status: Validated (v2) | Date: 2026-02-07
> Purpose: Design and validate the AI prompt that generates structured results when a deep dive is published
> Risk: #1 in Risk Register — "AI summary quality is insufficient"
> Test result: **4.45/5 average (89%)** across 5 real Vibe team conversations

> **REFRAME NOTE (2026-02-07):** This doc was originally titled "Fork Resolution Prompt." In the AI Deep Dive
> model, this prompt runs when a user **publishes** their deep dive findings back to the team thread. The prompt
> itself is unchanged and validated — it generates structured output (headline + bullets + deferred items + open
> questions) from a side-context conversation. The validation results apply directly.
> See [`PRODUCT-CORE-REFRAME.md`](PRODUCT-CORE-REFRAME.md).

---

## 1. Context

When a user resolves a fork, OpenVibe generates a structured summary that gets posted
to the main thread. This summary is the **entire output** of the fork visible to
non-participants. If the summary is bad, the fork/resolve model fails.

### Requirements (from MVP-DESIGN-SYNTHESIS)
- Decision #11: Progressive disclosure — headline / summary / full
- Decision #15: No streaming — collect full response then post
- Open Question #5: Structured (headline + bullets) vs free-form → **structured**
- Open Question #6: Posted as system message with special rendering
- Open Question #7: Post-processing with Haiku → **yes, separate call**

### What the Gist analysis tells us about real threads
- 1097 threads analyzed (Oct-Jan 2026), >=5 replies each
- 42% resolve clearly, 55% partial — most threads lack explicit closure
- "Partial closure dominates" — threads reach next steps but stop short
- Common patterns: clarification loops, cross-functional handoffs, artifact-driven
- Threads with topic drift have 0% resolution rate
- Source: `https://gist.github.com/jiulongw/f5a7d8c07df1d1927502cdce5f5d6ee6`

---

## 2. Prompt Design

### 2.1 Input Structure

```
PARENT_MESSAGE: The message the fork was created from (provides context for why the fork exists)
FORK_MESSAGES: All messages in the fork, in chronological order (author + content + timestamp)
FORK_DESCRIPTION: The user-provided or auto-generated fork description
```

### 2.2 Resolution Prompt (v2 — validated)

```
You are a fork resolution summarizer for a team collaboration tool.

A "fork" is a side-discussion that branched off from a main thread. The user has
decided this fork's work is complete and wants to post a summary back to the main
thread. Your job is to distill the fork into a concise, accurate summary.

## Context

**Fork description:** {{FORK_DESCRIPTION}}

**Original message (fork point):**
{{PARENT_MESSAGE}}

**Fork discussion ({{MESSAGE_COUNT}} messages, {{PARTICIPANT_COUNT}} participants):**
{{FORK_MESSAGES}}

## Instructions

Generate a resolution summary in the following JSON format:

{
  "headline": "A single sentence (max 120 chars) that captures THE key outcome or decision. Start with a verb or noun, not 'The team discussed...'",
  "bullets": [
    "Key finding, decision, or action item — one per bullet",
    "Include WHO is responsible for action items when explicitly assigned in the discussion",
    "3-5 bullets. Fewer is better if the discussion was focused."
  ],
  "deferred_items": [
    "Decisions explicitly deferred to future iterations (0-2 items)"
  ],
  "open_questions": [
    "Genuinely unresolved questions that remain open after this fork discussion (0-2 items)"
  ]
}

## Rules

1. ONLY include information that was explicitly discussed in the fork messages.
   Never infer, speculate, or add information not present in the conversation.
   1a. If a participant corrects themselves in a later message, use the corrected
       information and omit the original error.
2. Prioritize DECISIONS and ACTIONS over discussion process.
   2a. Include process information ONLY if it explains why a decision was made
       or why information is incomplete.
   Bad: "The team discussed three options for rate limiting"
   Good: "Chose token bucket rate limiting via Cloudflare Workers"
3. If no clear decision was reached, state the outcome honestly.
   Examples: "Rate limiting approach narrowed to 2 options, needs final call"
             "Thread UX architecture discussed; follow-up meeting scheduled"
4. Use the participants' own language and terminology.
   4a. Output in English. Preserve key technical terms and product names as-is.
5. If the fork contains code snippets or technical details, reference them
   but don't reproduce them. Example: "Implementation in auth/middleware.ts"
6. Keep bullets concrete and actionable. Avoid vague summaries.
7. Distinguish between "deferred_items" (decided to postpone) and
   "open_questions" (no decision made). Use the appropriate field.
8. For action items without explicit owners, use passive voice
   (e.g., "Roadmap impact to be assessed") rather than inventing assignments.
```

### 2.3 Haiku Post-Processing Prompt (for progressive disclosure)

This is a separate, cheaper call that runs on the agent's full response (not the fork resolution). Used when an agent response exceeds 500 words.

```
Summarize this AI agent response into exactly two parts:

1. HEADLINE: One sentence (max 100 chars) that captures the main point.
2. SUMMARY: 3-5 bullet points covering the key information.

The full response will be available via "Show more". Your summary should give
enough context that a reader can decide whether to expand.

Response to summarize:
{{AGENT_RESPONSE}}

Return as JSON: {"headline": "...", "summary": ["...", "..."]}
```

---

## 3. Test Plan

### 3.1 Test Conversations

| # | Type | Source | Channel | Messages | Participants |
|---|------|--------|---------|----------|-------------|
| 1 | Design decision | Chat share behavior | #team-ai-dev-cn | 11 | 3 (Jiulong, Ludan, Levey) |
| 2 | Architecture exploration | Thread vs Space UX | #proj-vibe-ai | 12 | 3 (Charles, Sean, Ludan) |
| 3 | Strategic direction | Bot PDP roadmap pivot | #core-product | 3 | 1 (Charles) |
| 4 | Multi-stakeholder strategy | SaaS offering + AI Memory | #core-product | 20 | 5 (Charles, Jiulong, Sean, Stan, Yinan) |
| 5 | Customer-driven decision | Canvas pen feature backlash | #core-product | 5 | 3 (Charles, Sean, Lidia) |

### 3.2 Evaluation Criteria

| Criteria | Weight | Description |
|----------|--------|-------------|
| Accuracy | 40% | No hallucinated facts. Every bullet traceable to a message. |
| Completeness | 25% | Key decisions/actions captured. Nothing important missing. |
| Conciseness | 20% | No fluff. Would a non-participant get the gist in 10 seconds? |
| Headline quality | 15% | Captures THE outcome. Not generic. Not too long. |

### 3.3 Rating Scale

- **5/5**: Perfect — would post without editing
- **4/5**: Good — minor wording tweaks only
- **3/5**: Acceptable — captures the right info but needs restructuring
- **2/5**: Poor — missing key info or includes wrong info
- **1/5**: Unusable — hallucinated, incoherent, or completely off

**Target: Average 4+/5 across test conversations.**

---

## 4. Test Results

### Test 1: Chat Share Design Discussion (4.65/5)

**Source:** #team-ai-dev-cn, thread 1765255912.466149
**Type:** Design decision — multiple options discussed, one chosen
**Messages:** 11 | **Participants:** Jiulong Wang, Ludan Chuang, (Levey mentioned)

**Output:**
```json
{
  "headline": "Chat sharing changed from auto-clone to browse-first model with manual save",
  "bullets": [
    "Shared links now open in browse/view mode showing 'Shared by User', not auto-clone",
    "Users must click 'Save a copy to my chats' to clone; after cloning, becomes personal chat",
    "Shared links update with new content (ChatGPT model), not new links per update (Grok model)",
    "Trash behavior: deleted chats invalidate links temporarily; restore re-enables; permanent after 30 days",
    "Ludan to update Figma flow and sync with Shane"
  ],
  "deferred_items": [
    "Remembering opened shared links — deferred to future iteration with group chat and permissions"
  ],
  "open_questions": []
}
```

**Evaluation:**

| Criteria | Score | Notes |
|----------|-------|-------|
| Accuracy | 5/5 | All points directly traceable. No hallucinations. |
| Completeness | 5/5 | Captured initial problem, solution evolution, trash behavior, deferred items. |
| Conciseness | 4/5 | Dense but readable. Could merge bullets 1-2. |
| Headline | 4/5 | Action-oriented, captures core UX shift. |
| **Overall** | **4.65/5** | |

---

### Test 2: Thread vs Space UX Architecture (4.35/5)

**Source:** #proj-vibe-ai, thread 1763226254.160899
**Type:** Architecture exploration — partially resolved, led to meeting
**Messages:** 12 | **Participants:** Charles Yang, Sean Chiu, (Ludan mentioned)

**Output:**
```json
{
  "headline": "Thread should be collaboration center, not Space; Space becomes organizational container",
  "bullets": [
    "Thread = 'context-based dropbox' with feed-based interface (Slack-like density, WhatsApp-like input)",
    "Sean's design had Space as collaboration center; missing Space knowledge presentation layer",
    "AI analysis identified 10 risks with Space-centric model: too heavy for sharing, tasks/discussions lose context",
    "New direction: Share threads (lightweight), not spaces; tasks/discussions/meetings should be thread-based",
    "Charles & Sean scheduled huddle to finalize thread UX (2025-11-21)"
  ],
  "deferred_items": [],
  "open_questions": [
    "Whether to add third organizational layer: Workspace > Domain > Space",
    "Final thread UX structure not documented (resolved in follow-up meeting)"
  ]
}
```

**Evaluation:**

| Criteria | Score | Notes |
|----------|-------|-------|
| Accuracy | 5/5 | All bullets trace to messages. AI feedback reference correct. |
| Completeness | 4/5 | Got core shift. Missing "aha moment" concept Charles emphasized. |
| Conciseness | 3/5 | Bullet 1 is context rather than decision. Could be tighter. |
| Headline | 5/5 | Perfectly captures architectural decision in one sentence. |
| **Overall** | **4.35/5** | |

**Note:** This conversation is an exploration, not a clean decision. The prompt handled the "inconclusive → scheduled meeting" outcome well.

---

### Test 3: Bot PDP Roadmap Pivot (4.85/5)

**Source:** #core-product, thread 1768883143.836219
**Type:** Strategic direction — single-author, self-correcting
**Messages:** 3 | **Participants:** Charles Yang

**Output:**
```json
{
  "headline": "Bot narrative pivots from meeting camera to AI workspace entry point; roadmap delayed for completeness",
  "bullets": [
    "Core narrative: FROM 'meeting camera + transcription' TO '360 meeting device + Vibe AI Workspace entry'",
    "Core capabilities: in-conversation (listen/understand, talk/action, present) + after-meeting (memory & collaboration)",
    "Current roadmap gaps: Next Action, reply quality, Claude backend all missing",
    "Decision: delay launch to deliver complete product rather than ship incomplete",
    "Next actions: (1) Claude Code integration plan (2) Roadmap impact (3) Product spec (4) Architecture review"
  ],
  "deferred_items": [],
  "open_questions": [
    "How to integrate Claude Code/OpenCode capabilities as backend intelligence?"
  ]
}
```

**Evaluation:**

| Criteria | Score | Notes |
|----------|-------|-------|
| Accuracy | 5/5 | Correctly used self-corrected capability model from msg 2. |
| Completeness | 5/5 | Strategic pivot, gaps, decision logic, next steps all captured. |
| Conciseness | 4/5 | Tight. Minor room to compress. |
| Headline | 5/5 | Dual-punch: WHAT changed + HOW (delay). |
| **Overall** | **4.85/5** | |

---

### Test 4: SaaS Offering Strategy & AI Memory Architecture (3.85/5)

**Source:** #core-product, thread 1762160960
**Type:** Multi-stakeholder strategy — strategic direction, misaligned assumptions corrected, multi-layered (kiosk + SaaS + memory tiers)
**Messages:** 20 | **Participants:** Charles Yang, Jiulong Wang, Sean Chiu, Stan Feng, Yinan Xu

**Output:**
```json
{
  "headline": "SaaS offering restructured around Room AI plan with ARR attach rate as north star metric",
  "bullets": [
    "Kiosk mode confirmed as default experience for all S1/S1 Pro boards, emphasizing Canvas AI and multi-model recording features",
    "Stan to lead comprehensive SaaS offering proposal, coordinating with Sean (strategy), Tanya (GTM/Growth), and Molly (talent planning)",
    "AI capabilities structured in 3 dimensions: Capture & Transcript, Summarization & Info Extraction, AI Agent & Workflow, mapped to Personal AI (Dot/Orbit) vs Room AI (Bot/Board) offerings",
    "Memory architecture proposal: Device AI Package = isolated recordings, Pro Plan = personal-level memory, Team Plan = team-level memory and collaboration",
    "Pro Plan will include limited Space/file count and partial Thread/Context experience to enable upsell path to Team Plan"
  ],
  "deferred_items": [
    "Memory scope definition for non-meeting Board use cases (browser, whiteboarding without audio input)"
  ],
  "open_questions": [
    "Public vs private context handling for Board's multiple space/role combinations and anonymous users"
  ]
}
```

**Evaluation:**

| Criteria | Score | Notes |
|----------|-------|-------|
| Accuracy | 4/5 | All facts traceable. "North star metric" from Charles's message. |
| Completeness | 4/5 | Major strategic decisions captured. Missing: specific GTM/channel sales context. |
| Conciseness | 3/5 | Bullet 3 includes full taxonomy which may be too granular for a summary. |
| Headline | 4/5 | Accurate and outcome-focused. Could surface kiosk mode clarification more prominently. |
| **Overall** | **3.85/5** | |

**Note:** Complex 20-message strategic discussion with multiple sub-topics. The prompt handles the kiosk mode misunderstanding correction well (both Jiulong and Sean admit misalignment, Charles clarifies), but the AI capability taxonomy in bullet 3 is over-detailed for a summary. This is the hardest test case — longest thread, most participants, most layered strategy.

---

### Test 5: Canvas Pen Feature — Customer Backlash (4.55/5)

**Source:** #core-product, thread 1768371106
**Type:** Customer-driven decision — complaint response, product compromise, downstream communication
**Messages:** 5 | **Participants:** Charles Yang, Sean Chiu, Lidia (mentioned)

**Output:**
```json
{
  "headline": "Custom pen feature to remain paywalled in public sessions, reopened for logged-in private sessions",
  "bullets": [
    "Sean to implement solution: private sessions (logged-in users) get custom pens, public sessions maintain full tool visibility for feature discovery",
    "Jiulong confirmed feasibility; design starting this week, Jiulong will implement with adjusted brush size selection and defaults for public sessions",
    "Product team to brief support team on the change to avoid user confusion",
    "Pixel brush rationale preserved: performance optimization, future AI text conversion capability, and eraser functionality retention"
  ],
  "deferred_items": [],
  "open_questions": [
    "Whether to continue pushing Vibe service and standalone device management after Dot launch (planned service sunset in H2)"
  ]
}
```

**Evaluation:**

| Criteria | Score | Notes |
|----------|-------|-------|
| Accuracy | 5/5 | Every detail traceable. Correctly distinguishes decision from context. |
| Completeness | 5/5 | Decision, implementation plan, support communication, and tangential service sunset captured. |
| Conciseness | 4/5 | Bullet 4 (rationale) could be condensed, but overall tight. |
| Headline | 4/5 | Clear outcome. "Paywalled" is slightly informal but accurate. |
| **Overall** | **4.55/5** | |

**Note:** Clean focused discussion. The prompt correctly identifies the compromise solution (public vs private sessions) and picks up the downstream communication gap Charles flagged. The service sunset question (from msg 4) correctly placed in open_questions.

---

## 5. Iteration Log

| Version | Change | Reason | Impact |
|---------|--------|--------|--------|
| v1 | Initial prompt | — | Baseline |
| v2 | Added `deferred_items` field | Test 1 conflated deferred decisions with open questions | Cleaner separation of "decided to punt" vs "no decision" |
| v2 | Added self-correction rule (1a) | Test 3 had self-correction; worked by luck in v1 | Explicit guidance for common pattern |
| v2 | Added process info rule (2a) | Test 2 showed process context sometimes necessary | Less aggressive pruning of useful context |
| v2 | Improved inconclusive handling (3) | Test 2 ended with "let's meet" — valid outcome | Better headline examples for non-decisions |
| v2 | Added language rule (4a) | All tests mixed Chinese/English | Always output English, preserve terms |
| v2 | Added passive voice rule (8) | Tests had unassigned actions | Prevents invented assignments |

---

## 6. Resolved Decisions

1. **Model for resolution**: **Sonnet 4.5**
   - Risk Register says "Use Sonnet 4.5 (not Haiku) for summaries"
   - Cost: ~$0.01-0.03 per resolution (acceptable at ~50 forks/month = ~$1.50/mo)
   - Haiku for progressive disclosure post-processing only

2. **Output language**: **English always, preserve technical terms**
   - Vibe team's working language for written artifacts is English
   - Chinese terms preserved when they're product-specific

3. **Output structure**: **JSON with 4 fields**
   - `headline`, `bullets`, `deferred_items`, `open_questions`
   - Frontend parses JSON, renders as structured card

## 7. Remaining Open Decisions

1. **Max fork size**: What if a fork has 50+ messages?
   - Sonnet's 200K window can handle ~400 messages easily
   - Recommendation: include all messages, no truncation for MVP
   - Revisit if context costs become significant

2. **User editing**: How much editing should the UI allow?
   - Recommendation: allow editing headline + bullets before posting
   - Do NOT allow editing after posting (integrity of resolution)

---

*Validated: 2026-02-07*
*Test data source: Real Vibe team Slack conversations (5 threads, 51 total messages)*
