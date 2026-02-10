# Agent in Conversation

> V2 Design Doc | Created: 2026-02-09
> Status: Draft
> Depends on: V2-VISION.md, AGENT-MODEL.md, AGENT-ORCHESTRATION-REFERENCE.md
> Scope: Layer 1 — How agents participate in conversations within the shared workspace

---

## 1. Design Principles

**1. Agents are quiet by default, loud when it matters.**
An agent that constantly interjects is worse than no agent. The baseline is silence. Agents speak when spoken to, when something they're responsible for happens, or when something is genuinely wrong. Proactivity is earned through trust level, not granted by default. This maps directly to the L1-L4 trust system: an L1 agent never speaks unsolicited; an L3 agent posts its Monday report without asking.

**2. Messages are the universal interface.**
Every agent action manifests as a message in a channel or thread. No hidden dashboards, no separate "agent workspace." If an agent did something, there's a message trail. This follows Yangyi's core insight: IM-based async messaging is the foundation for all human-agent coordination. The audit log supplements but doesn't replace the conversation trail.

**3. Human tempo, not machine tempo.**
Agents can generate 10,000 words in 3 seconds. Humans can't read 10,000 words in 3 seconds. Agent output must respect the reader's bandwidth. This means: structured output by default, progressive disclosure always, and a hard norm that agent messages should be scannable in under 10 seconds. If the output needs more, it gets folded.

**4. The conversation is the control surface.**
You shouldn't need a settings panel to tell an agent what to do. @mention is invocation. Reply is feedback. Reaction is approval/rejection. Thread is context boundary. The conversational affordances that already exist for human-to-human communication should also work for human-to-agent communication. The settings panel exists for structural changes (trust level, SOUL edits, tool grants) -- not for day-to-day interaction.

**5. Agents don't talk to each other in front of humans unless asked.**
Two agents having a conversation in a channel is bizarre and noisy. Agent-to-agent coordination happens in the orchestration layer (Proposal/Mission/Steps), not in the message stream. The one exception: when a human explicitly asks agents to collaborate ("@Growth and @Coder, figure out why signups dropped and whether it's a bug or a marketing issue"). Even then, the output should be consolidated, not a ping-pong thread.

---

## 2. Invocation Model

### 2.1 Three Modes of Activation

| Mode | Trigger | Trust Level Required | Example |
|------|---------|---------------------|---------|
| **Reactive** | @mention in a message | Any (L1+) | "@Vibe what's our churn rate this month?" |
| **Proactive** | SOUL-defined triggers (schedule, event, threshold) | L3+ | @Growth posts weekly report every Monday 9am |
| **System** | Platform events (new PR, metric alert, member joined) | L2+ (configured by admin) | @Coder auto-reviews new PRs in #engineering |

### 2.2 Reactive: @mention

This is the primary invocation mode and the simplest to understand.

**Mechanics:**
1. User types `@AgentSlug` anywhere in a message
2. System parses the mention, resolves to an `agents` record
3. A task is created: `task_type = 'message_response'`
4. Agent processes the task using assembled context (SOUL + thread history + memory)
5. Response posted as a message with `author_type = 'agent'`

**Context boundaries:**
- In a channel message: agent sees the last N messages in that channel (N = configurable, default 50)
- In a thread: agent sees the full thread (up to context window budget)
- In a deep dive: agent sees the parent message + all dive messages (NOT the full parent thread -- the dive is its own context)

**Multiple agents in one message:**
"@Growth what's our CAC trend? @Coder is the tracking pixel deployed correctly?" creates two independent tasks. Responses arrive in whatever order the agents finish. No coordination between them -- they answer their respective questions independently. This is the right default because most multi-mention messages contain independent questions.

**Mention without a question:**
"@Growth FYI we changed the attribution model yesterday" -- the agent acknowledges with a brief response and records this as episodic memory. Not every mention requires a substantive answer.

### 2.3 Proactive: SOUL-Defined Triggers

Agents at L3+ can be configured with proactive behaviors in their SOUL:

```yaml
behavior:
  proactive:
    - trigger: "Monday 9am UTC"
      action: "Generate and post weekly growth report to #growth"
    - trigger: "Any metric drops >15% week-over-week"
      action: "Alert #growth channel immediately with analysis"
```

**How proactive messages work:**

1. The orchestration layer evaluates triggers on a heartbeat (per Voxyz pattern: `/api/ops/heartbeat` every 5 minutes)
2. A matching trigger creates a Proposal
3. For L3+ agents, the proposal auto-approves (per trust level)
4. The agent executes and posts the result as a regular message in the designated channel
5. The message includes a subtle "proactive" indicator so humans know it wasn't triggered by a mention

**Anti-spam guardrails:**

- Each proactive trigger has a `cooldown` (minimum interval between firings)
- Each agent has a daily message budget (default: 20 proactive messages/day)
- If budget exhausted, agent drops to reactive-only until next day
- Admin can override budgets per agent

**The key design tension:** L3+ proactive agents are powerful but can be noisy. The solution is NOT to make them less proactive -- it's to make their proactive output high-signal. This is enforced through:
1. SOUL constraints (quality requirements in `behavior.communication`)
2. Feedback loop (humans react thumbs-down, agent learns to calibrate)
3. Hard budget (can't spam even if misconfigured)

### 2.4 System: Platform Event Triggers

Distinct from SOUL-defined proactive behaviors, these are workspace-level integrations:

```yaml
# Workspace-level trigger rules (ops_trigger_rules table)
- name: "PR Auto-Review"
  condition: { event_type: "github.pull_request.opened", repo: "openvibe/*" }
  agent: "@coder"
  channel: "#engineering"
  trust_required: L2
```

System triggers are configured by workspace admins, not by the agent's SOUL. The agent receives a task with event context and responds in the designated channel. This separation matters: the SOUL defines what the agent *wants* to do; system triggers define what the *organization* needs the agent to do.

### 2.5 What About Auto-Triggering by Content?

**Decision: No auto-trigger by content analysis in V2.**

The temptation is: "if someone mentions a metric in #general, @Growth should automatically chime in with the latest numbers." This fails for three reasons:

1. **False positives are worse than false negatives.** An agent that responds when you didn't want it is more annoying than an agent that stays quiet when you might have wanted it. 用户可以忍受手动 @mention, 但忍受不了被打断.
2. **Ambiguity.** "Our numbers look good this quarter" -- should @Growth respond? With what? The context is too thin for useful output.
3. **Cost.** Content analysis on every message means an LLM call per message for classification. At scale, this is the single most expensive thing the system could do.

The right path to ambient intelligence is through the drift nudge model from V1: the system can *suggest* that a mention might be useful ("This looks like a metrics question -- ask @Growth?") without the agent actually responding. This is a UI affordance, not an agent behavior. Deferred to Phase 5.

---

## 3. Message Types & Formats

### 3.1 The Universal Structure

Every agent message follows the same outer structure:

```
┌─────────────────────────────────────────────────┐
│ [Agent Avatar] Agent Name [Trust Badge] [Timestamp]
│
│ [Message Content — varies by type]
│
│ [Action Bar: thumbs up/down | "Why?" | Copy | ...]
└─────────────────────────────────────────────────┘
```

The content varies. The chrome doesn't. This consistency is critical -- humans should be able to process agent messages with the same muscle memory as human messages.

### 3.2 Five Message Types

| Type | When Used | Length Target | Example |
|------|-----------|---------------|---------|
| **Quick Reply** | Simple questions, acknowledgments, FYIs | 1-3 sentences | "Current CAC is $42, up 8% from last month." |
| **Analysis** | Data questions, comparisons, research | 1 paragraph + structured data | Metric breakdown with table |
| **Report** | Scheduled reports, comprehensive reviews | Headline + bullets + expandable full | Weekly growth report |
| **Action Request** | Agent needs approval or human input | Question + options + context | "Should I proceed with Option A or B?" |
| **Status Update** | Long-running task progress | 1-2 lines with progress indicator | "Analyzing 3 months of data... 67% complete" |

The agent doesn't explicitly choose a type. The system infers it from the output length and structure, then applies the right rendering. Short responses (< 280 chars) render inline. Medium responses (280-1000 chars) render fully. Long responses (> 1000 chars) get progressive disclosure.

### 3.3 Progressive Disclosure (Mandatory for Long Output)

Any agent output > 1000 characters renders as:

```
┌─────────────────────────────────────────────────┐
│ [Avatar] @Growth                    Monday 9:00am
│
│ ■ Weekly Growth Report: Feb 3-9                  ← HEADLINE (always visible)
│
│ Key findings:                                    ← SUMMARY (always visible)
│ - DAU up 12% to 847 (driven by onboarding fix)
│ - CAC increased 8% to $42 (needs investigation)
│ - Trial-to-paid conversion at 23% (target: 25%)
│
│ ▸ View full analysis (2,847 words)              ← EXPAND (click to reveal)
│
│ [thumbs up] [thumbs down] [Why?]
└─────────────────────────────────────────────────┘
```

The headline and summary are generated by the agent as part of its response (not post-processed by a separate model). The SOUL's `behavior.communication.format` instructs the agent to structure its output this way. Specifically, for any response that would exceed ~500 words, the agent is instructed to produce:

```json
{
  "headline": "One-line summary (< 100 chars)",
  "key_points": ["Bullet 1", "Bullet 2", "Bullet 3"],
  "full_content": "The complete analysis in markdown...",
  "confidence": "high" | "medium" | "low",
  "sources": ["List of data sources used"]
}
```

If the agent returns unstructured text (e.g., from an older model or a poorly configured SOUL), the system falls back to a Haiku call that extracts headline + bullets. This is the same V1 approach but positioned as a fallback, not the primary path.

### 3.4 Structured Data Blocks

Agent messages can contain rich blocks within their content:

**Table Block:**
```
| Metric | This Week | Last Week | Change |
|--------|-----------|-----------|--------|
| DAU    | 847       | 756       | +12%   |
| CAC    | $42       | $39       | +8%    |
```

**Code Block:**
```typescript
// The fix for the tracking pixel
window.analytics.track('signup', { source: utm_source });
```

**Action Buttons:**
```
┌──────────────────────────────────────┐
│ I've drafted two options for the     │
│ pricing page copy. Which should I    │
│ proceed with?                        │
│                                      │
│ [Option A: Value-focused]            │
│ [Option B: Feature-focused]          │
│ [Neither — let me rethink]           │
└──────────────────────────────────────┘
```

Action buttons are only available to L2+ agents (L1 agents can suggest but can't present actionable options). Clicking a button creates a new message from the user (visible to everyone) and triggers a follow-up task for the agent. This keeps everything in the message trail -- no hidden state transitions.

### 3.5 Visual Distinction: Agent vs Human

| Element | Human Message | Agent Message |
|---------|--------------|---------------|
| Avatar | User photo | Agent avatar (designed, not generic robot) |
| Name badge | None | Small "AI" chip + trust level on hover |
| Background | Default | Subtle tint (2-3% opacity shift, NOT a bold color) |
| Border | None | Thin left accent line (agent's assigned color) |
| Font | Default | Same (agents should NOT look like "system messages") |
| Actions | Reply, React | Reply, React, Thumbs up/down, "Why?" |

**The "Why?" link** is unique to agent messages. Clicking it expands an inline section showing:
- The relevant SOUL principles that guided this response
- Key context the agent used (which messages it read, which memories it retrieved)
- Confidence level and any caveats

This is the transparency mechanism from AGENT-MODEL.md in action. It's not a debugging tool -- it's a trust-building tool. When a manager can see *why* @Growth chose to highlight CAC over retention, they calibrate their trust in the agent's judgment.

---

## 4. Long-Running Tasks

### 4.1 The Problem

Some agent tasks take > 30 seconds: analyzing 3 months of data, generating a comprehensive report, reviewing a large PR. The user needs to know the agent is working, see progress, and have the ability to intervene.

### 4.2 Task Lifecycle (Voxyz-Influenced)

```
User @mentions agent with a complex request
    │
    ▼
[Proposal Created]  ← Agent estimates scope: quick (<30s) or mission (>30s)
    │
    ├── Quick? → Execute immediately, post response (standard flow)
    │
    └── Mission? → Agent posts acknowledgment + plan
            │
            ▼
        ┌─────────────────────────────────────────┐
        │ @Growth                                   │
        │                                           │
        │ I'll analyze Q4 growth data for you.      │
        │ This will take a few minutes.             │
        │                                           │
        │ Plan:                                     │
        │ 1. Pull Mixpanel data (Oct-Dec)          │
        │ 2. Calculate cohort metrics              │
        │ 3. Compare against benchmarks            │
        │ 4. Generate report                       │
        │                                           │
        │ ━━━━━━━━━━━━━━━━━ 0%                     │
        │ [Cancel]                                  │
        └─────────────────────────────────────────┘
            │
            ▼
        [Mission + Steps created in orchestration layer]
        [Worker picks up steps sequentially]
            │
            ├── Step 1 complete → progress bar updates (25%)
            ├── Step 2 complete → progress bar updates (50%)
            │       │
            │       └── (User can see intermediate output if they click)
            ├── Step 3 complete → progress bar updates (75%)
            └── Step 4 complete → final output replaces progress message
```

### 4.3 Progress Visibility

The progress message is a **live-updating message** (via Supabase Realtime on the `tasks` table). As each step completes, the message updates in-place:

```
@Growth
Analyzing Q4 growth data...

 Step 1/4: Pull Mixpanel data ........... done
 Step 2/4: Calculate cohort metrics ..... done
 Step 3/4: Compare against benchmarks ... running
 Step 4/4: Generate report .............. waiting

━━━━━━━━━━━━━━━━━ 62%

[View intermediate results] [Cancel]
```

**"View intermediate results"** expands to show what the agent has produced so far. This is useful when you realize midway that the agent is going in the wrong direction -- you can cancel and redirect before it wastes tokens on Step 4.

### 4.4 Cancellation and Redirection

**Cancel:** User clicks [Cancel]. The running step is terminated. The agent posts a brief note: "Cancelled at Step 3. Partial results available above." Remaining steps are marked `skipped`. The mission is marked `cancelled`. No new tasks spawn from this mission.

**Redirect:** User replies to the progress message: "Actually, focus on retention metrics, not growth." The agent:
1. Pauses the current mission
2. Posts: "Got it. Adjusting focus to retention metrics. Restarting analysis."
3. Creates a new mission with adjusted steps
4. The old mission is marked `superseded`

Redirect only works if the agent is L2+ (has enough trust to interpret a redirection without human re-confirmation of the new plan). For L1 agents, the user must cancel and re-invoke with a new request.

### 4.5 Timeout and Self-Healing

Per Voxyz's self-healing pattern:
- Steps running for > 30 minutes with no progress update: auto-marked `failed`
- Failed steps trigger a diagnostic: the agent (or a system diagnostic agent) posts an error message in the thread
- Stale missions are cleaned up on heartbeat

### 4.6 When Does Quick vs Mission Apply?

The agent decides based on the request complexity:

| Signal | Quick Task (< 30s) | Mission (> 30s) |
|--------|-------------------|-----------------|
| Simple question | "What's our DAU?" | - |
| Data lookup | "What was churn last month?" | - |
| Analysis request | - | "Analyze Q4 growth trends" |
| Multi-step request | - | "Review this PR and suggest fixes" |
| Report generation | - | "Write the weekly growth report" |
| Comparison | "DAU this week vs last" | "Compare our metrics against 3 competitors" |

The heuristic is in the SOUL's `capabilities.skills`: each skill has a `typical_duration` field. If the matching skill's duration exceeds 30 seconds, it's a mission. The agent can also escalate to mission mid-execution if a "quick" task turns out to be more complex than expected -- it posts the acknowledgment/plan message and transitions to mission mode.

---

## 5. Multi-Turn Collaboration

### 5.1 Thread as Context Boundary

Every thread (and every deep dive) is a context boundary. When you reply to an agent's message within a thread, the agent sees the full thread history as working memory. This is the "multi-turn collaboration" model:

```
Thread: "Q1 planning discussion"
│
├── Alice: "@Growth what should our Q1 targets be?"
│
├── @Growth: "Based on current trajectory, I'd suggest:
│             - DAU target: 1,200 (15% growth from 1,043)
│             - CAC target: <$38 (8% reduction)
│             - Conversion target: 27% (from 23%)
│             Here's my reasoning..."
│
├── Alice: "The DAU target seems conservative. We're launching
│           the referral program in Jan."
│
├── @Growth: "Good point. With the referral program, historical
│             data from similar launches suggests 20-30% boost.
│             Revised DAU target: 1,400 (34% growth).
│             Want me to model the referral impact in detail?"
│
├── Alice: "Yes, do a deep dive on referral program impact."
│
└── [Deep Dive created: "Referral program growth modeling"]
```

Each message from Alice refines the context. The agent's second response incorporates both the original question AND Alice's correction. This is natural -- it works the same way a human conversation works.

### 5.2 Deep Dives (Formerly "Forks")

Deep dives are the multi-turn collaboration mode on steroids. From V1's core reframe: one human + AI, thinking partner, not summarizer.

**In V2, deep dives are the primary place agents do extended work.** The channel is for quick exchanges. The thread is for focused discussion. The deep dive is where the real thinking happens.

**Deep dive context assembly:**
1. The parent message (what sparked the dive)
2. All messages within the dive (the human + AI conversation)
3. The agent's SOUL (identity, principles, constraints)
4. Relevant episodic memory (what the agent has learned from past dives)
5. Relevant semantic memory from knowledge base (team context)

**NOT included:** The full parent thread. The dive is its own context. If the human needs the agent to know something from the parent thread, they paste or summarize it. This is a deliberate constraint -- context pollution from the parent thread would dilute the dive's focus.

**The "Publish" moment:**
When the human is satisfied with the dive's conclusion, they click [Publish]. The agent generates:
- Headline (one line)
- Key findings (3-5 bullets)
- Full analysis (expandable)

This is posted to the parent thread as a structured "Dive Result" message. Other team members see the compressed output. If they want to go deeper, they can start their own deep dive on the result.

### 5.3 When Does a Thread Produce a "Result"?

Not every thread interaction produces a formal result. The mapping:

| Interaction | Produces Formal Result? | Mechanism |
|-------------|------------------------|-----------|
| Quick @mention Q&A | No | Agent response is the result |
| Multi-turn thread discussion | No | The thread IS the record |
| Deep dive | Yes, when published | Dive Result posted to parent thread |
| Long-running mission | Yes, when complete | Final output replaces progress message |
| Proactive report | Yes, always | Structured report message |

The key distinction: quick exchanges are ephemeral-feeling (even though they're persisted). Deep dives and missions produce artifact-quality output that is meant to be referenced later.

### 5.4 Context Accumulation Within a Thread

As a thread grows, the agent can't fit everything in context. The strategy:

**Under 50 messages:** Full thread in context. No summarization.

**50-200 messages:** Sliding window. Last 50 messages fully in context. Earlier messages summarized by a lightweight model (Haiku) into a "thread summary" that's prepended to context. Summary is cached and regenerated every 20 new messages.

**Over 200 messages:** Thread summary + last 30 messages + any messages the user explicitly references (via reply/quote). Semantic search over older messages to include the 5 most relevant to the current question.

This isn't visible to the user. The agent just "remembers" what was discussed, with graceful degradation for very long threads.

---

## 6. Multi-Agent Dynamics

### 6.1 Core Rule: Agents Don't Initiate Conversations With Each Other in Channels

This is the most important rule. Without it, two agents can create an infinite loop:

```
BAD:
@Growth: "Signups dropped 15% this week."
@Coder: "I'll check if the tracking pixel is broken."
@Growth: "Good idea. Let me know what you find."
@Coder: "Found a bug in the signup event. Fixing now."
@Growth: "Great. I'll recalculate the metrics after the fix."
@Coder: "Fix deployed. Can you verify?"
@Growth: "Verified. Numbers are correcting. Let me run a full analysis..."
[... continues forever, costs $50 in tokens, floods the channel]
```

**The rule:** An agent only responds when:
1. A human @mentions it
2. A proactive trigger fires (SOUL-defined or system-defined)
3. The orchestration layer assigns it a task (internal, not visible in conversation)

An agent does NOT respond to another agent's message in a conversation. Period. Even if another agent @mentions it. The @mention from another agent is logged but does not trigger a response.

### 6.2 When Humans Want Multi-Agent Collaboration

If a human wants two agents to work together, they have two options:

**Option A: Sequential invocation (simple)**
```
Alice: "@Growth what's happening with our signups?"
@Growth: "Signups dropped 15%. Possible causes: tracking issue,
          ad spend reduction, or seasonal dip."
Alice: "@Coder can you check if the tracking is working correctly?"
@Coder: "Checking... The signup event pixel has a bug introduced in PR #142.
          It's firing on page load instead of form submit."
Alice: "@Growth recalculate signups accounting for the tracking bug."
@Growth: "Recalculated: actual signups are flat, not down 15%. The drop
          was entirely due to the tracking bug."
```

The human mediates. This is slower but controlled. No runaway conversations.

**Option B: Orchestrated collaboration (advanced, L3+ agents only)**
```
Alice: "@Growth and @Coder, investigate why signups dropped and give me a joint report."
```

This triggers a special multi-agent task:
1. System creates a Mission with the request
2. System creates a private orchestration thread (not visible in the channel) where agents coordinate
3. Each agent works on its part (Growth analyzes data, Coder checks technical systems)
4. When both are done, the system consolidates into a single response posted by the initiating agent (Growth, as the first mentioned):

```
@Growth [with @Coder]
Joint Investigation: Signup Drop

Root Cause: Tracking bug (technical), not actual decline.
- @Coder found: signup pixel bug in PR #142 (fires on load, not submit)
- @Growth found: correcting for bug, actual signups are flat week-over-week
- Ad spend and seasonal patterns are normal

Recommendation: Fix the pixel, then re-evaluate in 1 week.

[View investigation details]
```

The "[with @Coder]" badge indicates this was a collaborative output. Expanding "View investigation details" shows each agent's individual analysis.

**Implementation note:** The private orchestration thread uses the Voxyz Proposal/Mission/Steps model internally. The agents don't "talk" to each other -- the orchestration layer sequences their work and merges outputs. This is critical: there is no agent-to-agent message passing in the conversation layer.

### 6.3 Multiple Agents in the Same Channel

Multiple agents can be active in the same channel. They don't interfere with each other because:

1. Each agent only responds to its own @mentions
2. Proactive triggers target specific channels, not "wherever another agent is active"
3. The orchestration layer deduplicates -- if two agents would both respond to the same trigger (e.g., metric alert), only the one with the more specific SOUL match responds

**Channel presence indicator:**
The channel header shows which agents are "active" in this channel (have been invoked in the last 7 days or have proactive triggers targeting this channel):

```
#growth  |  Active agents: @Growth, @Vibe
```

This helps users know who to @mention without checking a settings page.

### 6.4 Agent-to-Agent Rules Summary

| Scenario | Behavior |
|----------|----------|
| Agent A posts in channel | Agent B does NOT respond |
| Agent A @mentions Agent B | Logged, does NOT trigger response |
| Human asks two agents to collaborate | Orchestrated via Mission, consolidated output |
| Two agents have proactive triggers for same event | System picks the more specific one |
| Agent needs data from another agent's domain | Orchestration layer routes the request internally |
| Agent disagrees with another agent's output | Does NOT post a rebuttal. Logs disagreement in episodic memory. Human can ask for it. |

---

## 7. UX Details

### 7.1 Agent "Thinking" Indicator

When an agent is processing a task, the thread shows:

```
@Growth is thinking...
```

This is a ephemeral indicator (not a message), similar to typing indicators in chat apps. It appears immediately when the task is created and disappears when the response is posted.

For missions (long-running tasks), the indicator transitions to the progress message after 5 seconds:
- 0-5 seconds: "@Growth is thinking..."
- >5 seconds: Progress message with plan and progress bar (see Section 4)

### 7.2 Confidence and Reasoning

**Confidence indicator:** Not shown inline (it would clutter every message). Instead:
- The agent's response text naturally hedges when confidence is low ("Based on limited data..." or "I'm not certain, but...")
- The "Why?" expansion shows explicit confidence: "Confidence: Medium. Data is from 2 weeks ago and may not reflect recent changes."

**Reasoning chain:** Available via "Why?" on every agent message. Shows:
1. Which SOUL principles were applied
2. Key context used (messages read, memories retrieved)
3. Alternatives considered (if applicable)
4. Confidence assessment

This is NOT a chain-of-thought dump. It's a curated explanation designed for a manager reviewing an employee's work. The system assembles it from the agent's structured output, not from raw LLM thinking tokens.

### 7.3 Feedback Mechanism

Every agent message has:

| Action | Meaning | What Happens |
|--------|---------|-------------|
| Thumbs up | Good response | Recorded as positive episodic memory. Reinforces behavior. |
| Thumbs down | Bad response | Recorded as negative episodic memory. Prompts for optional feedback text. |
| Reply | Continuation | Adds to thread context. Agent uses this for multi-turn. |
| "Why?" | Explain yourself | Expands reasoning panel (no new LLM call -- pre-computed). |

**Thumbs down flow:**
1. User clicks thumbs down
2. Small prompt appears: "What was wrong? (optional)" with a text field
3. If user provides feedback, it becomes an episodic memory entry:
   ```yaml
   episode_type: feedback_received
   summary: "User said: 'The churn numbers were wrong -- you used monthly, not annual.'"
   learning: "Clarify churn calculation basis (monthly vs annual) before presenting."
   ```
4. This learning is injected into future invocations as Priority 3 context

The feedback loop is the mechanism by which agents improve within a workspace. It's not fine-tuning the model -- it's accumulating behavioral guidance in episodic memory that shapes future prompt assembly.

### 7.4 Mobile Considerations

Agent messages tend to be longer than human messages. On mobile:

1. **Progressive disclosure is even more aggressive.** On screens < 768px:
   - Only headline visible by default (not headline + bullets)
   - One tap to see bullets
   - Second tap to see full content
   - Tables render as stacked key-value pairs, not horizontal tables

2. **Action buttons stack vertically.** On desktop, options can be side-by-side. On mobile, they stack.

3. **"Why?" panel is a bottom sheet,** not inline expansion. Inline expansion on mobile pushes content around in disorienting ways.

4. **Progress indicators are simplified.** Instead of the multi-step progress view, mobile shows: "@Growth is working on your request... (2 of 4 steps complete)". One line, not a table.

5. **Agent messages have a "Read more in desktop" link** for content that's genuinely too complex for mobile (large tables, code blocks with context). This is a pragmatic concession: some agent output is desktop-native.

### 7.5 Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `@` then type | Agent mention autocomplete (same as user mention) |
| `Cmd+Shift+D` | Start deep dive from selected message |
| `Cmd+Enter` | Send message (same as human messages) |
| `Esc` | Cancel long-running task (when progress message is focused) |

Agent invocation should feel exactly like mentioning a teammate. No special mode, no command palette, no slash commands. `@` is the universal invocation interface.

---

## 8. Open Questions

### Needs User Input

1. **Proactive message frequency.** What's the right daily budget for L3+ agents? 20/day per agent feels right for a 20-person team, but could be too noisy or too quiet depending on the agent's role. Should this be per-agent configurable from day one, or start with a global default?

2. **Deep dive initiation.** In V1, only humans could create deep dives. In V2, should L3+ agents be able to initiate a deep dive when they encounter a question that needs more exploration? E.g., "@Growth is preparing the weekly report and discovers an anomaly -- should it be able to start a dive and then publish the findings?" The risk is unsupervised agent activity; the benefit is faster anomaly investigation.

3. **Cross-channel agent memory.** When @Growth learns something in #growth, should it remember that context when mentioned in #general? Currently, episodic memory is per-agent (not per-channel), so yes. But this could lead to context leakage -- an agent mentioning confidential #leadership data in #general. Should memory have channel-level access control?

4. **Agent response editing.** Can a human edit an agent's message after it's posted? Use case: the agent's analysis is 90% right but has a wrong number. Should the human be able to fix it in place (with an "edited by [human]" indicator), or must they reply with a correction? Editing preserves clean thread flow; replying preserves audit integrity.

5. **Notification rules for agent messages.** Proactive agent messages: should they trigger notifications for channel members? A Monday morning report notification is useful. A routine status update notification is annoying. Proposal: proactive messages are silent by default (visible when you open the channel, but no push/badge). Mentions of specific humans within agent messages DO trigger notifications. 需要 dogfood 验证.

### Needs Technical Investigation

6. **Progress message live updates.** Supabase Realtime on the `tasks` table can broadcast step completions. But the progress message itself is in the `messages` table. Option A: update the message content on each step change (triggers Realtime update on messages). Option B: a separate real-time subscription on the task, with frontend compositing the progress view. Option A is simpler; Option B is more efficient.

7. **Multi-agent orchestration thread.** The "private orchestration thread" for multi-agent collaboration: is this a real thread in the `threads` table (with `visibility = 'system'`), or is it purely in the orchestration layer (Mission + Steps, no messages)? If it's a real thread, the "View investigation details" expansion can show the actual messages. If it's orchestration-only, the expansion shows a rendered summary. 前者更透明, 后者更简单.

8. **SOUL-generated vs post-processed progressive disclosure.** Section 3.3 proposes the agent itself generates structured output (headline + bullets + full). But different models handle this differently. Claude Sonnet 4.5 reliably produces structured JSON; smaller/older models may not. Do we enforce structured output via tool_use (guaranteed JSON) or allow free-form with Haiku post-processing as fallback? Tool_use is more reliable but constrains the agent's output format.

---

*Next: TRUST-SYSTEM.md -- How does L1-L4 mechanically gate agent actions in conversations?*
