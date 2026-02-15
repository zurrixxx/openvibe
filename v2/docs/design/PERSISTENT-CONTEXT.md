# Persistent Context

> V2 Design Doc | Created: 2026-02-09
> Status: Draft
> Depends on: V2-VISION.md, AGENT-MODEL.md, AGENT-ORCHESTRATION-REFERENCE.md
> Scope: Layer 2 — How context is created, maintained, shared, and used across the workspace

---

## 1. Design Principles

**1. Context is a product, not a side-effect.** Most tools treat context as "whatever the LLM happens to remember." In OpenVibe, context is deliberately created, curated, and assembled. It's the compound interest of every conversation.

**2. Automatic by default, curated when it matters.** 90% of context should accumulate without anyone thinking about it. The remaining 10% -- the decisions, the "this is how we do things" moments -- get elevated by humans or agents flagging them. The system should never require a human to manually maintain a knowledge base as a separate activity from doing their work.

**3. Context has a cost, so it needs a budget.** Every token of context injected into a prompt is a token not available for reasoning. Context assembly is not "include everything" -- it's a prioritized selection under a hard ceiling. Think of it as packing for a trip: SOUL is your passport (always), current thread is your itinerary (always), everything else competes for the remaining suitcase space.

**4. Scoping is trust, not bureaucracy.** Agent context access follows the same trust model as action permissions. An L1 agent sees less context not because we're hiding things, but because an L1 agent hasn't earned the judgment to use broad context wisely. Context scope expands with trust level.

**5. Knowledge decays. Design for it.** A pricing decision from 6 months ago may have been superseded. A tech stack choice from last week is still fresh. Context without temporal awareness becomes misinformation. Every knowledge entry has a freshness signal.

---

## 2. Context Types

### 2.1 Taxonomy

| Type | Scope | Created By | Lifespan | Example |
|------|-------|-----------|----------|---------|
| **Thread History** | Per-thread | Automatic (messages) | Permanent (stored) | Last 50 messages in #product thread |
| **Dive Result** | Per-thread | Human publishes | Permanent | "Kiosk bundling: Option B projects 23% higher ARR" |
| **Agent Episode** | Per-agent | Automatic (after task) | 90-day TTL, some permanent | "Charles said: include cohort retention next time" |
| **Feedback** | Per-agent | Human gives feedback | Permanent (behavioral) | Thumbs down + "Too verbose, be concise" |
| **Knowledge Entry** | Per-workspace | Agent or human creates | Has `expires_at`, reviewed periodically | "SaaS pricing: Starter $29, Pro $99, Enterprise custom" |
| **SOUL** | Per-agent | Admin defines | Permanent (versioned) | Agent role, principles, constraints |
| **Channel Description** | Per-channel | Admin/human | Permanent | "#product: Product decisions and roadmap discussions" |
| **Workspace Config** | Per-workspace | Admin | Permanent | Company name, industry, team size |

### 2.2 Structured vs Unstructured

Context is layered:

| Layer | Format | Why |
|-------|--------|-----|
| **SOUL** | Structured YAML/JSONB | Queryable, composable, enforceable |
| **Knowledge entries** | Semi-structured: topic + content + metadata | Needs to be searchable by topic, but content is natural language |
| **Episodes** | Structured: type + summary + learning | Machine-processable for retrieval |
| **Thread history** | Unstructured: raw messages | Too expensive to structure every message; structure emerges at dive/publish time |
| **Dive results** | Semi-structured: headline + bullets + full | Created structured by the publish flow |

Key insight: **structure is created at decision points, not at every message.** Raw conversation is unstructured. When someone deep dives and publishes, structure is created. The act of making something structured IS the act of making it important.

---

## 3. Memory Architecture (MVP)

### 3.1 The Three Layers (and what to cut)

| Layer | What | MVP? | Reasoning |
|-------|------|------|-----------|
| **Working Memory** | Context window for current invocation | Yes | This is just "what goes in the prompt." Without it, nothing works. |
| **Episodic Memory** | Per-agent history of what it's done | Yes, minimal | Without it, agents start from zero every invocation. Even MVP needs "remember the feedback I gave you." |
| **Semantic Memory** | Shared workspace knowledge | Deferred to Sprint 5+ | The most valuable but the hardest to get right. Day 1 can survive without it. |

### 3.2 MVP Implementation (Day 1)

**Working Memory (Sprint 2):**
- Thread messages (last 50, configurable)
- SOUL (always injected)
- Current user info (name, role)

**Episodic Memory -- Minimal (Sprint 4):**
- Store only two episode types: `feedback_received` and `learning_acquired`
- Retrieve last 5 unresolved feedback items at every invocation
- No embedding search. Just `ORDER BY created_at DESC LIMIT 5 WHERE episode_type = 'feedback_received' AND applied = false`

**Knowledge Base -- Deferred (Sprint 5+):**
- Not in MVP. The team is small. They know the context.
- Trigger to build: agents repeatedly ask questions whose answers are in old threads they can't see.

### 3.3 Memory Creation

**How feedback becomes episodic memory:**

```
User gives thumbs down on agent message
  -> UI shows optional text field: "What should it do differently?"
  -> User types: "Include cohort data, not just overall retention"
  -> System creates agent_episode:
      episode_type: 'feedback_received'
      summary: "Include cohort data, not just overall retention"
      learning: null (extracted later or by agent on next invocation)
      applied: false
  -> Next invocation, this episode is in the prompt:
      "[RECENT FEEDBACK] User Charles (2 days ago): Include cohort data, not just overall retention"
```

**How completed tasks become episodes (auto, Sprint 4+):**

Only if:
- The task received explicit feedback (thumbs up/down)
- The task failed
- The task involved a trust-level check

Routine successful tasks with no feedback do NOT create episodes. This prevents memory pollution.

### 3.4 Memory Retrieval (MVP)

No semantic search on day 1. Retrieval is:

1. **Recency-based**: Last N episodes of type X
2. **Filtered**: Only `feedback_received` where `applied = false`
3. **Hard limit**: Max 5 episodes injected per invocation (~500 tokens)

Semantic search (pgvector embeddings) is the Phase 5 upgrade.

---

## 4. Knowledge Accumulation

### 4.1 The Natural Pipeline

```
Raw conversation (thread messages)
    | [human initiates deep dive]
Deep dive (human + AI thinking)
    | [human publishes]
Dive result (structured: headline + bullets + full)
    | [agent or human flags as knowledge]
Knowledge entry (topic + content + metadata + expiry)
    | [time passes, context changes]
Outdated / superseded / archived
```

Key decision: **knowledge entries are NOT auto-extracted from conversations.** They come from dive results and explicit human actions.

Why not auto-extract?
1. **Quality**: "Let's try $29 for Starter" is a suggestion, not a decision
2. **Authority**: Knowledge needs attribution and trust
3. **Volume**: Auto-extraction produces more noise than signal

### 4.2 How Knowledge Gets Created (MVP)

**Path 1: Dive Result Promotion (primary)**

When a dive is published, the result card includes a "Pin to Knowledge" affordance.

**Path 2: Agent Suggestion (Sprint 5+)**

After publishing, @Vibe asks: "Should I add this to workspace knowledge under 'pricing'?"

**Path 3: Manual Entry (always available)**

Admin or member adds knowledge entries directly.

### 4.3 Avoiding Knowledge Rot

1. **Expiry dates**: Knowledge entries have optional `expires_at`. Expired = flagged for review.
2. **Contradiction detection (Sprint 6+)**: New entry contradicts existing = flagged for admin.
3. **Usage tracking**: Entries never retrieved in 90 days = auto-archived.

---

## 5. Context Assembly

### 5.1 The Budget

Task-type dependent:

| Task Type | Context Budget | Rationale |
|-----------|---------------|-----------|
| Quick @mention response | ~8K tokens | Short answer, limited context needed |
| Thread conversation | ~15K tokens | Need recent thread history + SOUL + feedback |
| Deep dive session | ~30K tokens | Rich context needed |
| Publish/summarize | ~20K tokens | Need full dive history to compress |

### 5.2 Priority Stack

```
P0: SOUL (identity + principles + constraints)         ~500-2000 tokens
    ALWAYS included. Non-negotiable.

P1: Current task context                               ~2000-8000 tokens
    - For @mention: the message + surrounding 5 messages
    - For thread: last 50 messages
    - For deep dive: all dive messages + parent message from thread

P2: Active feedback (episodic, unresolved)             ~300-500 tokens
    - Last 5 feedback_received where applied=false

P3: Relevant knowledge entries (semantic memory)        ~500-2000 tokens
    - Only when knowledge base exists (Sprint 5+)

P4: Channel description + workspace context            ~100-200 tokens

P5: Recent dive results from same thread               ~500-1000 tokens
    - Headlines only

P6: Older episodic memory                              remainder
```

### 5.3 Cross-Channel Context

**MVP answer: No cross-channel context.** Each invocation gets context from its own channel/thread only.

The unlock is the knowledge base. Knowledge entries are workspace-scoped, not channel-scoped. An agent in #product that retrieves a knowledge entry about "tech stack: migrating to tRPC" gets cross-channel awareness through distilled knowledge, not raw messages.

### 5.4 Cross-Session Context

Agents "remember" through episodic memory, not re-reading old threads:

```
2 weeks ago:
  Feedback: "Don't recommend pricing changes without margin data"
  -> Episode created

Today:
  Agent invoked about pricing
  -> Episode retrieved, injected into prompt
  -> Agent includes margin data
```

The agent remembers the LEARNING, not the conversation. More efficient and more useful.

---

## 6. Scoping & Privacy

### 6.1 Agent Visibility Model

| Trust Level | Can See | Rationale |
|-------------|---------|-----------|
| L1 (Observer) | Channels it's explicitly added to; thread history only | Minimum exposure |
| L2 (Advisor) | Channels it's added to; thread history + dive results | Needs dive results for advice |
| L3 (Operator) | All public channels; shared knowledge base | Broad awareness for autonomy |
| L4 (Autonomous) | All channels including private (if granted); full KB | Full context for full autonomy |

### 6.2 Private Threads

| Type | Agent Access | Use Case |
|------|-------------|----------|
| **Human-only thread** | No agent can see or participate | HR, sensitive, legal |
| **Agent-restricted thread** | Only specified agents | Discussing agent performance |

### 6.3 Agent Memory Privacy

- Agent episodic memory is per-agent, not shared
- Knowledge entries are workspace-shared by design
- If agent is deactivated, episodes are archived, not transferred

---

## 7. Open Questions

1. **Knowledge Entry UI**: Dedicated sidebar section vs inline pinned messages vs admin-only? Recommendation: Simple searchable list sidebar.

2. **Feedback granularity**: Thumbs only vs thumbs + optional text vs structured form? Recommendation: Thumbs + optional text.

3. **Episode retention**: 90-day blanket TTL or type-specific? Recommendation: Feedback = permanent. Task completions = 90-day TTL.

4. **Deep dive history**: Agent sees previous dives as headlines, summaries, or full? Recommendation: D for MVP (dive results are messages in thread, included naturally). B as upgrade.

5. **Agent-to-agent memory sharing**: Ever? Recommendation: No for now. Important learnings promoted via knowledge base later.

6. **Trust level + context scope**: Ship simultaneously or separately? Recommendation: Uniform access for MVP. Add trust-based scoping when first L3 agent exists.

---

## 8. Implementation Phasing

| Phase | What | Sprint |
|-------|------|--------|
| **Day 1** | Working memory only: SOUL + thread messages + user info | Sprint 2 |
| **Week 3-4** | Feedback mechanism: thumbs up/down + text on agent messages | Sprint 2-3 |
| **Week 5-6** | Episodic memory (minimal): store feedback, inject last 5 | Sprint 3-4 |
| **Week 7-8** | Dive result awareness: published dives in thread context | Sprint 4 |
| **Post-dogfood** | Knowledge base: table, "Pin to Knowledge" UI, search | Sprint 5+ |
| **Later** | Semantic retrieval: pgvector embeddings | Sprint 6+ |
| **Later** | Cross-channel context via knowledge base | Sprint 6+ |
| **Later** | Trust-based context scoping | When L3+ agents exist |

---

## 9. The Flywheel

```
Humans and agents converse in threads
    -> Deep dives produce structured findings
        -> Findings get promoted to knowledge
            -> Knowledge feeds into future agent invocations
                -> Agents give better responses with more context
                    -> Better responses lead to more deep dives
                        -> More deep dives produce more knowledge
```

Each cycle, the workspace gets smarter. This is the compound interest of context -- and OpenVibe's data moat.

---

*This design starts minimal (working memory + feedback only) and expands based on observed need. The biggest risk is not "too little context" but "too much noise in context." Start sparse, add when agents demonstrably suffer from missing information.*

*Next: TRUST-SYSTEM.md -- How does L1-L4 mechanically gate agent actions?*
