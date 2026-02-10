# V1 -> V2 Design Insight Audit

> Audited: 2026-02-09
> Purpose: Ensure nothing valuable from V1 research is lost in V2 pivot

---

## 1. MUST Carry Forward

### 1.1 Risk-Based Action Classification
**Source:** R3, SYNTHESIS Finding #7

V1 concluded: classify actions by **risk level** (AUTONOMOUS / APPROVE / ESCALATE), not confidence. A confident agent can still take catastrophic action.

**V2 action:** Port R3 risk matrix into Trust Level spec. Define what constitutes low/medium/high risk per domain (messaging, data, external comms, financial).

### 1.2 AI Summary Quality Is Load-Bearing
**Source:** SYNTHESIS Finding #2 (CRITICAL), resolution-prompt.md

If AI summaries are mediocre, the product has no reason to exist. V1 validated resolution prompt at 4.45/5.

**V2 action:** Establish output quality standards for all agent output types. Adapt V1 resolution prompt rules (self-correction, process filtering, inconclusive handling).

### 1.3 Progressive Disclosure (3-Layer Output)
**Source:** resolution-prompt.md, MVP-DESIGN-SYNTHESIS.md

Headline -> summary (3-5 bullets) -> full detail. Sonnet for generation, Haiku for post-processing.

**V2 action:** Standard for all agent output. Defined in AGENT-IN-CONVERSATION.md Section 3.3.

### 1.4 Context Assembly Architecture (4 Layers)
**Source:** AGENT-DEFINITION-MODEL.md, R7

4-layer model with token budgets. Key insight: sub-task context includes parent message summary, NOT full parent history.

**V2 action:** Reconcile with V2's `buildContextForAgent()`. Adopt minimal-parent-context principle for Mission -> Steps.

### 1.5 Universal Slack Pain Data
**Source:** slack-pain-ranking.md, fork-necessity-analysis.md

From 1,097-thread analysis:
- P1: No explicit outcomes (55% partial) -> Agent tasks need completion criteria
- P2: Topic drift (22pt drop) -> Agent conversations need scope boundaries
- P4: No structured output -> Agent output must be structured
- P6: Undiscoverable past decisions -> Audit log must be searchable
- P7: Review loops don't converge -> Need convergence mechanism

### 1.6 Kill Signals
**Source:** HANDOFF-CONTEXT-THESIS.md

V2 needs equivalent kill signals:
- Zero agents deployed after 4 weeks
- >40% of agent outputs rated unhelpful
- Trust levels don't change behavior
- Anthropic/OpenAI ships native agent governance
- Team prefers direct API over organization layer

### 1.7 Cross-Runtime Context Problem
**Source:** R7, SYNTHESIS Finding #3

No framework solves cross-runtime context. V2's Orchestration Layer spans multiple runtimes. Port V1's ContextItem schema.

### 1.8 Cost Model Realism
**Source:** R3

V1: ~$1K-2.5K/month for 20-person team. V2 will be higher (autonomous agents generate usage without human triggering). Update cost model.

---

## 2. Can Archive

| Item | Why Archivable |
|------|---------------|
| Fork/Resolve thread model (R1) | V2 uses Proposal -> Mission -> Steps |
| "Deep Dive" as core experience | V2 core is "Agent as Employee" |
| Adoption Wedge: product direction decisions | V2 wedge is "deploy first agent" |
| Slack Gravity analysis | V2 integrates with Slack, doesn't replace it |
| V1 12-table data model | V2 needs different schema |
| Fork Resolver agent | V2 handles as capability within agent role |

Preserve from archived items: Discourse threading insight ("deep threading kills engagement") and the adoption analysis framework methodology.

---

## 3. V2 Blind Spots

### 3.1 Output Quality Validation
V1 had validated prompt + test methodology + quality bar. V2 has no quality measurement framework. Risk: Performance Review becomes subjective.

### 3.2 Context Overflow Strategy
V1 had 4 strategies (summarization, checkpointing, hierarchical agents, sliding window). V2 has budget but no overflow behavior defined.

### 3.3 Agent-to-Agent Communication
V2 implies multi-agent coordination but hasn't specified HOW agents communicate. Yangyi's task-driven groups = right starting point.

### 3.4 Review Convergence
V1 identified "review loops don't converge" (P7). V2's Performance Review has no convergence mechanism for conflicting/endless feedback.

### 3.5 Searchable Agent History
V2's audit log is compliance-focused, not discovery-focused. Need semantic search over agent reasoning for institutional knowledge.

### 3.6 Notification Model
V2 agents generate events continuously. No notification design exists. Need trust-level-mapped notification urgency.

### 3.7 Moat Durability
V2-VISION says "OpenAI/Claude don't do org layer" but doesn't stress-test. V1 had rigorous moat analysis. Port framework.

---

## 4. Reusable Assets

| Asset | Source | V2 Application |
|-------|--------|---------------|
| Resolution Prompt v2 | resolution-prompt.md | Template for agent task completion reports |
| Progressive Disclosure Prompt | resolution-prompt.md (Haiku section) | Apply to all agent output > 500 words |
| Risk Classification Matrix | R3 | Map to L1-L4 trust levels |
| Context Assembly Pattern | AGENT-DEFINITION-MODEL.md | Adapt for V2 SOUL + mission context |
| Agent-as-Configuration principle | AGENT-DEFINITION-MODEL.md | Already adopted in AGENT-MODEL.md |
| 6-Sub-Problem Framework | HANDOFF-CONTEXT-THESIS.md | Architectural checklist for V2 |
| Discourse Threading Insight | R1 | Keep conversations flat by default |
| ContextItem Schema | R7 | Cross-runtime event payload format |
| Adoption Framework Methodology | adoption-wedge-analysis.md | Apply to "which agent use case first?" |
| Supabase + Tech Stack | MVP-DESIGN-SYNTHESIS.md | Confirmed in V2-VISION |

---

*Summary: 8 must-carry, 6 archivable, 7 blind spots, 10 reusable assets.*
