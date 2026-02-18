# OpenVibe SDK — Getting Started

## Install

```bash
pip install -e ".[dev]"   # from v4/openvibe-sdk/
```

Requires Python >= 3.12. Dependencies: `anthropic`, `langgraph`, `pydantic`, `pyyaml`.

---

## 1. Define an Operator

Operator = a group of workflow nodes. `@llm_node` = automatic LLM call where docstring is system prompt and return value is user message.

```python
from openvibe_sdk import Operator, llm_node, agent_node

class RevenueOps(Operator):
    operator_id = "revenue_ops"

    @llm_node(model="sonnet", temperature=0.3, output_key="qualification")
    def qualify_lead(self, state):
        """You are a lead qualification expert. Score the lead 0-100."""
        return f"Company: {state['company']}, Revenue: {state['revenue']}"

    @llm_node(model="haiku", output_key="summary")
    def summarize_deal(self, state):
        """You are a deal analyst. Summarize the deal status."""
        return f"Deal: {state['deal_name']}, Stage: {state['stage']}"
```

**What `@llm_node` does for you:**
- Docstring -> system prompt (can also load from file)
- Return value -> user message
- Auto JSON parse (if LLM returns JSON, it's automatically parsed)
- `state[output_key]` auto-populated with result
- Episode auto-recorded (when Role is managing the operator)

---

## 2. Define a Role

Role = WHO — identity, soul, memory, authority. A Role owns Operators.

```python
from openvibe_sdk import Role, AuthorityConfig, ClearanceProfile, Classification

class CRO(Role):
    role_id = "cro"
    soul = (
        "You are the CRO of Vibe. Data-driven, aggressive but measured.\n"
        "You care about pipeline velocity, CAC payback, and net revenue retention."
    )
    # soul can also point to a file: soul = "prompts/cro-soul.md"

    operators = [RevenueOps]

    authority = AuthorityConfig(
        autonomous=["qualify_lead", "review_pipeline"],
        needs_approval=["change_pricing"],
        forbidden=["sign_contracts"],
    )

    clearance = ClearanceProfile(
        agent_id="cro",
        domain_clearance={
            "sales": Classification.CONFIDENTIAL,
            "finance": Classification.INTERNAL,
        },
    )
```

---

## 3. Use the Role

### 3a. Simplest — respond()

```python
from openvibe_sdk import AgentMemory

llm = ...  # any LLMProvider (see section 7)
mem = AgentMemory(agent_id="cro")
cro = CRO(llm=llm, agent_memory=mem)

# Conversational response — soul auto-injected into system prompt
response = cro.respond("How's the pipeline looking?")
print(response.content)
# => "Pipeline is strong at $2.1M weighted..."
```

What happens under the hood:
1. `_load_soul()` loads soul text
2. `agent_memory.recall_insights(query=message)` retrieves relevant knowledge
3. System prompt assembled: `soul + knowledge + user message`
4. LLM called
5. Episode auto-recorded to agent_memory

### 3b. Execute workflow nodes through Operator

```python
op = cro.get_operator("revenue_ops")
state = {"company": "Acme Corp", "revenue": "$50M ARR"}
result = op.qualify_lead(state)
print(result["qualification"])
# => "85 — Strong fit, VP sponsor"
```

`get_operator()` returns an Operator with:
- **Role-aware LLM** — every LLM call auto-injects soul + memory
- **MemoryAssembler** — `memory_scope` decorator param auto-assembles context
- **Episode recorder** — node execution auto-recorded as Episode

### 3c. Authority check

```python
cro.can_act("qualify_lead")    # => "autonomous"
cro.can_act("change_pricing")  # => "needs_approval"
cro.can_act("sign_contracts")  # => "forbidden"
cro.can_act("unknown_action")  # => "needs_approval" (default: cautious)
```

---

## 4. Memory

### AgentMemory — 3-tier (Fact / Episode / Insight)

```python
from openvibe_sdk import AgentMemory, Insight, Episode
from datetime import datetime, timezone

mem = AgentMemory(agent_id="cro")

# Store an insight (L3 — compressed knowledge)
mem.store_insight(Insight(
    id="ins-1", agent_id="cro",
    content="Webinar leads convert at 2x the rate of cold outbound",
    confidence=0.85, evidence_count=12, source_episode_ids=[],
    created_at=datetime.now(timezone.utc), domain="sales",
))

# Recall insights by query (keyword match)
results = mem.recall_insights(query="webinar")

# Episodes are auto-recorded by respond() and @llm_node/@agent_node
episodes = mem.recall_episodes()
```

### reflect() — Episode to Insight compression

```python
# After accumulating episodes, compress into insights via LLM
insights = cro.reflect()
# LLM analyzes episodes, extracts patterns, stores as Insights
```

### MemoryFilesystem — virtual fs navigation

```python
fs = cro.memory_fs

fs.browse("/")                  # => ["identity", "knowledge", "experience"]
fs.browse("/knowledge")         # => ["sales", "finance"] (domains with data)
fs.browse("/knowledge/sales")   # => ["ins-1"] (insight IDs)

fs.read("/identity/soul.md")    # => soul text
fs.read("/.directory")          # => navigation summary with stats

fs.search("revenue retention")  # => [{"content": "...", ...}]
```

---

## 5. Agent Node — tool-using loop

```python
def web_search(query: str) -> str:
    """Search the web for information."""
    return f"Results for: {query}"

def read_url(url: str) -> str:
    """Read content from a URL."""
    return f"Content of {url}"

class CompanyIntel(Operator):
    operator_id = "company_intel"

    @agent_node(tools=[web_search, read_url], output_key="research")
    def research(self, state):
        """You are a research analyst. Use tools to gather information."""
        return f"Research {state['company_name']} thoroughly."
```

**How it works:**
1. LLM sees tool schemas (auto-generated from function signature + docstring)
2. LLM decides to call tools -> SDK executes them -> feeds results back
3. Loop repeats until LLM responds with text (no tool calls)
4. `max_steps` optional safety valve

---

## 6. RoleRuntime — managed lifecycle

For multiple Roles, use RoleRuntime to manage them together:

```python
from openvibe_sdk import RoleRuntime

llm = ...  # LLMProvider
runtime = RoleRuntime(roles=[CRO, CMO], llm=llm)

cro = runtime.get_role("cro")
# runtime auto-creates AgentMemory for each Role

response = cro.respond("Revenue update?")
assert cro.agent_memory is not None  # auto-created
assert cro.memory_fs is not None     # auto-available
```

RoleRuntime also supports registering workflow graph factories for full dispatch:

```python
runtime.register_workflow("revenue_ops", "qualify", create_qualify_graph)
result = runtime.activate("cro", "revenue_ops", "qualify", {"company": "Acme"})
```

---

## 7. LLM Provider

Built-in `AnthropicProvider`, or bring your own:

```python
from openvibe_sdk.llm.anthropic import AnthropicProvider

# Real provider (requires ANTHROPIC_API_KEY env var)
llm = AnthropicProvider()

# Model aliases: "sonnet" / "haiku" / "opus" auto-resolve to full model IDs
```

For testing, use a FakeLLM:

```python
from openvibe_sdk.llm import LLMResponse

class FakeLLM:
    def __init__(self, responses):
        self.calls = []
        self._responses = list(responses)
        self._i = 0

    def call(self, *, system, messages, **kw):
        self.calls.append({"system": system, "messages": messages})
        text = self._responses[min(self._i, len(self._responses) - 1)]
        self._i += 1
        return LLMResponse(content=text, tokens_in=10, tokens_out=20)
```

---

## Quick Reference

| Concept | Class/Decorator | What it does |
|---------|----------------|-------------|
| Operator | `class MyOp(Operator)` | Logic container, holds `@llm_node` methods |
| `@llm_node` | decorator | Single LLM call, docstring=system, return=user msg |
| `@agent_node` | decorator | Tool-using loop until text response |
| Role | `class MyRole(Role)` | Identity (soul + operators + authority + memory) |
| `respond()` | `role.respond(msg)` | Direct conversation with soul + memory context |
| `reflect()` | `role.reflect()` | Compress episodes into insights via LLM |
| `memory_fs` | `role.memory_fs` | Virtual filesystem over memory |
| `can_act()` | `role.can_act(action)` | Authority check (autonomous/needs_approval/forbidden) |
| RoleRuntime | `RoleRuntime(roles, llm)` | Manages multiple Roles, auto-wires memory |
| AgentMemory | `AgentMemory(agent_id)` | 3-tier: Episode, Insight + reflect |
| AuthorityConfig | on Role class | What Role can/can't do autonomously |
| ClearanceProfile | on Role class | Memory access control per domain |
