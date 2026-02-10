# Feedback Loop Design

> V2 Design Doc | Created: 2026-02-09
> Status: Draft
> Depends on: AGENT-MODEL.md, V2-VISION.md
> Layer: 3 (Learning) — builds on Layer 1 (Trust & Governance) and Layer 2 (Agent as Employee)

---

## 0. The Problem, Stated Precisely

Current AI tools have broken feedback loops:

- **ChatGPT**: You give feedback in one session. Next session, it's gone. The "Memory" feature is a band-aid — it stores facts ("user prefers concise answers"), not behavioral corrections ("you overcomplicated the last analysis").
- **Copilot/Cursor**: You accept or reject completions. The tool learns nothing from your rejections. It makes the same mistakes next time.
- **Slack AI**: You can't give feedback at all. It summarizes. You read it. There's no loop.

The tightest feedback loop wins. If human judgment takes 3 seconds to feed back into agent behavior, the team gets exponentially more value than if it takes 3 minutes (or never).

**OpenVibe's Layer 3 thesis**: The workspace that converts human judgment into persistent agent improvement fastest will produce agents that teams actually trust — not because the underlying LLM is better, but because the agent has been shaped by the team's standards.

---

## 1. Design Principles

**1. Feedback is a side-effect of work, not a separate activity.**
People don't "give feedback." They react, edit, ignore, rewrite, escalate. The system must capture signal from these natural behaviors, not demand explicit evaluation ceremonies.

**2. 3 seconds or it won't happen.**
If explicit feedback takes more than 3 seconds, adoption drops to near-zero. Emoji reactions: ~1 second. Inline correction: ~5 seconds. Writing a note: ~30 seconds. Design for the 1-second case as default, with optional deeper paths.

**3. Feedback has a half-life.**
"Use shorter sentences" is permanent. "Our Q1 CAC was $42" expires. "Don't mention the acquisition" expires when the acquisition is announced. The system must handle temporal decay, not just accumulation.

**4. The human decides the blast radius.**
A correction to one message should not silently become a permanent behavioral rule. The user explicitly chooses: "this once" vs "always." Auto-promotion from local to permanent is dangerous — it assumes the system understands intent, and it doesn't.

**5. Silence is ambiguous. Don't pretend otherwise.**
No reaction to an agent's message could mean: "I agree," "I didn't read it," "I disagree but don't have time," or "I've left the company." The system should not interpret silence. It should measure engagement (did the user read it? did anyone act on it?) separately from approval.

---

## 2. Feedback Taxonomy

### 2.1 The Three Channels

| Channel | Examples | Capture Method | Effort | Signal Strength |
|---------|----------|---------------|--------|----------------|
| **Explicit** | Thumbs up/down, "do it differently," correction text | User deliberately acts | 1-30 sec | High (clear intent) |
| **Behavioral** | User ignores response, rewrites output, asks someone else, edits before sharing | System observes user actions | 0 sec (passive) | Medium (requires interpretation) |
| **Structural** | "Always do X," "Never do Y," trust level change, SOUL edit | Admin deliberately changes config | 30-300 sec | Highest (permanent) |

### 2.2 Explicit Feedback Types

| Type | Gesture | Effect | Persistence |
|------|---------|--------|-------------|
| **Approve** | Single emoji reaction (any positive: thumbs up, check, etc.) | Reinforces current behavior | Episodic memory (this episode = positive outcome) |
| **Reject** | Thumbs down reaction | Flags current response as bad | Episodic memory (negative outcome) + prompts optional correction |
| **Correct** | Reply with correction ("No, the number is $42, not $38") | Agent receives correction in conversation | Thread-persistent (agent uses correction in this thread) |
| **Redirect** | "Do it differently: be more concise / use tables / focus on X" | Agent adjusts approach in this conversation | Thread-persistent + optionally promoted to SOUL |
| **Instruct** | "Always / Never" button or explicit instruction | New behavioral rule | Permanent (added to SOUL constraints or behavior) |

### 2.3 Behavioral Signals

| Signal | What It Means | System Response |
|--------|---------------|-----------------|
| **User edits agent output before sharing externally** | Response was close but not right | Log the diff. Surface to admin: "Users edited @Growth's reports 8/10 times this week." |
| **User ignores agent response (no read receipt, no reaction, no reply within 24h)** | Ambiguous. Do NOT interpret as feedback. | Track engagement rate. Surface to admin as metric, not as feedback to the agent. |
| **User asks the same question to a different agent or human** | First agent's answer wasn't satisfactory | Log the pattern. "User asked @Growth, then re-asked in #general." |
| **User rewrites agent output from scratch** | Response was bad enough to redo | Strong negative signal. Log as implicit rejection. |
| **User forwards agent output without changes** | Output was useful as-is | Positive signal. Track "forwarded unchanged" rate. |

**Key decision: Behavioral signals feed the admin dashboard, not the agent directly.** The risk of misinterpreting behavioral signals and auto-adjusting agent behavior is higher than the benefit. A human (admin) reviews patterns and decides whether to translate them into explicit feedback or SOUL changes.

### 2.4 Structural Feedback

These are not "feedback" in the casual sense. They are deliberate configuration changes that happen to be informed by accumulated feedback.

| Action | Where It Lives | Who Can Do It |
|--------|---------------|---------------|
| Add a `never_do` constraint | `agents.soul.constraints.never_do[]` | Admin |
| Add a `guardrail` | `agents.soul.constraints.guardrails[]` | Admin |
| Change communication style | `agents.soul.behavior.communication` | Admin |
| Change trust level | `agents.trust_level` | Admin |
| Add a behavioral rule | `agents.soul.behavior.proactive[]` or `reactive[]` | Admin |

---

## 3. Feedback UI

### 3.1 Message-Level Feedback (< 3 seconds)

Every agent message gets a subtle feedback bar that appears on hover:

```
┌──────────────────────────────────────────────────┐
│  @Growth                                    L2   │
│                                                  │
│  Weekly growth report for Feb 3-9:               │
│  - DAU: 1,247 (+12% WoW)                       │
│  - Retention D7: 34% (-2pp)                     │
│  - Revenue: $12.4K (+8%)                        │
│                                                  │
│  D7 retention dipped due to onboarding flow      │
│  changes shipped Thursday. Recommend reverting   │
│  the tooltip removal.                            │
│                                                  │
├──────────────────────────────────────────────────┤
│  [thumbs up] [thumbs down]  [correct...]  [why] │  ← hover bar
└──────────────────────────────────────────────────┘
```

**[thumbs up]**: One click. Creates positive `agent_episode` (type: `feedback_received`, outcome: `positive`). No further action needed.

**[thumbs down]**: One click. Creates negative episode. Then opens a **minimal correction prompt**:

```
┌──────────────────────────────────────────────┐
│  What was wrong?                              │
│                                                │
│  [Inaccurate] [Wrong format] [Not useful]     │  ← quick tags (optional)
│                                                │
│  ┌──────────────────────────────────────────┐ │
│  │ Tell @Growth what to do differently...   │ │  ← optional free text
│  └──────────────────────────────────────────┘ │
│                                                │
│  [Just flag it]    [Send correction]           │
└──────────────────────────────────────────────┘
```

"Just flag it" = log negative feedback without a correction (still useful as a signal).
"Send correction" = log feedback AND post correction as a reply visible to the agent.

Total time for thumbs down + quick tag: ~3 seconds.
Total time for thumbs down + written correction: ~15 seconds.
Both are valid. The system works with either.

**[correct...]**: Opens inline editing. The user can highlight part of the agent's response and provide a correction directly. This is the PR review model applied to agent output.

```
┌──────────────────────────────────────────────────┐
│  @Growth                                         │
│                                                  │
│  D7 retention dipped due to onboarding flow      │
│  changes shipped Thursday.                       │
│  ╔══════════════════════════════════════════════╗ │
│  ║ Recommend reverting the tooltip removal.     ║ │  ← user highlighted this
│  ╚══════════════════════════════════════════════╝ │
│  ┌──────────────────────────────────────────────┐ │
│  │ Don't recommend actions. Flag the data,     │ │  ← inline correction
│  │ let the team decide.                         │ │
│  └──────────────────────────────────────────────┘ │
│  [Cancel]   [ ] Apply always   [Submit]          │
│                                  ↑                │
│                    checkbox promotes to SOUL rule  │
└──────────────────────────────────────────────────┘
```

The "Apply always" checkbox is the explicit promotion mechanism. Unchecked = this-thread-only correction. Checked = the correction becomes a behavioral rule in the SOUL.

**[why]**: Shows the agent's reasoning chain for this response. Not feedback — it's transparency. But it contextualizes feedback: if the user sees WHY the agent recommended reverting, they can give more precise feedback ("your reasoning was right, but don't give recommendations — just flag the data").

### 3.2 Thread-Level Feedback

At the end of a resolved deep dive or completed task, a compact feedback card:

```
┌──────────────────────────────────────────────────┐
│  Deep dive resolved                               │
│  @Vibe helped analyze pricing strategy            │
│                                                  │
│  Was this dive useful?                           │
│  [Very useful]  [Somewhat]  [Not useful]         │
│                                                  │
│  Optional: What would have made it better?       │
│  ┌──────────────────────────────────────────────┐ │
│  │                                              │ │
│  └──────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────┘
```

This fires ONCE per resolved dive/task. Not on every message. The constraint is: users get "feedback fatigue" if asked too often. Once per completed interaction is the ceiling.

### 3.3 Proactive Agent Feedback

When an agent posts proactively (scheduled reports, anomaly alerts), the feedback bar is the same as 3.1 but with an additional option:

```
│  [thumbs up] [thumbs down]  [correct...]  [stop these]  [why] │
```

**[stop these]**: "I don't want these proactive reports anymore." This is the strongest signal — a direct request to remove a proactive behavior. Confirmation dialog: "Stop @Growth's weekly reports? You can re-enable in Agent Settings." If confirmed, the proactive trigger is disabled in the SOUL.

### 3.4 Feedback from Multiple Interaction Points

Feedback can originate from:

| Surface | Feedback Available |
|---------|-------------------|
| Agent message in thread | thumbs up/down, correction, inline edit |
| Deep dive resolution card | usefulness rating + free text |
| Agent profile page | View all feedback history, add a note |
| Admin panel | Aggregate view, SOUL editing, trust level changes |
| Agent mention reply | Natural language correction ("@Growth, next time include cohort data") |

The last one is critical: **any reply to an agent that contains corrective language IS feedback**, even without clicking a button. The system should detect corrective intent in replies (using a lightweight classifier) and log them as episodic memory with `type: feedback_received`.

---

## 4. Feedback-to-Behavior Pipeline

### 4.1 Three Levels of Persistence

```
                    ┌─────────────────────────┐
 User gives         │  Level 1: IMMEDIATE     │
 feedback  ───────► │  (this conversation)    │  Agent adjusts right now
                    │  Lives in: thread context│
                    └──────────┬──────────────┘
                               │
                    User clicks │ "Apply always"
                    OR admin    │ promotes
                               ▼
                    ┌─────────────────────────┐
                    │  Level 2: EPISODIC      │
                    │  (remembered by agent)  │  Agent recalls in future similar tasks
                    │  Lives in: agent_episodes│
                    └──────────┬──────────────┘
                               │
                    Admin reviews│ pattern, edits SOUL
                               ▼
                    ┌─────────────────────────┐
                    │  Level 3: STRUCTURAL    │
                    │  (permanent behavior)   │  Agent always behaves this way
                    │  Lives in: agents.soul  │
                    └─────────────────────────┘
```

### 4.2 Level 1: Immediate (Context Window)

**How it works**: User gives correction in thread. The correction is a message. It's in the context window. The agent sees it on next invocation in this thread.

**No special engineering needed.** This is how ChatGPT "try again" works. The feedback is literally part of the conversation.

**Example flow**:
1. @Growth posts weekly report
2. User replies: "Include cohort retention, not just overall"
3. User: "@Growth redo the report"
4. @Growth sees the correction in thread context, includes cohort data

**Limitations**: Gone when the conversation ends. The agent makes the same mistake in a different thread.

### 4.3 Level 2: Episodic (Agent Memory)

**How it works**: Feedback creates an `agent_episodes` row. At invocation time, relevant episodes are injected into the prompt (per `AGENT-MODEL.md` Section 3 — Priority 3: Recent episodic memory).

**What gets stored**:

```yaml
# agent_episodes row
episode_type: "feedback_received"
summary: "User said: Include cohort retention breakdown in weekly reports, not just overall retention"
details:
  feedback_text: "Include cohort retention, not just overall"
  source_user_id: "uuid-charles"
  source_message_id: "uuid-msg-123"
  category: "format_correction"  # inaccurate | format_correction | style | scope | factual
  sentiment: "negative"          # positive | negative | neutral
learning: "Add cohort breakdown to weekly growth reports"
applied: false
```

**Retrieval**: When @Growth is invoked for a task related to "weekly report" or "growth metrics," the episodic memory retriever surfaces this episode. It appears in the prompt as:

```
[RECENT FEEDBACK]
- Charles (Feb 9): "Include cohort retention breakdown in weekly reports, not just overall retention"
  Learning: Add cohort breakdown to weekly growth reports
```

**When does feedback become episodic?**

| Feedback Type | Auto-creates Episode? | Details |
|---------------|----------------------|---------|
| Thumbs up | Yes | `outcome: positive`, no learning |
| Thumbs down (no correction) | Yes | `outcome: negative`, learning: null |
| Thumbs down + quick tag | Yes | `outcome: negative`, learning from tag |
| Thumbs down + written correction | Yes | `outcome: negative`, learning from correction text |
| Inline correction | Yes | Full correction stored |
| Reply with corrective intent | Yes (via classifier) | Correction extracted |
| Inline correction + "Apply always" | Yes + **also Level 3** | Dual write |
| Trust level change | Yes | Special episode type `trust_changed` |

**Episodic memory TTL (from AGENT-MODEL.md Section 7)**:
- Feedback episodes: 180 days (longer than task episodes)
- Positive feedback: 90 days (less actionable over time)
- Negative feedback with learning: 180 days
- Episodes marked `applied: true`: archived after 90 days
- Admin can mark any episode as "permanent" (no TTL)

### 4.4 Level 3: Structural (SOUL Modification)

**How it works**: An admin (or user with the "Apply always" checkbox) adds a rule to the agent's SOUL. This changes the system prompt permanently.

**Two paths to Level 3**:

**Path A: User-initiated (via "Apply always")**
1. User gives inline correction with "Apply always" checked
2. System proposes a SOUL modification:
   ```
   ┌────────────────────────────────────────────────┐
   │  Add to @Growth's behavioral rules?            │
   │                                                │
   │  Proposed rule:                                │
   │  "In weekly reports, always include cohort     │
   │   retention breakdown, not just overall        │
   │   retention numbers."                          │
   │                                                │
   │  This will be added to @Growth's SOUL under    │
   │  behavior.communication.format                 │
   │                                                │
   │  [Cancel]           [Add Rule]                 │
   └────────────────────────────────────────────────┘
   ```
3. If confirmed, the rule is written to `agents.soul`
4. An `agent_episodes` row is also created with `episode_type: constraint_added`
5. SOUL version is incremented (for audit trail)

**Path B: Admin-initiated (from dashboard)**
1. Admin reviews feedback patterns on agent profile page
2. Sees: "5 users corrected @Growth's report format this month"
3. Admin clicks "Edit SOUL" and adds the rule manually
4. Same episode + SOUL version created

**Path B is the expected steady-state.** Path A is a shortcut for power users. Most users will just thumbs-down and optionally write a correction. The admin is the one who decides if a pattern of corrections should become a permanent rule.

### 4.5 Decision: Who Decides What Level?

**The user decides Level 1 vs Level 2+3. The admin decides Level 2 vs Level 3.**

| Decision | Who | How |
|----------|-----|-----|
| "This response needs correction" | Any user | Thumbs down / correction |
| "This should be remembered" | Automatic | All explicit feedback creates an episode |
| "This should be a permanent rule" | User (via checkbox) or Admin (via dashboard) | "Apply always" or SOUL edit |
| "This episode should be promoted to SOUL" | Admin | Reviews pattern, edits SOUL |

**Why not auto-promote?** Because the system cannot reliably distinguish "three people gave the same feedback" from "three people had the same misconception." A human admin must validate before a behavioral rule becomes permanent. Voxyz's trigger system auto-promotes with `probability`, which works for content but is dangerous for behavioral rules.

---

## 5. Aggregation & Conflict Resolution

### 5.1 Pattern Detection

The system tracks feedback patterns, but **does not auto-act on them.** It surfaces patterns to the admin.

**Pattern detection query** (runs daily or on admin dashboard load):

```
For each agent in the workspace:
  Group feedback episodes by:
    - learning text (fuzzy match: cosine similarity > 0.85)
    - category (format_correction, style, scope, etc.)
    - time window (last 30 days)

  If a cluster has >= 3 episodes from >= 2 distinct users:
    Flag as "recurring pattern" on admin dashboard
```

**Admin dashboard display**:

```
┌────────────────────────────────────────────────────────┐
│  @Growth — Recurring Feedback Patterns                  │
│                                                         │
│  ⚠️ "Reports are too long" (4 feedback items, 3 users) │
│     Charles (Feb 3): "Be more concise"                 │
│     Alice (Feb 5): "Too much detail, give me headlines"│
│     Bob (Feb 7): "TL;DR please"                        │
│     Charles (Feb 9): "Still too long"                   │
│     [Resolve: Edit SOUL]  [Dismiss]                     │
│                                                         │
│  ℹ️ "Include competitor data" (2 items, 2 users)        │
│     Not enough signal yet — monitoring                  │
└────────────────────────────────────────────────────────┘
```

### 5.2 Conflicting Feedback

Real scenario: Alice says "Be more detailed." Bob says "Be more concise." Who wins?

**Resolution hierarchy**:

1. **Admin explicit rule** overrides all individual feedback
2. **More users** on one side tips the balance (3 vs 1 = majority wins)
3. **More recent feedback** takes priority over older (behavior may have already changed)
4. **Equal conflict** = escalate to admin. System does NOT pick a side.

**When conflict is detected**:

```
┌────────────────────────────────────────────────────────┐
│  ⚠️ Conflicting feedback for @Growth                    │
│                                                         │
│  "Be more detailed" — Alice (Feb 5)                    │
│  "Be more concise" — Bob (Feb 7), Charles (Feb 9)     │
│                                                         │
│  System cannot resolve. Admin decision needed.          │
│  [View all feedback]  [Edit SOUL]                       │
└────────────────────────────────────────────────────────┘
```

**Design decision: conflicting feedback is surfaced, never auto-resolved.** This is the organizational governance angle — the admin is the "manager" who decides how the agent should behave when the team disagrees.

### 5.3 Feedback by Trust Level

Feedback from users with higher workspace roles carries implicit weight:

| User Role | Feedback Weight | Rationale |
|-----------|----------------|-----------|
| Admin | 2x | Admin sets standards for the workspace |
| Member | 1x | Normal weight |
| Agent (agent-to-agent feedback, future) | 0.5x | Lower confidence, needs human validation |

This weighting is used ONLY for pattern detection sorting, not for auto-action. An admin's single thumbs-down does not automatically override a member's feedback.

---

## 6. Proactive Agent Feedback Loops

### 6.1 The Silence Problem

Agent posts a weekly report. Nobody reacts. Three possible interpretations:

1. "It's fine, I read it and moved on." (Approval)
2. "I didn't read it." (Irrelevant)
3. "It's wrong but I don't have time to correct it." (Suppressed negative feedback)

**Design decision: The system tracks read receipts separately from reactions.**

```
Agent Post Engagement:
  - 12/20 workspace members viewed (read receipt)
  - 3/12 viewers reacted (thumbs up: 2, thumbs down: 1)
  - 0 replies
  - 0 forwards

Interpretation: 60% read rate, 25% reaction rate among readers.
```

The admin dashboard shows engagement metrics for proactive agent posts. This is NOT feedback sent to the agent. It's observability for the admin.

### 6.2 Should Agents Ask "Was This Useful?"

**No. Not by default.**

"Was this useful?" is the enterprise software trap. It trains users to ignore the question (click-fatigue). Worse, it makes the agent feel needy and undermines the "employee" mental model. An employee who asks "was that useful?" after every email is annoying.

**Exception**: After a HIGH-EFFORT agent task (deep dive resolution, multi-step analysis that took > 60 seconds), a ONE-TIME unobtrusive feedback card is acceptable (see Section 3.2). Not after every message. Not after routine reports.

### 6.3 Proactive Agent Self-Assessment

Instead of asking the user, agents should self-assess based on available signals:

```yaml
# Internal self-assessment (not shown to user, stored in episodic memory)
episode_type: "self_assessment"
summary: "Weekly report posted Feb 9. Read by 12/20 users. 2 positive, 1 negative reaction. No corrections. Engagement similar to last 3 weeks."
details:
  read_rate: 0.60
  reaction_rate: 0.25
  sentiment_balance: 0.67  # (positive - negative) / total reactions
  trend: "stable"
```

If engagement drops significantly (read rate drops below 30% for 3 consecutive weeks), the system surfaces this to the admin: "@Growth's weekly reports are losing readership. Consider reviewing format or frequency."

---

## 7. Measuring Improvement

### 7.1 Core Metrics

| Metric | Calculation | What It Shows | Display |
|--------|-------------|---------------|---------|
| **Acceptance Rate** | (positive reactions + no-edit forwards) / total agent messages | % of output accepted as-is | Agent profile, admin dashboard |
| **Correction Rate** | corrections / total agent messages | How often output needs fixing | Agent profile (lower = better) |
| **Feedback Velocity** | Avg time from agent output to user reaction | How quickly humans engage | Admin dashboard |
| **Learning Incorporation** | Episodes with `applied: true` / total feedback episodes | Is the agent actually using feedback? | Agent profile |
| **Repeat Correction Rate** | Same correction given 2+ times / total corrections | Agent isn't learning | Admin dashboard (alert if > 20%) |
| **Engagement Trend** | Rolling 4-week read rate + reaction rate on proactive posts | Is proactive work valued? | Admin dashboard |

### 7.2 The "Getting Better" Visualization

On the agent profile page, a simple trend chart:

```
@Growth — Performance Trend (Last 8 Weeks)

Acceptance Rate:  62% → 68% → 71% → 74% → 78% → 81% → 79% → 83%
                  ▁▂▃▃▅▆▅█

Corrections:      12   9    8    6    4    3    5    2
                  █▆▅▄▃▂▃▁

Key Moments:
  Week 2: Charles added "include cohort retention" rule
  Week 4: Trust promoted L1 → L2
  Week 6: Alice flagged "reports too long" — SOUL updated
```

**This is the visible "agent learning" moment that builds trust.** The admin can point to the chart and say: "We gave @Growth feedback about report format in Week 2. By Week 4, acceptance rate went from 68% to 74%. It's learning."

The chart is simple on purpose. Not a dashboard with 20 metrics. One line going up (acceptance) and one going down (corrections). A human can glance at it in 3 seconds and know: is this agent getting better?

### 7.3 Performance Review Integration

From `AGENT-MODEL.md` Section 6 — Performance Reviews already define:

```typescript
interface AgentReview {
  metrics: {
    tasks_completed: number;
    tasks_failed: number;
    avg_response_quality: number;
    approvals_needed: number;
    constraints_triggered: number;
  };
  recommendation: 'promote' | 'maintain' | 'demote' | 'terminate';
}
```

**Feedback metrics feed directly into `avg_response_quality`:**

```
avg_response_quality = weighted_average(
  acceptance_rate * 0.5,         # Most important: is output accepted?
  (1 - correction_rate) * 0.3,  # How often needs fixing?
  learning_incorporation * 0.2   # Does it actually use feedback?
)
```

A review that recommends "promote" should require:
- `avg_response_quality` > 0.75 over the review period
- `repeat_correction_rate` < 0.15 (not making the same mistakes)
- Zero `never_do` violations

A review that recommends "demote" should trigger when:
- `avg_response_quality` < 0.50 over 2+ weeks
- OR `repeat_correction_rate` > 0.30
- OR any `never_do` violation

---

## 8. Data Model Additions

### 8.1 New Table: `agent_feedback`

```sql
-- Explicit feedback on agent messages
CREATE TABLE agent_feedback (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  agent_id UUID NOT NULL REFERENCES agents(id) ON DELETE CASCADE,
  message_id UUID NOT NULL REFERENCES messages(id) ON DELETE CASCADE,
  user_id UUID NOT NULL REFERENCES users(id),

  -- What kind of feedback
  feedback_type TEXT NOT NULL
    CHECK (feedback_type IN ('approve', 'reject', 'correct', 'redirect', 'instruct')),

  -- Quick categorization (optional)
  category TEXT
    CHECK (category IN ('inaccurate', 'wrong_format', 'not_useful', 'style', 'scope', 'other')),

  -- The feedback content
  correction_text TEXT,              -- free text correction
  highlighted_text TEXT,             -- which part of agent message was highlighted
  apply_always BOOLEAN DEFAULT false, -- should this become a SOUL rule?

  -- Metadata
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- One feedback per user per message (can update, not duplicate)
CREATE UNIQUE INDEX idx_agent_feedback_unique
  ON agent_feedback(message_id, user_id);

CREATE INDEX idx_agent_feedback_agent
  ON agent_feedback(agent_id, created_at DESC);
```

### 8.2 New Table: `agent_engagement`

```sql
-- Tracks engagement with agent messages (read receipts, forwards, edits)
CREATE TABLE agent_engagement (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  agent_id UUID NOT NULL REFERENCES agents(id) ON DELETE CASCADE,
  message_id UUID NOT NULL REFERENCES messages(id) ON DELETE CASCADE,
  user_id UUID NOT NULL REFERENCES users(id),

  engagement_type TEXT NOT NULL
    CHECK (engagement_type IN ('read', 'forwarded', 'edited_before_share', 'rewritten', 'ignored')),

  details JSONB,  -- e.g., edit diff for 'edited_before_share'

  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_agent_engagement_agent
  ON agent_engagement(agent_id, created_at DESC);
```

### 8.3 Extended: `agent_episodes`

The existing `agent_episodes` table (from `AGENT-MODEL.md`) already handles most of the feedback storage. The `agent_feedback` table is the raw input; `agent_episodes` is the processed output.

**Pipeline**: `agent_feedback` row inserted --> trigger/function creates corresponding `agent_episodes` row with extracted `learning`.

### 8.4 New Table: `agent_metrics_daily`

```sql
-- Pre-aggregated daily metrics for performance charts
CREATE TABLE agent_metrics_daily (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  agent_id UUID NOT NULL REFERENCES agents(id) ON DELETE CASCADE,
  date DATE NOT NULL,

  -- Counts
  messages_sent INT NOT NULL DEFAULT 0,
  feedback_positive INT NOT NULL DEFAULT 0,
  feedback_negative INT NOT NULL DEFAULT 0,
  corrections_received INT NOT NULL DEFAULT 0,

  -- Rates (pre-calculated for fast chart rendering)
  acceptance_rate DECIMAL(5,4),       -- 0.0000 to 1.0000
  correction_rate DECIMAL(5,4),
  engagement_read_rate DECIMAL(5,4),
  engagement_reaction_rate DECIMAL(5,4),

  -- Repeat corrections
  repeat_corrections INT NOT NULL DEFAULT 0,

  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

  UNIQUE (agent_id, date)
);

CREATE INDEX idx_agent_metrics_daily_agent
  ON agent_metrics_daily(agent_id, date DESC);
```

---

## 9. Day 1 Minimum

For internal dogfood launch, the minimum feedback surface:

### Must Have

1. **Thumbs up / thumbs down** on every agent message (explicit approve/reject)
2. **Reply-based correction** (just replying to an agent with a correction; agent sees it in thread context = Level 1)
3. **Episodic memory** for thumbs down + corrections (Level 2 — agent remembers across threads)
4. **Admin SOUL editing** (Level 3 — admin can add rules manually)
5. **Basic metrics** on agent profile: acceptance rate, correction count, messages sent

### Nice to Have (add during dogfood based on demand)

6. Inline correction with highlight (PR-review style)
7. "Apply always" checkbox (user-initiated Level 3 promotion)
8. Feedback categorization tags (inaccurate / wrong format / not useful)
9. Pattern detection on admin dashboard
10. Engagement tracking (read receipts, edit-before-share)
11. Performance trend chart

### Explicitly Not Day 1

12. Behavioral signal capture (user ignores / rewrites) — too complex, too easy to misinterpret
13. Conflict resolution — wait until there's actual conflicting feedback
14. Agent self-assessment — wait until proactive agents exist
15. Feedback weighting by role — flat weighting is fine for 20 users
16. Auto-promotion of episodic to SOUL — always human-initiated

---

## 10. Open Questions

1. **Corrective intent detection in replies.** When a user replies to @Growth with "The number is actually $42," is that feedback or just a message? A lightweight classifier could detect corrective intent, but false positives are annoying (user gets "Was this feedback?" prompt when they're just chatting). Alternative: only treat explicit button-clicks as feedback. Replies are just messages that happen to be in context. **Leaning toward: explicit only for Day 1. Add intent detection later if users say "I gave feedback by replying but the agent didn't learn."**

2. **Feedback on agent ACTIONS vs agent MESSAGES.** The current design covers feedback on things agents say. But V2 agents also DO things (L3+ agents execute actions: post reports, run analyses, update spreadsheets). How do you give feedback on an action? "You updated the spreadsheet wrong" is different from "your message was wrong." **Leaning toward: actions produce messages that describe what happened. Feedback targets those messages. Actions themselves are audited, not feedbacked.**

3. **Cross-agent learning.** If @Growth gets feedback "be more concise," should @Coder also learn this? Or is it agent-specific? **Leaning toward: agent-specific. Different agents have different communication styles on purpose. Workspace-wide preferences belong in a workspace settings doc, not in individual agent feedback.**

4. **Feedback fatigue monitoring.** If we show thumbs up/down on every agent message, will users just ignore it (like cookie consent banners)? Should we measure feedback response rate and hide the UI if it drops below a threshold? **Leaning toward: always show on hover (non-intrusive), never force feedback. If users stop giving feedback, that's fine — the metrics from what they DO give are still useful.**

5. **Feedback on deep dive resolution quality.** The MVP design already has thumbs up/down on resolution summaries (MVP-DESIGN-SYNTHESIS.md Section 2.4: "Resolution summary approval > 75%"). This feedback naturally feeds into the same pipeline. But who does it feedback to — @Vibe (who helped with the dive) or the resolution system? **Leaning toward: resolution quality feedback goes to the workspace-level config (resolution prompt quality), not to the individual agent.**

---

*Next: TRUST-SYSTEM.md -- How does L1-L4 work mechanically? (Referenced from AGENT-MODEL.md)*
