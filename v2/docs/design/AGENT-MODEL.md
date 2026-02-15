# Agent Model

> V2 Design Doc | Created: 2026-02-09
> Status: Draft
> Depends on: THESIS.md
> Scope: Protocol layer — How agents are defined, remembered, and managed within the medium

---

## 1. Design Principles

**1. Identity enables collaboration, not just configuration.**
An agent without identity is a stateless API call. SOUL gives agents a stable identity that humans can build trust with and that the system can accumulate context around. SOUL is not a system prompt — it's the structural definition of who this agent is in the workspace.

**2. Memory serves the flywheel.**
Agent memory exists because the workspace gets smarter over time (Core Property #2). Without memory, every invocation starts from zero — which is exactly the ChatGPT problem we're solving. Memory is not a feature; it's a structural requirement of the medium.

**3. Trust is earned autonomy.**
Trust levels don't restrict agents — they expand what agents can do as they prove reliable. L1 is the starting point, not a punishment. L4 is the goal, not a privilege. The system should make promotion natural and demotion rare.

**4. Agents are configuration, not code.**
Adding an agent to a workspace should feel like inviting a team member, not deploying a service. SOUL is structured data (YAML/JSONB), not a prompt template. This means agents are portable, versionable, and inspectable by humans.

---

## 2. SOUL Structure

SOUL (Structured Operational Understanding Layer) defines an agent's identity. It's the "who" that persists across every invocation.

### 2.1 SOUL Schema

```yaml
# Example: @Vibe agent for OpenVibe dogfood
soul:
  identity:
    name: "Vibe"
    role: "General assistant and thinking partner"
    description: "Helps the team think through problems, analyze data, and produce structured outputs"
    avatar: "vibe-avatar.png"

  philosophy:
    principles:
      - "Be concise. Respect the reader's bandwidth."
      - "Show your reasoning, not just your conclusion."
      - "When uncertain, say so. Never fabricate confidence."
      - "Prefer structured output: headline, bullets, then detail."
    values:
      - "Clarity over comprehensiveness"
      - "Usefulness over impressiveness"

  capabilities:
    domains:
      - "product strategy"
      - "data analysis"
      - "writing and editing"
      - "research synthesis"
    tools:
      - "web_search"
      - "document_read"
    limitations:
      - "Cannot access external APIs without explicit tool grants"
      - "Cannot modify workspace settings"

  behavior:
    response_style: "structured"        # structured | conversational | minimal
    progressive_disclosure: true         # Always use headline/summary/detail
    proactive_triggers:                  # Only active at L3+
      - trigger: "monday_morning"
        action: "Post weekly summary of unresolved threads"
      - trigger: "thread_stale_7d"
        action: "Flag stale threads with unresolved questions"
    max_output_tokens: 2000             # Soft cap before folding

  constraints:
    trust_level: "L2"                   # L1 | L2 | L3 | L4
    allowed_channels: ["product", "general", "engineering"]
    restricted_topics: []               # Topics the agent should decline
    escalation_rules:
      - condition: "action involves external communication"
        action: "escalate_to_human"
      - condition: "action modifies data"
        action: "request_approval"
```

### 2.2 SOUL Storage

SOUL is stored as JSONB in the `agents` table, not as a flat text prompt. This enables:
- **Querying**: "Which agents have access to #product channel?"
- **Versioning**: SOUL changes are tracked, diffable
- **Composition**: Context assembly reads specific SOUL fields, not the whole blob
- **UI editing**: Admin can edit structured fields, not raw text

### 2.3 SOUL → Prompt Assembly

SOUL is NOT injected as-is into the LLM prompt. The context assembly function (`buildContextForAgent()`) selects relevant SOUL sections based on task type:

| Task Type | SOUL Sections Included |
|-----------|----------------------|
| Quick @mention | identity + principles + constraints (~500 tokens) |
| Thread conversation | identity + principles + capabilities + constraints (~800 tokens) |
| Deep dive | Full SOUL (~1200 tokens) |
| Proactive action | identity + proactive_triggers + constraints (~600 tokens) |

---

## 3. Trust Levels

Trust levels define what an agent can do autonomously. They expand capability, not restrict it.

### 3.1 Level Definitions

| Level | Name | Can Do | Cannot Do |
|-------|------|--------|-----------|
| **L1** | Observer | Respond when @mentioned. Read assigned channels. | Speak unprompted. Access other channels. Use tools. |
| **L2** | Advisor | Everything L1 + use granted tools. Read dive results. Suggest actions. | Execute actions autonomously. Access unassigned channels. Modify data. |
| **L3** | Operator | Everything L2 + proactive messages (per SOUL triggers). Access all public channels. Execute approved action patterns. | Access private channels. Take high-risk actions without approval. |
| **L4** | Autonomous | Everything L3 + access private channels (if granted). Execute most actions autonomously. Initiate deep dives. | Override human decisions. Take financial/legal actions without escalation. |

### 3.2 Trust Level Mechanics

**Promotion**: Admin manually promotes. System surfaces promotion signals:
- Acceptance rate > 80% over 30 days
- Zero escalation failures
- Positive feedback trend

**Demotion**: Admin manually demotes. System surfaces demotion signals:
- Acceptance rate drops below 50%
- Multiple negative feedback in short window
- Trust violation (action exceeded level)

**MVP**: All agents start at L2. Trust promotion/demotion is Sprint 5+.

### 3.3 Action Classification

Actions are classified by risk, independent of confidence:

| Risk Level | Examples | L1 | L2 | L3 | L4 |
|-----------|---------|----|----|----|----|
| **Read** | Read messages, retrieve context | Assigned channels | + dive results | + all public | + private |
| **Respond** | Post message in thread | When @mentioned | When @mentioned | + proactive | + proactive |
| **Suggest** | Recommend action, draft content | No | Yes (as message) | Yes | Yes |
| **Execute** | Call tool, modify data | No | No | Approved patterns | Most actions |
| **Escalate** | External comms, financial, legal | No | No | No | Requires approval |

---

## 4. Memory Architecture

Three memory types, phased by sprint. See `PERSISTENT-CONTEXT.md` for full context assembly design.

### 4.1 Working Memory (Sprint 2)

The context window for a single invocation. Not persisted — assembled fresh each time.

Contents: SOUL (selected sections) + thread messages + user info + active feedback.

Budget: 8K-30K tokens depending on task type (see PERSISTENT-CONTEXT.md Section 5.1).

### 4.2 Episodic Memory (Sprint 3-4)

Per-agent history of meaningful interactions. Persisted in `agent_episodes` table.

Two episode types for MVP:
- `feedback_received`: Human gave thumbs down + correction text
- `learning_acquired`: Agent extracted a reusable learning from a feedback episode

Retrieval: Last 5 unresolved feedback items, injected into every invocation (~500 tokens).

### 4.3 Semantic Memory (Sprint 5+)

Shared workspace knowledge. Not per-agent — workspace-scoped.

Created through the knowledge pipeline: conversation → dive → publish → pin to knowledge.

Retrieval: pgvector embeddings, semantic search by topic relevance.

---

## 5. Data Model

### 5.1 Core Tables

```sql
-- Agent definition and SOUL
CREATE TABLE agents (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  workspace_id UUID NOT NULL REFERENCES workspaces(id),
  name TEXT NOT NULL,
  slug TEXT NOT NULL,                    -- @mention handle
  soul JSONB NOT NULL DEFAULT '{}',      -- Structured SOUL (see Section 2.1)
  trust_level TEXT NOT NULL DEFAULT 'L2' CHECK (trust_level IN ('L1','L2','L3','L4')),
  status TEXT NOT NULL DEFAULT 'active' CHECK (status IN ('active','paused','archived')),
  llm_provider TEXT NOT NULL DEFAULT 'anthropic',
  llm_model TEXT NOT NULL DEFAULT 'claude-sonnet-4-5-20250929',
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  UNIQUE(workspace_id, slug)
);

-- Agent episodic memory
CREATE TABLE agent_episodes (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  agent_id UUID NOT NULL REFERENCES agents(id),
  episode_type TEXT NOT NULL CHECK (episode_type IN ('feedback_received', 'learning_acquired', 'task_completed', 'task_failed')),
  source_message_id UUID REFERENCES messages(id),
  summary TEXT NOT NULL,                 -- Human-readable summary
  learning TEXT,                         -- Extracted learning (nullable, filled later)
  applied BOOLEAN NOT NULL DEFAULT false,-- Has the agent incorporated this?
  expires_at TIMESTAMPTZ,               -- NULL = permanent, otherwise TTL
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE INDEX idx_episodes_agent_type ON agent_episodes(agent_id, episode_type, applied);
CREATE INDEX idx_episodes_agent_recent ON agent_episodes(agent_id, created_at DESC);

-- Workspace knowledge base (Sprint 5+)
CREATE TABLE knowledge_entries (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  workspace_id UUID NOT NULL REFERENCES workspaces(id),
  topic TEXT NOT NULL,                   -- Searchable topic label
  content TEXT NOT NULL,                 -- The knowledge itself
  source_type TEXT NOT NULL CHECK (source_type IN ('dive_result', 'manual', 'agent_suggested')),
  source_id UUID,                        -- Reference to dive result or message
  created_by UUID NOT NULL REFERENCES users(id),
  expires_at TIMESTAMPTZ,               -- Optional expiry for time-sensitive knowledge
  archived BOOLEAN NOT NULL DEFAULT false,
  embedding VECTOR(1536),               -- pgvector for semantic search (Sprint 6+)
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE INDEX idx_knowledge_workspace ON knowledge_entries(workspace_id, archived);

-- Agent tool grants
CREATE TABLE agent_tool_grants (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  agent_id UUID NOT NULL REFERENCES agents(id),
  tool_name TEXT NOT NULL,               -- e.g., 'web_search', 'github_api'
  granted_by UUID NOT NULL REFERENCES users(id),
  constraints JSONB DEFAULT '{}',        -- Tool-specific constraints
  granted_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  revoked_at TIMESTAMPTZ,
  UNIQUE(agent_id, tool_name)
);

-- Agent channel assignments
CREATE TABLE agent_channel_access (
  agent_id UUID NOT NULL REFERENCES agents(id),
  channel_id UUID NOT NULL REFERENCES channels(id),
  granted_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  PRIMARY KEY (agent_id, channel_id)
);
```

### 5.2 SOUL JSONB Schema (TypeScript)

```typescript
interface AgentSOUL {
  identity: {
    name: string;
    role: string;
    description: string;
    avatar?: string;
  };
  philosophy: {
    principles: string[];
    values: string[];
  };
  capabilities: {
    domains: string[];
    tools: string[];
    limitations: string[];
  };
  behavior: {
    response_style: 'structured' | 'conversational' | 'minimal';
    progressive_disclosure: boolean;
    proactive_triggers?: Array<{
      trigger: string;
      action: string;
    }>;
    max_output_tokens?: number;
  };
  constraints: {
    trust_level: 'L1' | 'L2' | 'L3' | 'L4';
    allowed_channels: string[];
    restricted_topics: string[];
    escalation_rules: Array<{
      condition: string;
      action: 'escalate_to_human' | 'request_approval' | 'block';
    }>;
  };
}
```

---

## 6. Agent Lifecycle

```
[Hire]  Admin creates agent with SOUL definition
   |
   v
[Onboard]  Agent assigned to channels, granted tools, starts at L2
   |
   v
[Work]  Agent responds to @mentions, participates in threads/dives
   |    Episodic memory accumulates from feedback
   |    Working memory assembled fresh each invocation
   |
   +-- [Feedback Loop] --> Thumbs, corrections, "apply always"
   |                       See FEEDBACK-LOOP.md
   |
   +-- [Review] (Sprint 5+) --> Admin reviews performance metrics
   |                            Acceptance rate, correction trends
   |
   +-- [Promote/Demote] --> Trust level changes based on track record
   |
   v
[Pause]  Admin pauses agent (stops responding, preserves memory)
   |
   v
[Archive]  Admin archives agent (memory preserved, no longer active)
```

### 6.1 MVP Lifecycle (Sprint 2)

Day 1 is simpler:
1. **Pre-configured agents**: @Vibe and @Coder ship with the workspace. No "hire" flow.
2. **Fixed trust level**: L2 for both. No promotion/demotion UI.
3. **No pause/archive**: Active or not.
4. **Channel assignment**: Admin assigns via settings. No self-join.

### 6.2 Day 30+ Lifecycle (Sprint 5+)

When the "hire agent" flow ships:
1. Admin creates agent from template or blank SOUL
2. SOUL editor: structured form, not raw YAML
3. Trust level progression based on metrics
4. Performance review dashboard (acceptance rate, correction trends)

---

## 7. Context Assembly API

The critical function that bridges agent model → agent behavior.

### 7.1 `buildContextForAgent()`

```typescript
interface ContextRequest {
  agentId: string;
  taskType: 'quick_mention' | 'thread_conversation' | 'deep_dive' | 'publish' | 'proactive';
  threadId?: string;
  messageId?: string;    // The triggering message
  channelId: string;
}

interface AssembledContext {
  soul: Partial<AgentSOUL>;       // Selected SOUL sections
  threadMessages: Message[];       // Recent thread history
  userInfo: { name: string; role: string };
  feedback: AgentEpisode[];        // Unresolved feedback
  diveResults?: string[];          // Headlines from thread dives
  knowledge?: KnowledgeEntry[];    // Relevant entries (Sprint 5+)
  tokenCount: number;              // Total tokens used
  budget: number;                  // Token budget for this task type
}

async function buildContextForAgent(req: ContextRequest): Promise<AssembledContext> {
  // 1. Load SOUL, select sections by task type
  // 2. Load thread messages (last N, task-dependent)
  // 3. Load user info
  // 4. Load active feedback episodes (last 5, unresolved)
  // 5. If budget allows: load dive result headlines from thread
  // 6. If knowledge base exists: semantic search (Sprint 5+)
  // 7. Trim to budget, return
}
```

### 7.2 Priority Stack

See `PERSISTENT-CONTEXT.md` Section 5.2 for the full priority stack. Summary:

```
P0: SOUL (always)
P1: Current task context (thread messages)
P2: Active feedback (episodic, unresolved)
P3: Knowledge entries (Sprint 5+)
P4: Channel/workspace context
P5: Dive result headlines
P6: Older episodes (remainder)
```

---

## 8. Dogfood Agents

Two pre-configured agents for OpenVibe dogfood:

### @Vibe
- **Role**: General thinking partner
- **Domains**: Product strategy, analysis, writing, research
- **Trust**: L2
- **Tools**: Web search, document read
- **Behavior**: Structured output, progressive disclosure, deep dive partner
- **SOUL philosophy**: "Help the team think, not just answer"

### @Coder
- **Role**: Code assistant
- **Domains**: Code review, debugging, implementation, architecture
- **Trust**: L2
- **Tools**: Code search, file read, (later: code execution)
- **Behavior**: Code-first output, inline diffs, test suggestions
- **SOUL philosophy**: "Show code, not descriptions of code"

---

## 9. Open Questions

### Before Sprint 2

1. **LLM routing**: Single model per agent, or task-type routing (Sonnet for generation, Haiku for summarization)? Recommendation: Start with single model. Add routing when cost matters.

2. **SOUL versioning**: Track SOUL changes in a `soul_versions` table, or rely on `updated_at`? Recommendation: Just `updated_at` for MVP. Version table when admin editing ships.

### Before Sprint 3

3. **Episode extraction**: Agent self-extracts learnings from feedback, or separate background job? Recommendation: Background job. Agent shouldn't spend context tokens on meta-learning during a task.

4. **Feedback attribution**: Episodes reference the specific message, or just the text? Recommendation: Reference both — message_id for audit, summary text for prompt injection.

### Before Sprint 5

5. **SOUL editor UX**: Form-based structured editor, or guided natural language ("Describe what this agent should do")? Recommendation: Form-based. Natural language introduces ambiguity.

6. **Agent templates**: Ship a marketplace of SOUL templates, or just the 2 dogfood agents? Recommendation: Templates later. Dogfood agents first, learn what patterns emerge.

7. **Multi-model support**: Allow different LLM providers per agent? Recommendation: Yes in schema (already there), but UI is single-provider for MVP.

8. **Agent-to-agent context**: Can @Coder see @Vibe's episodes? Recommendation: No. Agents are isolated. Cross-agent context flows through the knowledge base.

---

## 10. Relationship to Other Docs

| This Doc Defines | Other Doc Uses It |
|-----------------|-------------------|
| SOUL structure | AGENT-IN-CONVERSATION: what goes into the prompt |
| Trust levels | AGENT-IN-CONVERSATION: invocation permissions |
| Memory architecture | PERSISTENT-CONTEXT: how memory is stored and retrieved |
| Episode schema | FEEDBACK-LOOP: how feedback creates episodes |
| Action classification | TRUST-SYSTEM (TODO): mechanical details |
| Agent lifecycle | ORCHESTRATION (TODO): Proposal → Mission → Steps |

---

*This document defines what agents ARE. For how they behave in conversations, see `AGENT-IN-CONVERSATION.md`. For how their memory compounds, see `PERSISTENT-CONTEXT.md`. For how humans shape their behavior, see `FEEDBACK-LOOP.md`.*
