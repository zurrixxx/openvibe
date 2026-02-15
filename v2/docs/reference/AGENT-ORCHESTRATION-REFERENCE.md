# Agent Orchestration Reference

> 综合学习自两篇 OpenClaw 实践文章，为 OpenVibe 提供架构参考

**Sources:**
- [@Voxyz_ai - "I Built an AI Company with OpenClaw + Vercel + Supabase"](https://x.com/voxyz_ai/status/2019914775061270747) (842K views, Feb 6 2026)
- [@KSimback - "My Complete Guide to Managing OpenClaw Agent Teams"](https://x.com/ksimback/status/2019804584273657884) (209K views, Feb 6 2026)

---

## Part 1: Technical Architecture (Voxyz)

### Core Insight

> "Between 'agents can produce output' and 'agents can run things end-to-end,' there's a full **execute → feedback → re-trigger** loop missing."

### The Closed Loop

```
Agent proposes an idea (Proposal)
        ↓
Auto-approval check (Auto-Approve)
        ↓
Create mission + steps (Mission + Steps)
        ↓
Worker claims and executes (Worker)
        ↓
Emit event (Event)
        ↓
Trigger new reactions (Trigger / Reaction)
        ↓
Back to step one
```

### Three-Layer Architecture

| Layer | Responsibility | Tech |
|-------|----------------|------|
| **OpenClaw (VPS)** | Think + Execute (brain + hands) | Claude + cron |
| **Vercel** | Approve + Monitor (control plane) | Next.js API routes |
| **Supabase** | All state (shared cortex) | Postgres + Realtime |

### Database Schema (Supabase)

```sql
-- Core tables needed for closed-loop agent orchestration

-- Proposals: where ideas start
CREATE TABLE ops_mission_proposals (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  agent_id TEXT NOT NULL,
  title TEXT NOT NULL,
  description TEXT,
  source TEXT NOT NULL, -- 'api' | 'trigger' | 'reaction'
  status TEXT NOT NULL DEFAULT 'pending', -- pending | accepted | rejected
  rejection_reason TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  processed_at TIMESTAMPTZ
);

-- Missions: approved proposals become missions
CREATE TABLE ops_missions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  proposal_id UUID REFERENCES ops_mission_proposals(id),
  title TEXT NOT NULL,
  status TEXT NOT NULL DEFAULT 'pending', -- pending | running | succeeded | failed
  created_at TIMESTAMPTZ DEFAULT NOW(),
  started_at TIMESTAMPTZ,
  completed_at TIMESTAMPTZ
);

-- Steps: missions break into executable steps
CREATE TABLE ops_mission_steps (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  mission_id UUID REFERENCES ops_missions(id),
  kind TEXT NOT NULL, -- 'draft_tweet' | 'crawl' | 'analyze' | 'write_content' | 'post_tweet' | 'deploy'
  status TEXT NOT NULL DEFAULT 'queued', -- queued | running | succeeded | failed
  input JSONB,
  output JSONB,
  last_error TEXT,
  reserved_at TIMESTAMPTZ,
  completed_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Events: audit trail of all agent actions
CREATE TABLE ops_agent_events (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  agent_id TEXT NOT NULL,
  event_type TEXT NOT NULL,
  payload JSONB,
  tags TEXT[],
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Policy: configuration as data (not code)
CREATE TABLE ops_policy (
  key TEXT PRIMARY KEY,
  value JSONB NOT NULL,
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Trigger rules: conditions that create proposals
CREATE TABLE ops_trigger_rules (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name TEXT NOT NULL,
  condition JSONB NOT NULL, -- e.g., {"event_type": "tweet_posted", "engagement_rate_gt": 0.05}
  proposal_template JSONB NOT NULL,
  cooldown_minutes INT DEFAULT 120,
  last_fired_at TIMESTAMPTZ,
  enabled BOOLEAN DEFAULT true
);

-- Reactions: agent-to-agent spontaneous interactions
CREATE TABLE ops_agent_reactions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  source_event_id UUID REFERENCES ops_agent_events(id),
  target_agent TEXT NOT NULL,
  reaction_type TEXT NOT NULL,
  status TEXT NOT NULL DEFAULT 'pending', -- pending | processed | skipped
  created_at TIMESTAMPTZ DEFAULT NOW(),
  processed_at TIMESTAMPTZ
);

-- Action runs: execution logs
CREATE TABLE ops_action_runs (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  step_id UUID REFERENCES ops_mission_steps(id),
  started_at TIMESTAMPTZ DEFAULT NOW(),
  completed_at TIMESTAMPTZ,
  success BOOLEAN,
  output JSONB,
  error TEXT
);
```

### Policy Examples

```json
// ops_policy: auto_approve
{
  "enabled": true,
  "allowed_step_kinds": ["draft_tweet", "crawl", "analyze", "write_content"]
}

// ops_policy: x_daily_quota
{
  "limit": 8
}

// ops_policy: worker_policy
{
  "enabled": false  // VPS only, Vercel doesn't execute
}

// ops_policy: reaction_matrix
{
  "patterns": [
    {
      "source": "twitter-alt",
      "tags": ["tweet", "posted"],
      "target": "growth",
      "type": "analyze",
      "probability": 0.3,
      "cooldown": 120
    },
    {
      "source": "*",
      "tags": ["mission:failed"],
      "target": "brain",
      "type": "diagnose",
      "probability": 1.0,
      "cooldown": 60
    }
  ]
}
```

### Three Pitfalls & Fixes

#### Pitfall 1: Two Places Fighting Over Work

**Problem:** VPS and Vercel both trying to claim and execute the same tasks.

**Fix:** Single executor. VPS is the sole executor. Vercel only runs the control plane.

```typescript
// Heartbeat (Vercel) does only 4 things:
const triggerResult = await evaluateTriggers(sb, 4_000);
const reactionResult = await processReactionQueue(sb, 3_000);
const learningResult = await promoteInsights(sb);
const staleResult = await recoverStaleSteps(sb);
// NO runMissionWorker here!
```

#### Pitfall 2: Triggered But Nobody Picked It Up

**Problem:** Triggers create proposals, but proposals never become missions.

**Fix:** Single entry point for all proposal creation.

```typescript
// proposal-service.ts — the single entry point
export async function createProposalAndMaybeAutoApprove(
  sb: SupabaseClient,
  input: ProposalServiceInput, // includes source: 'api' | 'trigger' | 'reaction'
): Promise<ProposalServiceResult> {
  // 1. Check daily limit
  // 2. Check Cap Gates
  // 3. Insert proposal
  // 4. Emit event
  // 5. Evaluate auto-approve
  // 6. If approved → create mission + steps
  // 7. Return result
}
```

#### Pitfall 3: Queue Keeps Growing When Quota Is Full

**Problem:** Quota full, but proposals still being approved, generating queued steps that will never execute.

**Fix:** Cap Gates — reject at the proposal entry point.

```typescript
const STEP_KIND_GATES: Record<string, StepKindGate> = {
  write_content: checkWriteContentGate,
  post_tweet: checkPostTweetGate,
  deploy: checkDeployGate,
};

async function checkPostTweetGate(sb: SupabaseClient) {
  const quota = await getOpsPolicyJson(sb, 'x_daily_quota', {});
  const limit = Number(quota.limit ?? 10);
  const { count } = await sb
    .from('ops_tweet_drafts')
    .select('id', { count: 'exact', head: true })
    .eq('status', 'posted')
    .gte('posted_at', startOfTodayUtcIso());
  
  if ((count ?? 0) >= limit) {
    return { ok: false, reason: `Daily tweet quota reached (${count}/${limit})` };
  }
  return { ok: true };
}
```

**Key principle:** Reject at the gate, don't pile up in the queue.

### Self-Healing: Stale Task Recovery

```typescript
// 30 minutes with no progress → mark failed
const STALE_THRESHOLD_MS = 30 * 60 * 1000;

const { data: stale } = await sb
  .from('ops_mission_steps')
  .select('id, mission_id')
  .eq('status', 'running')
  .lt('reserved_at', staleThreshold);

for (const step of stale) {
  await sb.from('ops_mission_steps').update({
    status: 'failed',
    last_error: 'Stale: no progress for 30 minutes',
  }).eq('id', step.id);
  
  await maybeFinalizeMissionIfDone(sb, step.mission_id);
}
```

### Triggers (4 Built-in)

| Condition | Action | Cooldown |
|-----------|--------|----------|
| Tweet engagement > 5% | Growth analyzes why it went viral | 2 hours |
| Mission failed | Sage diagnoses root cause | 1 hour |
| New content published | Observer reviews quality | 2 hours |
| Insight gets multiple upvotes | Auto-promote to permanent memory | 4 hours |

### Reaction Matrix

Probabilistic inter-agent interaction:

```json
{
  "source": "twitter-alt",
  "tags": ["tweet", "posted"],
  "target": "growth",
  "type": "analyze",
  "probability": 0.3,  // 30% chance, not 100%
  "cooldown": 120
}
```

> "probability isn't a bug, it's a feature. 100% determinism = robot. Add randomness = feels more like a real team."

### Heartbeat (VPS Crontab)

```bash
*/5 * * * * curl -s -H "Authorization: Bearer $KEY" https://yoursite.com/api/ops/heartbeat
```

---

## Part 2: Management Framework (KSimback)

### Core Insight

> "The hard part of AI isn't the intelligence, it's the management."

> "AI agent management is the new workforce management."

### Agent "Hiring" & Onboarding

#### SOUL.md Structure

Each agent needs a thorough SOUL.md:

```markdown
# Agent: [Name]

## Origin Story
[Creative backstory that explains how this agent approaches its work]

## Core Philosophy
[North star guiding principles]

## Inspirational Anchors
[Who/what does it model its thinking after]

## Skills & Methods
[Specific capabilities]

## Behavior Rules
[How it should act]

## Never Dos
[Hard boundaries]
```

#### Rules for Defining Agents

1. **Be specific** — Not "Research Analyst" but "SaaS Equity Research Analyst"
2. **Be thorough** — Origin story, philosophy, skills, never-dos
3. **Get feedback** — Run through LLMs to make it more robust

#### Onboarding Checklist

- [ ] SOUL.md complete and reviewed
- [ ] File structure consistent with other agents
- [ ] Access configured
- [ ] Announced to other agents
- [ ] Included in workflow system

### 4-Level Trust System

| Level | Name | Capabilities |
|-------|------|--------------|
| **L1** | Observer | Can perform assigned tasks, but cannot take action |
| **L2** | Advisor | Can perform tasks, recommend actions, execute on approval |
| **L3** | Operator | Autonomously execute on assigned projects within guardrails, daily reports |
| **L4** | Autonomous | Full authority over permissioned domains (still subject to guardrails) |

> "Trust is earned, not granted."

Agents start at L1 and get up-leveled through performance reviews. They can also be **demoted** if quality drops.

### Performance Reviews

Periodic evaluation:
1. Summary of output
2. Quality rating
3. Decision to up-level / maintain / down-level
4. Feedback passed to agent for learning

> "I had a content agent at L3 who started rushing work. Quality dropped so I bumped it back to L2 for a week."

### Shared Context Structure

Each project has its own folder:

```
project-name/
├── ACCESS.md      # Which agents have access
├── CONTEXT.md     # Working context (updated by any agent)
└── research/      # Supporting documents
```

- Any agent can read any project unless ACCESS.md denies them
- When an agent learns new context, they update CONTEXT.md
- CONTEXT.md has "Last updated by" header for traceability

### Agent Coordination Protocol

Agent registry with skills and capabilities:

```
When one agent needs help:
1. Check who's available
2. Provide context
3. Hand off the task
```

> "Last week I watched my design agent request help from a research agent for competitive analysis. Research agent delivered insights in 20 minutes. Design agent incorporated them and kept moving. I didn't coordinate any of that."

### Three Types of Memory

| Type | Purpose | Scope |
|------|---------|-------|
| **Daily notes** | Raw logs | Per agent |
| **Long-term memory** | Curated insights | Per agent |
| **Project-specific context** | Shared context | Shared across agents |

> "If I lose an agent and spin up a replacement, it has institutional memory from day one."

---

## Part 3: Implementation Checklist for OpenVibe

### Phase 1: Database Foundation

- [ ] Create Supabase tables (schema above)
- [ ] Set up initial policies in `ops_policy`
- [ ] Configure RLS for agent access

### Phase 2: Proposal Service

- [ ] Implement `createProposalAndMaybeAutoApprove()`
- [ ] Implement Cap Gates for each step kind
- [ ] Wire up all proposal sources (API, triggers, reactions)

### Phase 3: Execution Engine

- [ ] Set up VPS worker loop
- [ ] Implement step executors for each kind
- [ ] Implement `maybeFinalizeMissionIfDone()`

### Phase 4: Control Plane

- [ ] Heartbeat API route
- [ ] Trigger evaluator
- [ ] Reaction queue processor
- [ ] Stale task recovery

### Phase 5: Agent Management

- [ ] Define SOUL.md template
- [ ] Implement agent registry
- [ ] Set up shared context structure
- [ ] Implement level system

### Phase 6: Observability

- [ ] Activity feed dashboard
- [ ] Agent status (active/idle)
- [ ] Event stream viewer
- [ ] Mission/step progress tracker

---

## Key Takeaways

1. **Single source of truth** — Supabase holds all state
2. **Single entry point** — One function for proposal creation
3. **Reject early** — Cap Gates prevent queue buildup
4. **Self-healing** — Stale detection keeps system running
5. **Probabilistic reactions** — More natural than deterministic
6. **Trust is earned** — Leveling system for autonomy
7. **Memory persists** — Three-layer memory architecture

---

## Part 4: Multi-Agent IM Framework (Yangyi)

> Source: [@Yangyixxxx](https://x.com/yangyixxxx/status/1971425795429351834) (Sep 25, 2025, 49.8K views)

### Core Insight

> "如果你能看懂这张图，你就会意识到 —— **一定会出现一种支持人与 agents 交互的 IM**"

> "任务驱动的群组最大的意义在于**隔离上下文**"

> "这个框架是任何 Multi-Agents 的开端"

### Framework Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           Agent异步处理                                      │
├──────────┬──────────┬──────────┬─────────────────┬──────────────────────────┤
│ 沟通对象  │ 沟通机制  │ 反思机制  │ 群组（任务驱动）  │      个体Agent           │
├──────────┼──────────┼──────────┼─────────────────┼──────────────────────────┤
│ 混合群组  │ P2P单点  │ ReACT    │ 人员-加入/离开   │       LLM底座            │
│          │ 组间沟通  │ 自我反思  │                 │                          │
│Agent与   │ 向上汇报  │          │ 群组目标(公告)   │       Prompt             │
│Agent     │          │ 局外专家  │                 │                          │
│          │ 群组广播  │ 点评     │ 日志&数据Metrics │       MCP工具库          │
│人与Agent │ (群内交流)│          │                 │                          │
│          │          │ 人或Agent│ 工具(为达成任务) │       RAG知识库          │
│          │ 跨群组   │ 设定讨论  │ • 群组Agent可共用│                          │
│人与人    │ 广播(群发)│ 多元化   │ • 每个Agent独立  │       ReACT经验反思      │
│          │          │ 集体沟通  │   工具          │                          │
└──────────┴──────────┴──────────┴─────────────────┴──────────────────────────┘
                    │
                    ▼
         ┌─────────────────────────────┐
         │  基于IM的异步消息处理机制    │
         └─────────────────────────────┘
```

### Five Pillars

#### 1. 沟通对象 (Communication Objects)

| Type | Description |
|------|-------------|
| **混合群组** | Groups containing both humans and agents |
| **Agent与Agent** | Agent-to-agent communication |
| **人与Agent** | Human-to-agent interaction |
| **人与人** | Human-to-human (traditional) |

#### 2. 沟通机制 (Communication Mechanisms)

| Pattern | Use Case |
|---------|----------|
| **P2P单点沟通** | Direct 1:1 messaging |
| **组间沟通&向上汇报** | Cross-team + escalation |
| **群组广播 (群内交流)** | Broadcast within group |
| **跨群组广播 (群发)** | Broadcast across groups |

#### 3. 反思机制 (Reflection Mechanisms)

| Mechanism | Description |
|-----------|-------------|
| **Agent ReACT 自我反思** | Agent self-reflection via ReACT pattern |
| **局外专家点评** | External expert review |
| **人或Agent设定讨论主题** | Human or agent sets discussion topic |
| **多元化Agent集体沟通解决方案** | Diverse agents collaborate on solutions |

#### 4. 群组（任务驱动） (Task-Driven Groups)

**Key insight:** Groups exist to **isolate context** for specific tasks.

| Component | Purpose |
|-----------|---------|
| **人员 - 加入/离开** | Dynamic membership |
| **群组目标 (群公告)** | Group objective / announcement |
| **日志&数据Metrics** | Logging and metrics |
| **工具 (为达成任务)** | Tools for task completion |
| └ 群组Agent可共用 | Shared tools for group |
| └ 每个Agent独立工具 | Individual agent tools |

#### 5. 个体Agent (Individual Agent)

| Component | Description |
|-----------|-------------|
| **LLM底座** | Base LLM (e.g., Claude, GPT) |
| **Prompt** | System prompt / personality |
| **MCP工具库** | MCP tools (Model Context Protocol) |
| **RAG知识库** | RAG knowledge base |
| **ReACT经验反思** | ReACT experience reflection |

### Foundation Layer

> **基于IM的异步消息处理机制**

The entire system runs on an IM-based asynchronous message processing mechanism — essentially treating agent coordination like a chat system.

### Implications for OpenVibe

1. **Task-driven groups** = Context isolation = Clean separation of concerns
2. **Hybrid groups** (human + agent) is the natural interface, not separate dashboards
3. **Reflection mechanisms** are first-class citizens, not afterthoughts
4. **Individual agents** need: LLM + Prompt + Tools + Knowledge + Reflection
5. **IM as foundation** — all coordination is message-based, async-first

### Mapping to OpenVibe Architecture

| Yangyi Concept | OpenVibe Implementation |
|----------------|------------------------|
| 沟通对象 | Thread types (human, agent, mixed) |
| 沟通机制 | Message routing (P2P, broadcast, cross-thread) |
| 反思机制 | ReACT loop + external review triggers |
| 任务驱动群组 | Mission-scoped threads with access control |
| 个体Agent | Agent runtime (LLM + prompt + MCP + RAG) |
| 异步消息处理 | Supabase Realtime + event-driven execution |

---

*Last updated: 2026-02-08*
*Compiled by Maxos for OpenVibe reference*
