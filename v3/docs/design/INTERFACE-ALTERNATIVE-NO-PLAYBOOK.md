# Interface Alternative: No Playbook Abstraction Layer

> **Status:** 💭 Side Note - Not Approved
> **Date:** 2026-02-12
> **Context:** During V3 interface design, questioned whether "workflow" and "playbook" abstractions are necessary

---

## The Question

When designing sidebar structure, we kept trying to find the right word:
- ❌ "Workflows" - too tool-like (Zapier/n8n), doesn't reflect agent intelligence
- ❌ "Playbooks" - sports metaphor, implies fixed routines, not natural language
- ❌ "Processes" - too traditional, no differentiation from legacy BPM
- ❌ "Routines" - too mechanical
- ❌ "Operations" - too vague

**Core realization:** Maybe we don't need this abstraction layer at all.

---

## User Mental Model

### What users actually say:
- "我要让 agent 学会处理发票"
- "这个流程自动化了吗？"
- "agent 现在能做什么？"
- "这件事 agent 能帮我吗？"

### What users DON'T say:
- "我要创建一个 playbook"
- "这个 playbook 执行成功率 94%"

**Insight:** Users care about **what agents can do**, not abstract concepts like playbooks.

---

## Simplified Structure

### Sidebar Design (No Playbook Layer)

```
┌─────────────────────────────┐
│ TOP SECTION (Customizable)  │
│                             │
│ 🏠 Home                  ▶  │
│                             │
│ 🤖 Agents                ▶  │  ← Who can do things (Capabilities)
│                             │
│ ⚡️ Active               ▶  │  ← What's happening now (Execution)
│                             │
│ ••• More                 ▶  │
│                             │
├─────────────────────────────┤
│ BOTTOM SECTION (Fixed)      │
│                             │
│ SPACES                   ▼  │  ← Where content lives
│ • Finance (3)            ▼  │
│   • Q1 Budget (12)          │
│   • Invoice Review (3)      │
│                             │
│ • RevOps (1)             ▶  │
│ • Executive              ▶  │
│                             │
│ [+ New Space]               │
└─────────────────────────────┘
```

---

## Three Core Concepts

### 1. Agents (智能层)

**What it shows:**
- Who are the agents in this workspace?
- What can each agent do? (Capabilities)
- What is each agent's trust level?
- How is each agent performing?

**Expanded view:**
```
🤖 AGENTS                              ▼
┌──────────────────────────────────────┐
│ @Finance_Agent              [L2] 🟢  │
│ ┌──────────────────────────────────┐ │
│ │ Can do:                          │ │
│ │ • Process invoices (L2)          │ │
│ │ • Month-end close (L1)           │ │
│ │ • Budget analysis (L0)           │ │
│ │                                  │ │
│ │ Performance:                     │ │
│ │ • 94% success rate (30 days)     │ │
│ │ • 247 tasks completed            │ │
│ │                                  │ │
│ │ [Teach New Skill] [Configure]    │ │
│ └──────────────────────────────────┘ │
│                                      │
│ @RevOps_Agent               [L2] 🟢  │
│ • Lead scoring, pipeline analysis    │
│                                      │
│ @QA_Agent                   [L1] 🟡  │
│ • Learning mode                      │
│                                      │
│ ⊕ Add Agent                          │
└──────────────────────────────────────┘
```

**User flow:**
- Want to automate something? → Go to Agents → Pick one → Teach it
- Want to see what's automated? → Go to Agents → See what each can do
- Want to configure trust? → Go to Agents → Configure

---

### 2. Active (执行层)

**What it shows:**
- What's happening right now?
- What needs my attention?
- What's being worked on?

**Expanded view:**
```
⚡️ ACTIVE                              ▼
┌──────────────────────────────────────┐
│ ⚠️ NEED REVIEW (5)                   │
│    • Invoice #1234 ($12K unusual)    │
│      @Finance_Agent → waiting        │
│    • Lead score: Alice Chen          │
│      @RevOps_Agent → waiting         │
│    [Review All]                      │
│                                      │
│ ⟳ IN PROGRESS (23)                   │
│    • Invoice batch processing        │
│      @Finance_Agent - 47/50          │
│    • Lead scoring (Feb batch)        │
│      @RevOps_Agent - running         │
│    [View All]                        │
│                                      │
│ ✓ COMPLETED TODAY (47)               │
│    [View History]                    │
└──────────────────────────────────────┘
```

**User flow:**
- Check what needs attention → Go to Active → See "Need Review"
- Monitor progress → Go to Active → See "In Progress"
- Review history → Go to Active → See "Completed"

---

### 3. Spaces (内容层)

Same as current design - where conversations and content live.

---

## Comparison: With vs Without Playbook Layer

### With Playbook Layer (Current thinking)

```
User: "我要让 agent 处理发票"
System: "Create Invoice Processing Playbook"
User: "什么是 playbook？"
System: "It's like... a reusable workflow template..."
User: "😕 我就是想让 agent 帮我处理发票"

Mental model:
Playbook → Instantiate → Mission → Agent executes
(3 layers of abstraction)
```

### Without Playbook Layer (This proposal)

```
User: "我要让 agent 处理发票"
System: "Teach @Finance_Agent to process invoices"
User: "对，就是这个意思"

Mental model:
Agent learns capability → Agent executes when needed
(2 layers, direct)
```

---

## How "Workspace Gets Smarter" Shows Up

**Current design (with playbook):**
- Playbook library grows
- Playbook success rate improves
- Playbook coverage increases

**This proposal (no playbook):**
- Agent capabilities grow (listed under each agent)
- Agent trust level upgrades (L0 → L1 → L2 → L3)
- Agent success rate improves

**Which is more natural?**
- "Our @Finance_Agent can now do month-end close automatically" ✅
- "Our Invoice Processing Playbook success rate is 94%" ❓

---

## Management System Alignment

### Human team (OKR):
```
Q1 Objective: Improve financial operations efficiency
KR1: Close cycle from 10 days to 5 days
KR2: Invoice error rate < 1%
KR3: Human intervention < 10 times/month
```

### Human+Agent team (This proposal):
```
Instead of "Playbook maturity"...

Track by Agent Capability:
- @Finance_Agent capabilities:
  ├─ Invoice processing (L2) - 94% success, 247 done
  ├─ Month-end close (L1) - 87% success, 12 done
  └─ Budget analysis (L0) - Learning, 3 done

Metrics:
- Coverage: What % of work can agents do?
- Autonomy: What % requires human approval?
- Performance: Success rate per capability
```

**Simpler mental model:** Agents are team members with growing capabilities.

---

## Teaching Flow (Without Playbook Abstraction)

### User wants to automate invoice processing:

```
1. Go to Agents section
2. Click @Finance_Agent
3. Click [Teach New Skill]

Dialog:
┌────────────────────────────────────┐
│ Teach @Finance_Agent               │
│                                    │
│ What do you want to teach?         │
│ ┌────────────────────────────────┐ │
│ │ Process invoices               │ │
│ └────────────────────────────────┘ │
│                                    │
│ How should I learn?                │
│ ○ Watch you do it (demonstration) │
│ ○ Follow your instructions        │
│ ○ Learn from examples              │
│                                    │
│          [Start Teaching]          │
└────────────────────────────────────┘
```

After teaching, it shows up as a capability:
```
@Finance_Agent [L2]
├─ Process invoices (L1) ← New capability
│  Trust level: L1 (requires approval)
│  Learned: 2026-02-12
│  Success: 0/0 (not executed yet)
```

**No "playbook" mentioned anywhere. Just "teach agent a skill."**

---

## Advantages

1. **No abstraction to explain** - Users immediately understand "agent can do X"
2. **Agent-centric** - Aligns with "agent as participant" vision
3. **Natural language** - "Teach agent to do X" not "Create playbook for X"
4. **Clear capability view** - See all agent skills in one place
5. **Trust level natural** - "Agent trust level L2 for invoice processing" makes sense

---

## Potential Issues

### 1. What about reusable patterns?

**Problem:** Multiple agents need to do similar things (e.g., "approval flow")

**Solution:**
- Templates/patterns at teaching level
- "Teach @Agent using Finance Approval template"
- Not exposed as "playbook" to user

### 2. What about complex multi-agent workflows?

**Problem:** Some operations need orchestration (Agent A → Agent B → Agent C)

**Solution:**
- Show as capabilities: "@Lead_Agent coordinates lead qualification"
- Orchestration is hidden implementation detail
- User just sees: "This agent can coordinate these other agents"

### 3. What about analytics/reporting?

**Problem:** Management wants to see "what processes are automated"

**Solution:**
- Capability coverage report
- Shows: "Finance operations: 80% automated (12 capabilities)"
- Same data, different framing

---

## Open Questions

1. **Capability granularity:**
   - Is "Process invoices" one capability or many?
   - How to handle subcapabilities?

2. **Multi-agent coordination:**
   - How to teach workflows that span multiple agents?
   - Does one agent "own" the orchestration?

3. **Migration from current design:**
   - If we have playbooks in current design, how to communicate this change?

4. **Industry language:**
   - Does removing "playbook" make us less credible to enterprise buyers?
   - Do they expect to see "workflow library" or similar?

---

## Decision Needed

Should V3 interface:
- **Option A:** Keep playbook/workflow abstraction (current direction)
- **Option B:** Adopt agent-capability model (this proposal)
- **Option C:** Hybrid - playbooks exist but are de-emphasized in UI

**Trade-off:**
- Option A: More conceptually complete, but requires explaining abstractions
- Option B: Simpler for users, but may need playbook concept for advanced features
- Option C: Might get worst of both worlds (confusing)

---

## Related Documents

- `INTERFACE-FINAL-DESIGN.md` - Current approved design (with Workflows section)
- `THESIS.md` - V3 vision (agent as participant, cognition as infrastructure)
- Discussion date: 2026-02-12 (questioning "workflow" and "playbook" terminology)

---

## Status

💭 **Side note for consideration**

This alternative was proposed during interface design but not yet evaluated or approved. Preserving here for future reference.
