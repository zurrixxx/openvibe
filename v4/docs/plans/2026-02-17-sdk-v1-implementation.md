# OpenVibe SDK V1 — Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Build `openvibe-sdk` as a 4-layer Python package extracted from vibe-ai-adoption, with `@llm_node`, `@agent_node`, Role identity, and protocol-based infrastructure.

**Architecture:** Bottom-up — Layer 0 (Infrastructure protocols + types) → Layer 1 (Primitives: decorators + tools) → Layer 2 (Operator + OperatorRuntime) → Layer 3 (Role + RoleRuntime). Each layer depends only on the layer below.

**Tech Stack:** Python 3.13, anthropic SDK, langgraph, pydantic, pyyaml, pytest

**Design docs (read before starting):**
- `v4/docs/plans/2026-02-17-sdk-4-layer-architecture.md` — full 4-layer design
- `v4/docs/plans/2026-02-17-operator-sdk-design.md` — Operator layer detail + @llm_node/@agent_node specs

**Reference implementation:**
- `v4/vibe-ai-adoption/src/vibe_ai_ops/operators/base.py` — current OperatorRuntime + call_claude()
- `v4/vibe-ai-adoption/src/vibe_ai_ops/shared/claude_client.py` — current ClaudeClient
- `v4/vibe-ai-adoption/src/vibe_ai_ops/shared/models.py` — current config models
- `v4/vibe-ai-adoption/src/vibe_ai_ops/shared/config.py` — current YAML loader

---

## Task 1: Project Scaffold

**Files:**
- Create: `v4/openvibe-sdk/pyproject.toml`
- Create: `v4/openvibe-sdk/src/openvibe_sdk/__init__.py`
- Create: `v4/openvibe-sdk/src/openvibe_sdk/llm/__init__.py`
- Create: `v4/openvibe-sdk/src/openvibe_sdk/memory/__init__.py`
- Create: `v4/openvibe-sdk/tests/__init__.py`
- Create: `v4/openvibe-sdk/tests/test_imports.py`

**Step 1: Create directory structure**

```bash
mkdir -p v4/openvibe-sdk/src/openvibe_sdk/llm
mkdir -p v4/openvibe-sdk/src/openvibe_sdk/memory
mkdir -p v4/openvibe-sdk/tests
```

**Step 2: Create pyproject.toml**

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.backends"

[project]
name = "openvibe-sdk"
version = "0.1.0"
description = "4-layer framework for human+agent collaboration"
requires-python = ">=3.12"
dependencies = [
    "anthropic>=0.40.0",
    "langgraph>=0.3.0",
    "pydantic>=2.6.0",
    "pyyaml>=6.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0",
    "pytest-mock>=3.12",
]

[tool.hatch.build.targets.wheel]
packages = ["src/openvibe_sdk"]

[tool.pytest.ini_options]
testpaths = ["tests"]
pythonpath = ["src"]
```

**Step 3: Create empty __init__.py files**

`src/openvibe_sdk/__init__.py`:
```python
"""OpenVibe SDK — 4-layer framework for human+agent collaboration."""
```

`src/openvibe_sdk/llm/__init__.py`:
```python
"""LLM types, protocols, and providers."""
```

`src/openvibe_sdk/memory/__init__.py`:
```python
"""Memory protocols and stores."""
```

`tests/__init__.py`: empty file.

**Step 4: Write the smoke test**

`tests/test_imports.py`:
```python
def test_package_importable():
    import openvibe_sdk
    assert openvibe_sdk.__doc__ is not None
```

**Step 5: Create venv and run test**

```bash
cd v4/openvibe-sdk
python3.13 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest tests/test_imports.py -v
```

Expected: PASS

**Step 6: Commit**

```bash
git add v4/openvibe-sdk/
git commit -m "feat(sdk): scaffold openvibe-sdk package with pyproject.toml"
```

---

## Task 2: LLM Types + LLMProvider Protocol

**Files:**
- Modify: `v4/openvibe-sdk/src/openvibe_sdk/llm/__init__.py`
- Create: `v4/openvibe-sdk/tests/test_llm_types.py`

**Step 1: Write the failing tests**

`tests/test_llm_types.py`:
```python
from openvibe_sdk.llm import (
    LLMResponse,
    ToolCall,
    LLMProvider,
    MODEL_ALIASES,
    resolve_model,
)


def test_model_aliases_has_sonnet_haiku_opus():
    assert "sonnet" in MODEL_ALIASES
    assert "haiku" in MODEL_ALIASES
    assert "opus" in MODEL_ALIASES


def test_resolve_model_alias():
    assert resolve_model("sonnet") == "claude-sonnet-4-5-20250929"
    assert resolve_model("haiku") == "claude-haiku-4-5-20251001"
    assert resolve_model("opus") == "claude-opus-4-6"


def test_resolve_model_passthrough():
    assert resolve_model("claude-sonnet-4-5-20250929") == "claude-sonnet-4-5-20250929"
    assert resolve_model("custom-model") == "custom-model"


def test_tool_call_creation():
    tc = ToolCall(id="tc_1", name="search", input={"query": "test"})
    assert tc.id == "tc_1"
    assert tc.name == "search"
    assert tc.input == {"query": "test"}


def test_llm_response_defaults():
    r = LLMResponse(content="hello")
    assert r.content == "hello"
    assert r.tool_calls == []
    assert r.tokens_in == 0
    assert r.tokens_out == 0
    assert r.stop_reason == "end_turn"


def test_llm_response_with_tool_calls():
    tc = ToolCall(id="tc_1", name="search", input={"q": "x"})
    r = LLMResponse(content="", tool_calls=[tc], stop_reason="tool_use")
    assert len(r.tool_calls) == 1
    assert r.stop_reason == "tool_use"


def test_llm_provider_is_protocol():
    """LLMProvider should be a Protocol, not a concrete class."""
    import typing
    assert issubclass(type(LLMProvider), type(typing.Protocol))
```

**Step 2: Run tests to verify they fail**

```bash
cd v4/openvibe-sdk && source .venv/bin/activate
pytest tests/test_llm_types.py -v
```

Expected: FAIL — cannot import names from `openvibe_sdk.llm`

**Step 3: Implement LLM types**

`src/openvibe_sdk/llm/__init__.py`:
```python
"""LLM types, protocols, and providers."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Protocol, runtime_checkable

MODEL_ALIASES: dict[str, str] = {
    "sonnet": "claude-sonnet-4-5-20250929",
    "haiku": "claude-haiku-4-5-20251001",
    "opus": "claude-opus-4-6",
}


def resolve_model(name: str) -> str:
    """Resolve a model alias to its full model ID."""
    return MODEL_ALIASES.get(name, name)


@dataclass
class ToolCall:
    """A tool call from the LLM response."""

    id: str
    name: str
    input: dict[str, Any]


@dataclass
class LLMResponse:
    """Response from an LLM call."""

    content: str
    tool_calls: list[ToolCall] = field(default_factory=list)
    tokens_in: int = 0
    tokens_out: int = 0
    model: str = ""
    stop_reason: str = "end_turn"
    raw_content: Any = None


@runtime_checkable
class LLMProvider(Protocol):
    """Protocol for LLM providers. Implement this to add new LLM backends."""

    def call(
        self,
        *,
        system: str,
        messages: list[dict],
        model: str = "haiku",
        max_tokens: int = 4096,
        temperature: float = 0.7,
        tools: list[dict] | None = None,
    ) -> LLMResponse: ...
```

**Step 4: Run tests to verify they pass**

```bash
pytest tests/test_llm_types.py -v
```

Expected: all PASS

**Step 5: Commit**

```bash
git add v4/openvibe-sdk/src/openvibe_sdk/llm/__init__.py v4/openvibe-sdk/tests/test_llm_types.py
git commit -m "feat(sdk): add LLM types, LLMProvider protocol, model aliases"
```

---

## Task 3: AnthropicProvider

**Files:**
- Create: `v4/openvibe-sdk/src/openvibe_sdk/llm/anthropic.py`
- Create: `v4/openvibe-sdk/tests/test_anthropic_provider.py`

**Step 1: Write the failing tests**

`tests/test_anthropic_provider.py`:
```python
from unittest.mock import MagicMock

from openvibe_sdk.llm import LLMResponse, ToolCall
from openvibe_sdk.llm.anthropic import AnthropicProvider


def _mock_text_response(text="Hello", model="claude-haiku-4-5-20251001"):
    """Create a mock Anthropic API response with text content."""
    block = MagicMock()
    block.type = "text"
    block.text = text

    response = MagicMock()
    response.content = [block]
    response.usage.input_tokens = 10
    response.usage.output_tokens = 20
    response.stop_reason = "end_turn"
    return response


def _mock_tool_response():
    """Create a mock Anthropic API response with tool use."""
    text_block = MagicMock()
    text_block.type = "text"
    text_block.text = "I'll search for that."

    tool_block = MagicMock()
    tool_block.type = "tool_use"
    tool_block.id = "toolu_123"
    tool_block.name = "web_search"
    tool_block.input = {"query": "OpenVibe"}

    response = MagicMock()
    response.content = [text_block, tool_block]
    response.usage.input_tokens = 15
    response.usage.output_tokens = 30
    response.stop_reason = "tool_use"
    return response


def test_call_text_response(mocker):
    mock_client = MagicMock()
    mock_client.messages.create.return_value = _mock_text_response("Test output")
    mocker.patch(
        "openvibe_sdk.llm.anthropic.Anthropic", return_value=mock_client
    )

    provider = AnthropicProvider(api_key="test-key")
    result = provider.call(
        system="You are helpful.",
        messages=[{"role": "user", "content": "Hello"}],
        model="haiku",
    )

    assert isinstance(result, LLMResponse)
    assert result.content == "Test output"
    assert result.tool_calls == []
    assert result.tokens_in == 10
    assert result.tokens_out == 20
    assert result.stop_reason == "end_turn"
    assert result.model == "claude-haiku-4-5-20251001"


def test_call_resolves_model_alias(mocker):
    mock_client = MagicMock()
    mock_client.messages.create.return_value = _mock_text_response()
    mocker.patch(
        "openvibe_sdk.llm.anthropic.Anthropic", return_value=mock_client
    )

    provider = AnthropicProvider()
    provider.call(
        system="test",
        messages=[{"role": "user", "content": "hi"}],
        model="sonnet",
    )

    call_kwargs = mock_client.messages.create.call_args[1]
    assert call_kwargs["model"] == "claude-sonnet-4-5-20250929"


def test_call_with_tools(mocker):
    mock_client = MagicMock()
    mock_client.messages.create.return_value = _mock_tool_response()
    mocker.patch(
        "openvibe_sdk.llm.anthropic.Anthropic", return_value=mock_client
    )

    tools = [{"name": "web_search", "description": "Search", "input_schema": {}}]
    provider = AnthropicProvider()
    result = provider.call(
        system="test",
        messages=[{"role": "user", "content": "search"}],
        tools=tools,
    )

    assert result.content == "I'll search for that."
    assert len(result.tool_calls) == 1
    assert result.tool_calls[0].name == "web_search"
    assert result.tool_calls[0].id == "toolu_123"
    assert result.tool_calls[0].input == {"query": "OpenVibe"}
    assert result.stop_reason == "tool_use"

    call_kwargs = mock_client.messages.create.call_args[1]
    assert "tools" in call_kwargs


def test_call_without_tools_omits_param(mocker):
    mock_client = MagicMock()
    mock_client.messages.create.return_value = _mock_text_response()
    mocker.patch(
        "openvibe_sdk.llm.anthropic.Anthropic", return_value=mock_client
    )

    provider = AnthropicProvider()
    provider.call(
        system="test",
        messages=[{"role": "user", "content": "hi"}],
    )

    call_kwargs = mock_client.messages.create.call_args[1]
    assert "tools" not in call_kwargs
```

**Step 2: Run tests to verify they fail**

```bash
pytest tests/test_anthropic_provider.py -v
```

Expected: FAIL — `ModuleNotFoundError: No module named 'openvibe_sdk.llm.anthropic'`

**Step 3: Implement AnthropicProvider**

`src/openvibe_sdk/llm/anthropic.py`:
```python
"""Anthropic LLM provider — wraps the anthropic SDK."""

from __future__ import annotations

from anthropic import Anthropic

from openvibe_sdk.llm import LLMResponse, ToolCall, resolve_model


class AnthropicProvider:
    """LLMProvider implementation using Anthropic's Claude API."""

    def __init__(self, api_key: str | None = None):
        self._client = Anthropic(api_key=api_key)

    def call(
        self,
        *,
        system: str,
        messages: list[dict],
        model: str = "haiku",
        max_tokens: int = 4096,
        temperature: float = 0.7,
        tools: list[dict] | None = None,
    ) -> LLMResponse:
        resolved = resolve_model(model)
        kwargs: dict = dict(
            model=resolved,
            max_tokens=max_tokens,
            temperature=temperature,
            system=system,
            messages=messages,
        )
        if tools:
            kwargs["tools"] = tools

        response = self._client.messages.create(**kwargs)

        content = ""
        tool_calls: list[ToolCall] = []
        for block in response.content:
            if block.type == "text":
                content = block.text
            elif block.type == "tool_use":
                tool_calls.append(
                    ToolCall(id=block.id, name=block.name, input=block.input)
                )

        return LLMResponse(
            content=content,
            tool_calls=tool_calls,
            tokens_in=response.usage.input_tokens,
            tokens_out=response.usage.output_tokens,
            model=resolved,
            stop_reason=response.stop_reason,
            raw_content=response.content,
        )
```

**Step 4: Run tests to verify they pass**

```bash
pytest tests/test_anthropic_provider.py -v
```

Expected: all PASS

**Step 5: Commit**

```bash
git add v4/openvibe-sdk/src/openvibe_sdk/llm/anthropic.py v4/openvibe-sdk/tests/test_anthropic_provider.py
git commit -m "feat(sdk): add AnthropicProvider — wraps anthropic SDK"
```

---

## Task 4: Memory Protocol + InMemoryStore

**Files:**
- Modify: `v4/openvibe-sdk/src/openvibe_sdk/memory/__init__.py`
- Create: `v4/openvibe-sdk/src/openvibe_sdk/memory/in_memory.py`
- Create: `v4/openvibe-sdk/tests/test_memory.py`

**Step 1: Write the failing tests**

`tests/test_memory.py`:
```python
import typing

from openvibe_sdk.memory import MemoryEntry, MemoryProvider
from openvibe_sdk.memory.in_memory import InMemoryStore


def test_memory_provider_is_protocol():
    assert issubclass(type(MemoryProvider), type(typing.Protocol))


def test_memory_entry_creation():
    entry = MemoryEntry(key="k1", content="hello", namespace="ns")
    assert entry.key == "k1"
    assert entry.content == "hello"
    assert entry.namespace == "ns"
    assert entry.created_at is not None


def test_in_memory_store_implements_protocol():
    store = InMemoryStore()
    assert isinstance(store, MemoryProvider)


def test_store_and_recall():
    store = InMemoryStore()
    store.store("ns", "k1", "value1")
    store.store("ns", "k2", "value2")

    results = store.recall("ns", "")
    assert len(results) == 2


def test_recall_with_query_filter():
    store = InMemoryStore()
    store.store("ns", "k1", "webinar leads convert 2x")
    store.store("ns", "k2", "enterprise needs VP sponsor")
    store.store("ns", "k3", "cold email has low response")

    results = store.recall("ns", "webinar")
    assert len(results) == 1
    assert results[0].content == "webinar leads convert 2x"


def test_recall_respects_limit():
    store = InMemoryStore()
    for i in range(20):
        store.store("ns", f"k{i}", f"memory {i}")

    results = store.recall("ns", "", limit=5)
    assert len(results) == 5


def test_recall_empty_namespace():
    store = InMemoryStore()
    results = store.recall("nonexistent", "")
    assert results == []


def test_delete():
    store = InMemoryStore()
    store.store("ns", "k1", "value1")
    store.delete("ns", "k1")

    results = store.recall("ns", "")
    assert len(results) == 0


def test_delete_nonexistent_key():
    store = InMemoryStore()
    store.delete("ns", "missing")  # should not raise


def test_namespace_isolation():
    store = InMemoryStore()
    store.store("ns1", "k1", "first")
    store.store("ns2", "k1", "second")

    r1 = store.recall("ns1", "")
    r2 = store.recall("ns2", "")
    assert len(r1) == 1
    assert r1[0].content == "first"
    assert len(r2) == 1
    assert r2[0].content == "second"
```

**Step 2: Run tests to verify they fail**

```bash
pytest tests/test_memory.py -v
```

Expected: FAIL — cannot import `MemoryEntry`, `MemoryProvider` from `openvibe_sdk.memory`

**Step 3: Implement memory protocol and InMemoryStore**

`src/openvibe_sdk/memory/__init__.py`:
```python
"""Memory protocols and stores."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Protocol, runtime_checkable


@dataclass
class MemoryEntry:
    """A single memory entry."""

    key: str
    content: Any
    namespace: str = ""
    created_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    metadata: dict[str, Any] = field(default_factory=dict)


@runtime_checkable
class MemoryProvider(Protocol):
    """Protocol for memory backends."""

    def store(self, namespace: str, key: str, value: Any) -> None: ...

    def recall(
        self, namespace: str, query: str, limit: int = 10
    ) -> list[MemoryEntry]: ...

    def delete(self, namespace: str, key: str) -> None: ...
```

`src/openvibe_sdk/memory/in_memory.py`:
```python
"""In-memory store — dict-based, for dev/test."""

from __future__ import annotations

from typing import Any

from openvibe_sdk.memory import MemoryEntry


class InMemoryStore:
    """Simple in-memory MemoryProvider for development and testing."""

    def __init__(self) -> None:
        self._store: dict[str, dict[str, MemoryEntry]] = {}

    def store(self, namespace: str, key: str, value: Any) -> None:
        if namespace not in self._store:
            self._store[namespace] = {}
        self._store[namespace][key] = MemoryEntry(
            key=key, content=value, namespace=namespace
        )

    def recall(
        self, namespace: str, query: str, limit: int = 10
    ) -> list[MemoryEntry]:
        entries = list(self._store.get(namespace, {}).values())
        if query:
            entries = [
                e
                for e in entries
                if query.lower() in str(e.content).lower()
            ]
        return entries[:limit]

    def delete(self, namespace: str, key: str) -> None:
        if namespace in self._store:
            self._store[namespace].pop(key, None)
```

**Step 4: Run tests to verify they pass**

```bash
pytest tests/test_memory.py -v
```

Expected: all PASS

**Step 5: Commit**

```bash
git add v4/openvibe-sdk/src/openvibe_sdk/memory/ v4/openvibe-sdk/tests/test_memory.py
git commit -m "feat(sdk): add MemoryProvider protocol + InMemoryStore"
```

---

## Task 5: Tool Schema Converter

**Files:**
- Create: `v4/openvibe-sdk/src/openvibe_sdk/tools.py`
- Create: `v4/openvibe-sdk/tests/test_tools.py`

**Step 1: Write the failing tests**

`tests/test_tools.py`:
```python
from openvibe_sdk.tools import function_to_schema


def test_simple_function():
    def greet(name: str) -> str:
        """Say hello to someone."""
        return f"Hello {name}"

    schema = function_to_schema(greet)
    assert schema["name"] == "greet"
    assert schema["description"] == "Say hello to someone."
    assert schema["input_schema"]["type"] == "object"
    assert schema["input_schema"]["properties"]["name"]["type"] == "string"
    assert "name" in schema["input_schema"]["required"]


def test_multiple_params():
    def search(query: str, limit: int) -> str:
        """Search for items."""
        return ""

    schema = function_to_schema(search)
    props = schema["input_schema"]["properties"]
    assert "query" in props
    assert "limit" in props
    assert props["query"]["type"] == "string"
    assert props["limit"]["type"] == "integer"
    assert set(schema["input_schema"]["required"]) == {"query", "limit"}


def test_optional_param_with_default():
    def fetch(url: str, timeout: int = 30) -> str:
        """Fetch a URL."""
        return ""

    schema = function_to_schema(fetch)
    assert schema["input_schema"]["required"] == ["url"]
    assert "timeout" in schema["input_schema"]["properties"]


def test_bool_and_float_types():
    def configure(verbose: bool, threshold: float) -> str:
        """Configure settings."""
        return ""

    schema = function_to_schema(configure)
    props = schema["input_schema"]["properties"]
    assert props["verbose"]["type"] == "boolean"
    assert props["threshold"]["type"] == "number"


def test_no_docstring():
    def mystery(x: str) -> str:
        return x

    schema = function_to_schema(mystery)
    assert schema["description"] == ""


def test_no_type_hints_defaults_to_string():
    def untyped(x):
        """Do something."""
        return x

    schema = function_to_schema(untyped)
    assert schema["input_schema"]["properties"]["x"]["type"] == "string"
```

**Step 2: Run tests to verify they fail**

```bash
pytest tests/test_tools.py -v
```

Expected: FAIL — `ModuleNotFoundError: No module named 'openvibe_sdk.tools'`

**Step 3: Implement tool schema converter**

`src/openvibe_sdk/tools.py`:
```python
"""Tool schema converter — plain Python functions to Anthropic tool schema."""

from __future__ import annotations

import inspect
from typing import Any, get_type_hints


def function_to_schema(func: Any) -> dict[str, Any]:
    """Convert a plain Python function to Anthropic tool schema.

    Uses function name, type hints, and docstring. No decorator needed.
    """
    try:
        hints = get_type_hints(func)
    except Exception:
        hints = {}
    sig = inspect.signature(func)

    properties: dict[str, dict] = {}
    required: list[str] = []

    for name, param in sig.parameters.items():
        if name == "self":
            continue
        type_hint = hints.get(name, str)
        prop: dict[str, str] = {"type": _python_type_to_json(type_hint)}
        properties[name] = prop
        if param.default is inspect.Parameter.empty:
            required.append(name)

    return {
        "name": func.__name__,
        "description": (func.__doc__ or "").strip(),
        "input_schema": {
            "type": "object",
            "properties": properties,
            "required": required,
        },
    }


_TYPE_MAP: dict[type, str] = {
    str: "string",
    int: "integer",
    float: "number",
    bool: "boolean",
    list: "array",
    dict: "object",
}


def _python_type_to_json(type_hint: Any) -> str:
    """Map Python type hint to JSON Schema type string."""
    return _TYPE_MAP.get(type_hint, "string")
```

**Step 4: Run tests to verify they pass**

```bash
pytest tests/test_tools.py -v
```

Expected: all PASS

**Step 5: Commit**

```bash
git add v4/openvibe-sdk/src/openvibe_sdk/tools.py v4/openvibe-sdk/tests/test_tools.py
git commit -m "feat(sdk): add function_to_schema — converts functions to Anthropic tool schema"
```

---

## Task 6: Operator Base Class + @llm_node Decorator

**Files:**
- Create: `v4/openvibe-sdk/src/openvibe_sdk/operator.py`
- Create: `v4/openvibe-sdk/tests/test_llm_node.py`

**Step 1: Write the failing tests**

`tests/test_llm_node.py`:
```python
import json

from openvibe_sdk.llm import LLMResponse
from openvibe_sdk.operator import Operator, llm_node


class FakeLLM:
    """Fake LLM provider for testing."""

    def __init__(self, response_content="test output"):
        self.response_content = response_content
        self.last_call = None

    def call(self, *, system, messages, **kwargs):
        self.last_call = {
            "system": system,
            "messages": messages,
            **kwargs,
        }
        return LLMResponse(
            content=self.response_content,
            tokens_in=10,
            tokens_out=20,
            model=kwargs.get("model", "haiku"),
        )


class TestOperator(Operator):
    operator_id = "test_op"

    @llm_node(model="sonnet", temperature=0.3, output_key="result")
    def analyze(self, state):
        """You are a test analyst."""
        return f"Analyze: {state['input']}"


def test_operator_has_id():
    op = TestOperator()
    assert op.operator_id == "test_op"


def test_operator_accepts_llm():
    llm = FakeLLM()
    op = TestOperator(llm=llm)
    assert op.llm is llm


def test_llm_node_uses_docstring_as_system_prompt():
    llm = FakeLLM()
    op = TestOperator(llm=llm)
    op.analyze({"input": "hello"})

    assert llm.last_call["system"] == "You are a test analyst."


def test_llm_node_uses_return_as_user_message():
    llm = FakeLLM()
    op = TestOperator(llm=llm)
    op.analyze({"input": "hello"})

    messages = llm.last_call["messages"]
    assert len(messages) == 1
    assert messages[0]["role"] == "user"
    assert messages[0]["content"] == "Analyze: hello"


def test_llm_node_passes_model_and_temperature():
    llm = FakeLLM()
    op = TestOperator(llm=llm)
    op.analyze({"input": "x"})

    assert llm.last_call["model"] == "sonnet"
    assert llm.last_call["temperature"] == 0.3


def test_llm_node_writes_output_key():
    llm = FakeLLM(response_content="analysis result")
    op = TestOperator(llm=llm)
    state = {"input": "hello"}
    result = op.analyze(state)

    assert result["result"] == "analysis result"


def test_llm_node_auto_parses_json():
    json_response = json.dumps({"score": 85, "label": "high"})
    llm = FakeLLM(response_content=json_response)
    op = TestOperator(llm=llm)
    state = {"input": "x"}
    result = op.analyze(state)

    assert isinstance(result["result"], dict)
    assert result["result"]["score"] == 85


def test_llm_node_returns_raw_string_on_non_json():
    llm = FakeLLM(response_content="just plain text")
    op = TestOperator(llm=llm)
    state = {"input": "x"}
    result = op.analyze(state)

    assert result["result"] == "just plain text"


def test_llm_node_returns_state():
    llm = FakeLLM()
    op = TestOperator(llm=llm)
    state = {"input": "x", "existing": "preserved"}
    result = op.analyze(state)

    assert result["existing"] == "preserved"
    assert "result" in result


def test_llm_node_no_output_key():
    class NoKeyOp(Operator):
        @llm_node(model="haiku")
        def process(self, state):
            """You are a processor."""
            return "process this"

    llm = FakeLLM(response_content="done")
    op = NoKeyOp(llm=llm)
    state = {"input": "x"}
    result = op.process(state)

    assert result is state  # state returned but no key written


def test_llm_node_marks_method():
    op = TestOperator()
    assert hasattr(op.analyze, "_is_llm_node")
    assert op.analyze._is_llm_node is True
```

**Step 2: Run tests to verify they fail**

```bash
pytest tests/test_llm_node.py -v
```

Expected: FAIL — `ModuleNotFoundError: No module named 'openvibe_sdk.operator'`

**Step 3: Implement Operator + @llm_node**

`src/openvibe_sdk/operator.py`:
```python
"""Operator base class + @llm_node and @agent_node decorators."""

from __future__ import annotations

import functools
import json
from typing import Any


class Operator:
    """Base class for all operators.

    Provides self.llm (LLMProvider) and self.config to decorated methods.
    """

    operator_id: str = ""

    def __init__(self, llm: Any = None, config: Any = None) -> None:
        self.llm = llm
        self.config = config


def llm_node(
    model: str = "haiku",
    temperature: float = 0.7,
    max_tokens: int = 4096,
    output_key: str | None = None,
) -> Any:
    """Decorator: single LLM call.

    - Docstring = system prompt
    - Return value = user message
    - Auto JSON parse if response is valid JSON
    - state[output_key] = result (if output_key set)
    """

    def decorator(method: Any) -> Any:
        @functools.wraps(method)
        def wrapper(self: Operator, state: dict) -> dict:
            system_prompt = (method.__doc__ or "").strip()
            user_message = method(self, state)

            response = self.llm.call(
                system=system_prompt,
                messages=[{"role": "user", "content": user_message}],
                model=model,
                max_tokens=max_tokens,
                temperature=temperature,
            )

            result = _try_json_parse(response.content)

            if output_key:
                state[output_key] = result

            return state

        wrapper._is_llm_node = True
        wrapper._node_config = {
            "model": model,
            "temperature": temperature,
            "output_key": output_key,
        }
        return wrapper

    return decorator


def _try_json_parse(text: str) -> Any:
    """Try to parse text as JSON; return raw string on failure."""
    try:
        return json.loads(text)
    except (json.JSONDecodeError, TypeError):
        return text
```

**Step 4: Run tests to verify they pass**

```bash
pytest tests/test_llm_node.py -v
```

Expected: all PASS

**Step 5: Commit**

```bash
git add v4/openvibe-sdk/src/openvibe_sdk/operator.py v4/openvibe-sdk/tests/test_llm_node.py
git commit -m "feat(sdk): add Operator base class + @llm_node decorator"
```

---

## Task 7: @agent_node Decorator

**Files:**
- Modify: `v4/openvibe-sdk/src/openvibe_sdk/operator.py`
- Create: `v4/openvibe-sdk/tests/test_agent_node.py`

**Step 1: Write the failing tests**

`tests/test_agent_node.py`:
```python
import json

from openvibe_sdk.llm import LLMResponse, ToolCall
from openvibe_sdk.operator import Operator, agent_node


class FakeAgentLLM:
    """Fake LLM that simulates a tool-use conversation."""

    def __init__(self, responses: list[LLMResponse]):
        self.responses = list(responses)
        self.calls: list[dict] = []

    def call(self, *, system, messages, **kwargs):
        self.calls.append({
            "system": system,
            "messages": messages,
            **kwargs,
        })
        return self.responses.pop(0)


def _text_response(content="done"):
    return LLMResponse(content=content, stop_reason="end_turn")


def _tool_response(tool_name="search", tool_input=None):
    return LLMResponse(
        content="I'll use a tool.",
        tool_calls=[
            ToolCall(id="tc_1", name=tool_name, input=tool_input or {})
        ],
        stop_reason="tool_use",
    )


# --- Test tools ---

def search(query: str) -> str:
    """Search for information."""
    return f"Results for: {query}"


def calculator(expression: str) -> str:
    """Evaluate a math expression."""
    return str(eval(expression))


# --- Operator ---

class ResearchOp(Operator):
    operator_id = "research"

    @agent_node(tools=[search], output_key="findings")
    def investigate(self, state):
        """You are a research analyst."""
        return f"Investigate: {state['topic']}"


def test_agent_node_no_tools_returns_immediately():
    """If LLM responds with text (no tool calls), return immediately."""
    llm = FakeAgentLLM([_text_response("final answer")])
    op = ResearchOp(llm=llm)
    state = {"topic": "AI"}
    result = op.investigate(state)

    assert result["findings"] == "final answer"
    assert len(llm.calls) == 1


def test_agent_node_tool_loop():
    """LLM calls tool, gets result, then responds with text."""
    llm = FakeAgentLLM([
        _tool_response("search", {"query": "AI trends"}),
        _text_response("AI is growing fast"),
    ])
    op = ResearchOp(llm=llm)
    state = {"topic": "AI"}
    result = op.investigate(state)

    assert result["findings"] == "AI is growing fast"
    assert len(llm.calls) == 2

    # Second call should include tool result in messages
    second_messages = llm.calls[1]["messages"]
    assert len(second_messages) == 3  # user + assistant + tool_result


def test_agent_node_multi_step_loop():
    """LLM calls tools multiple times before finishing."""
    llm = FakeAgentLLM([
        _tool_response("search", {"query": "step 1"}),
        _tool_response("search", {"query": "step 2"}),
        _text_response("combined results"),
    ])
    op = ResearchOp(llm=llm)
    state = {"topic": "deep research"}
    result = op.investigate(state)

    assert result["findings"] == "combined results"
    assert len(llm.calls) == 3


def test_agent_node_executes_real_tool():
    """Tool function is actually called with the LLM's input."""
    calls = []
    original_search = search

    def tracking_search(query: str) -> str:
        calls.append(query)
        return original_search(query)

    class TrackOp(Operator):
        @agent_node(tools=[tracking_search], output_key="out")
        def investigate(self, state):
            """You research things."""
            return "research AI"

    llm = FakeAgentLLM([
        _tool_response("tracking_search", {"query": "test query"}),
        _text_response("done"),
    ])
    op = TrackOp(llm=llm)
    op.investigate({"x": 1})

    assert calls == ["test query"]


def test_agent_node_max_steps():
    """Respects max_steps limit."""

    class LimitedOp(Operator):
        @agent_node(tools=[search], output_key="out", max_steps=2)
        def investigate(self, state):
            """You research things."""
            return "go"

    # LLM keeps requesting tools beyond max_steps
    llm = FakeAgentLLM([
        _tool_response("search", {"query": "1"}),
        _tool_response("search", {"query": "2"}),
        _tool_response("search", {"query": "3"}),  # should not be reached
    ])
    op = LimitedOp(llm=llm)
    result = op.investigate({"x": 1})

    assert len(llm.calls) == 2  # stopped after 2 steps


def test_agent_node_auto_parses_json():
    json_output = json.dumps({"summary": "AI is important"})
    llm = FakeAgentLLM([_text_response(json_output)])
    op = ResearchOp(llm=llm)
    result = op.investigate({"topic": "AI"})

    assert isinstance(result["findings"], dict)
    assert result["findings"]["summary"] == "AI is important"


def test_agent_node_passes_tool_schemas():
    llm = FakeAgentLLM([_text_response("done")])
    op = ResearchOp(llm=llm)
    op.investigate({"topic": "x"})

    tools_sent = llm.calls[0].get("tools")
    assert tools_sent is not None
    assert len(tools_sent) == 1
    assert tools_sent[0]["name"] == "search"


def test_agent_node_marks_method():
    op = ResearchOp()
    assert hasattr(op.investigate, "_is_agent_node")
    assert op.investigate._is_agent_node is True


def test_agent_node_uses_docstring_as_system():
    llm = FakeAgentLLM([_text_response("done")])
    op = ResearchOp(llm=llm)
    op.investigate({"topic": "x"})

    assert llm.calls[0]["system"] == "You are a research analyst."


def test_agent_node_unknown_tool():
    """Unknown tool name returns error message, doesn't crash."""
    llm = FakeAgentLLM([
        _tool_response("nonexistent_tool", {"x": 1}),
        _text_response("ok"),
    ])
    op = ResearchOp(llm=llm)
    result = op.investigate({"topic": "x"})

    # Should complete without raising
    assert result["findings"] == "ok"
```

**Step 2: Run tests to verify they fail**

```bash
pytest tests/test_agent_node.py -v
```

Expected: FAIL — `ImportError: cannot import name 'agent_node' from 'openvibe_sdk.operator'`

**Step 3: Add @agent_node to operator.py**

Append to `src/openvibe_sdk/operator.py` (after the `llm_node` function):

```python
def agent_node(
    tools: list | None = None,
    model: str = "sonnet",
    temperature: float = 0.7,
    max_tokens: int = 4096,
    output_key: str | None = None,
    max_steps: int | None = None,
) -> Any:
    """Decorator: Pi-style agent loop.

    - Tools = plain Python functions (auto-converted to Anthropic schema)
    - Loops until LLM responds with text (no tool calls)
    - Optional max_steps safety valve
    """
    from openvibe_sdk.tools import function_to_schema

    tool_functions = {t.__name__: t for t in (tools or [])}
    tool_schemas = [function_to_schema(t) for t in (tools or [])]

    def decorator(method: Any) -> Any:
        @functools.wraps(method)
        def wrapper(self: Operator, state: dict) -> dict:
            system_prompt = (method.__doc__ or "").strip()
            user_message = method(self, state)

            messages: list[dict] = [
                {"role": "user", "content": user_message}
            ]
            steps = 0
            last_response = None

            while True:
                if max_steps is not None and steps >= max_steps:
                    break

                response = self.llm.call(
                    system=system_prompt,
                    messages=messages,
                    model=model,
                    max_tokens=max_tokens,
                    temperature=temperature,
                    tools=tool_schemas or None,
                )
                last_response = response

                if not response.tool_calls:
                    result = _try_json_parse(response.content)
                    if output_key:
                        state[output_key] = result
                    return state

                # Build assistant message with tool_use blocks
                assistant_content: list[dict] = []
                if response.content:
                    assistant_content.append(
                        {"type": "text", "text": response.content}
                    )
                for tc in response.tool_calls:
                    assistant_content.append(
                        {
                            "type": "tool_use",
                            "id": tc.id,
                            "name": tc.name,
                            "input": tc.input,
                        }
                    )
                messages.append(
                    {"role": "assistant", "content": assistant_content}
                )

                # Execute tools and build tool_result message
                tool_results: list[dict] = []
                for tc in response.tool_calls:
                    func = tool_functions.get(tc.name)
                    if func:
                        try:
                            tool_result = func(**tc.input)
                        except Exception as e:
                            tool_result = f"Error: {e}"
                    else:
                        tool_result = f"Unknown tool: {tc.name}"
                    tool_results.append(
                        {
                            "type": "tool_result",
                            "tool_use_id": tc.id,
                            "content": str(tool_result),
                        }
                    )
                messages.append({"role": "user", "content": tool_results})

                steps += 1

            # max_steps reached — use last response
            if last_response and output_key:
                state[output_key] = last_response.content
            return state

        wrapper._is_agent_node = True
        wrapper._node_config = {
            "model": model,
            "tools": [t.__name__ for t in (tools or [])],
            "output_key": output_key,
            "max_steps": max_steps,
        }
        return wrapper

    return decorator
```

**Step 4: Run tests to verify they pass**

```bash
pytest tests/test_agent_node.py -v
```

Expected: all PASS

**Step 5: Run all tests so far**

```bash
pytest tests/ -v
```

Expected: all PASS

**Step 6: Commit**

```bash
git add v4/openvibe-sdk/src/openvibe_sdk/operator.py v4/openvibe-sdk/tests/test_agent_node.py
git commit -m "feat(sdk): add @agent_node — Pi-style tool loop decorator"
```

---

## Task 8: Config Models + YAML Loader + OperatorRuntime

**Files:**
- Create: `v4/openvibe-sdk/src/openvibe_sdk/models.py`
- Create: `v4/openvibe-sdk/src/openvibe_sdk/config.py`
- Create: `v4/openvibe-sdk/src/openvibe_sdk/runtime.py`
- Create: `v4/openvibe-sdk/tests/test_config_models.py`
- Create: `v4/openvibe-sdk/tests/test_operator_runtime.py`

### Part A: Config models + YAML loader

**Step 1: Write the failing tests**

`tests/test_config_models.py`:
```python
import tempfile
from pathlib import Path

from openvibe_sdk.models import (
    NodeConfig,
    NodeType,
    OperatorConfig,
    TriggerConfig,
    TriggerType,
    WorkflowConfig,
)
from openvibe_sdk.config import load_operator_configs, load_prompt


def test_trigger_config():
    t = TriggerConfig(
        id="t1",
        type=TriggerType.CRON,
        schedule="0 9 * * 1-5",
        workflow="research",
    )
    assert t.id == "t1"
    assert t.type == TriggerType.CRON
    assert t.workflow == "research"


def test_node_config_defaults():
    n = NodeConfig(id="n1")
    assert n.type == NodeType.LOGIC
    assert n.model is None


def test_workflow_config():
    wf = WorkflowConfig(
        id="research",
        nodes=[
            NodeConfig(id="n1", type=NodeType.LLM, model="sonnet"),
            NodeConfig(id="n2"),
        ],
    )
    assert len(wf.nodes) == 2
    assert wf.checkpointed is True


def test_operator_config():
    op = OperatorConfig(
        id="company_intel",
        name="Company Intel",
        triggers=[
            TriggerConfig(
                id="t1", type=TriggerType.ON_DEMAND, workflow="research"
            )
        ],
        workflows=[
            WorkflowConfig(
                id="research",
                nodes=[NodeConfig(id="n1", type=NodeType.LLM)],
            )
        ],
    )
    assert op.id == "company_intel"
    assert len(op.triggers) == 1
    assert len(op.workflows) == 1
    assert op.enabled is True


def test_load_operator_configs_from_yaml():
    yaml_content = """
operators:
  - id: test_op
    name: Test Operator
    triggers:
      - id: t1
        type: on_demand
        workflow: wf1
    workflows:
      - id: wf1
        nodes:
          - id: n1
            type: llm
  - id: disabled_op
    name: Disabled Op
    enabled: false
    triggers: []
    workflows: []
"""
    with tempfile.TemporaryDirectory() as tmpdir:
        path = Path(tmpdir) / "operators.yaml"
        path.write_text(yaml_content)

        all_configs = load_operator_configs(str(path), enabled_only=False)
        assert len(all_configs) == 2

        enabled = load_operator_configs(str(path), enabled_only=True)
        assert len(enabled) == 1
        assert enabled[0].id == "test_op"


def test_load_prompt():
    with tempfile.TemporaryDirectory() as tmpdir:
        path = Path(tmpdir) / "prompt.md"
        path.write_text("You are a test agent.")

        content = load_prompt(str(path))
        assert content == "You are a test agent."
```

**Step 2: Run tests to verify they fail**

```bash
pytest tests/test_config_models.py -v
```

Expected: FAIL

**Step 3: Implement models.py and config.py**

`src/openvibe_sdk/models.py`:
```python
"""Config models for operators, workflows, nodes, and triggers."""

from __future__ import annotations

from enum import Enum

from pydantic import BaseModel, Field


class TriggerType(str, Enum):
    CRON = "cron"
    WEBHOOK = "webhook"
    ON_DEMAND = "on_demand"
    EVENT = "event"


class NodeType(str, Enum):
    LOGIC = "logic"
    LLM = "llm"


class TriggerConfig(BaseModel):
    id: str
    type: TriggerType
    schedule: str | None = None
    source: str | None = None
    workflow: str
    description: str = ""


class NodeConfig(BaseModel):
    id: str
    type: NodeType = NodeType.LOGIC
    model: str | None = None
    prompt_file: str | None = None


class WorkflowConfig(BaseModel):
    id: str
    description: str = ""
    nodes: list[NodeConfig]
    checkpointed: bool = True
    durable: bool = False
    max_duration_days: int | None = None
    timeout_minutes: int = 5


class OperatorConfig(BaseModel):
    id: str
    name: str
    owner: str = ""
    description: str = ""
    output_channels: list[str] = Field(default_factory=list)
    state_schema: str = ""
    triggers: list[TriggerConfig]
    workflows: list[WorkflowConfig]
    enabled: bool = True
```

`src/openvibe_sdk/config.py`:
```python
"""YAML config loader and prompt reader."""

from __future__ import annotations

from pathlib import Path

import yaml

from openvibe_sdk.models import OperatorConfig


def load_operator_configs(
    config_path: str,
    enabled_only: bool = False,
) -> list[OperatorConfig]:
    """Load operator configs from a YAML file."""
    with open(config_path) as f:
        data = yaml.safe_load(f)

    configs = [OperatorConfig(**op) for op in data["operators"]]
    if enabled_only:
        configs = [c for c in configs if c.enabled]
    return configs


def load_prompt(prompt_path: str) -> str:
    """Read a prompt file and return its content."""
    return Path(prompt_path).read_text()
```

**Step 4: Run tests to verify they pass**

```bash
pytest tests/test_config_models.py -v
```

Expected: all PASS

### Part B: OperatorRuntime

**Step 5: Write OperatorRuntime failing tests**

`tests/test_operator_runtime.py`:
```python
import tempfile
from pathlib import Path
from unittest.mock import MagicMock

import pytest

from openvibe_sdk.runtime import OperatorRuntime


YAML_CONTENT = """
operators:
  - id: op1
    name: Operator One
    triggers:
      - id: t1
        type: on_demand
        workflow: wf1
      - id: t2
        type: cron
        schedule: "0 9 * * *"
        workflow: wf2
    workflows:
      - id: wf1
        nodes:
          - id: n1
            type: llm
          - id: n2
            type: logic
      - id: wf2
        nodes:
          - id: n3
            type: llm
  - id: op2
    name: Operator Two
    enabled: false
    triggers: []
    workflows: []
"""


def _write_yaml(tmpdir):
    path = Path(tmpdir) / "operators.yaml"
    path.write_text(YAML_CONTENT)
    return str(path)


def test_from_yaml():
    with tempfile.TemporaryDirectory() as tmpdir:
        path = _write_yaml(tmpdir)
        runtime = OperatorRuntime.from_yaml(path, enabled_only=True)

        assert "op1" in runtime.operators
        assert "op2" not in runtime.operators


def test_from_yaml_all():
    with tempfile.TemporaryDirectory() as tmpdir:
        path = _write_yaml(tmpdir)
        runtime = OperatorRuntime.from_yaml(path, enabled_only=False)

        assert "op1" in runtime.operators
        assert "op2" in runtime.operators


def test_list_operators():
    with tempfile.TemporaryDirectory() as tmpdir:
        path = _write_yaml(tmpdir)
        runtime = OperatorRuntime.from_yaml(path)

        ops = runtime.list_operators()
        assert len(ops) == 1
        assert ops[0].id == "op1"


def test_get_operator():
    with tempfile.TemporaryDirectory() as tmpdir:
        path = _write_yaml(tmpdir)
        runtime = OperatorRuntime.from_yaml(path)

        op = runtime.get_operator("op1")
        assert op is not None
        assert op.name == "Operator One"

        assert runtime.get_operator("nonexistent") is None


def test_register_and_get_workflow():
    runtime = OperatorRuntime()
    factory = MagicMock()
    runtime.register_workflow("op1", "wf1", factory)

    assert runtime.get_workflow_factory("op1", "wf1") is factory
    assert runtime.get_workflow_factory("op1", "missing") is None


def test_activate():
    with tempfile.TemporaryDirectory() as tmpdir:
        path = _write_yaml(tmpdir)
        runtime = OperatorRuntime.from_yaml(path)

        mock_graph = MagicMock()
        mock_graph.invoke.return_value = {"output": "result"}
        factory = MagicMock(return_value=mock_graph)
        runtime.register_workflow("op1", "wf1", factory)

        result = runtime.activate("op1", "t1", {"input": "test"})
        assert result == {"output": "result"}
        factory.assert_called_once()
        mock_graph.invoke.assert_called_once_with({"input": "test"})


def test_activate_unknown_operator():
    runtime = OperatorRuntime()
    with pytest.raises(ValueError, match="Unknown operator"):
        runtime.activate("missing", "t1", {})


def test_activate_unknown_trigger():
    with tempfile.TemporaryDirectory() as tmpdir:
        path = _write_yaml(tmpdir)
        runtime = OperatorRuntime.from_yaml(path)

        with pytest.raises(ValueError, match="Unknown trigger"):
            runtime.activate("op1", "missing_trigger", {})


def test_activate_no_factory():
    with tempfile.TemporaryDirectory() as tmpdir:
        path = _write_yaml(tmpdir)
        runtime = OperatorRuntime.from_yaml(path)

        with pytest.raises(ValueError, match="No graph factory"):
            runtime.activate("op1", "t1", {})


def test_summary():
    with tempfile.TemporaryDirectory() as tmpdir:
        path = _write_yaml(tmpdir)
        runtime = OperatorRuntime.from_yaml(path)

        s = runtime.summary()
        assert s["operators"] == 1
        assert s["workflows"] == 2
        assert s["triggers"] == 2
        assert s["nodes"] == 3
        assert s["llm_nodes"] == 2
        assert s["logic_nodes"] == 1
```

**Step 6: Run tests to verify they fail**

```bash
pytest tests/test_operator_runtime.py -v
```

Expected: FAIL — `ModuleNotFoundError: No module named 'openvibe_sdk.runtime'`

**Step 7: Implement OperatorRuntime**

`src/openvibe_sdk/runtime.py`:
```python
"""OperatorRuntime + RoleRuntime — manages operators and roles."""

from __future__ import annotations

from typing import Any, Callable

from openvibe_sdk.config import load_operator_configs
from openvibe_sdk.models import OperatorConfig


class OperatorRuntime:
    """Central runtime for operators.

    Loads operators.yaml, indexes by ID, dispatches activations.
    """

    def __init__(self, config_path: str | None = None) -> None:
        self._config_path = config_path
        self.operators: dict[str, OperatorConfig] = {}
        self._workflow_factories: dict[str, dict[str, Callable]] = {}

    @classmethod
    def from_yaml(
        cls, config_path: str, enabled_only: bool = True
    ) -> OperatorRuntime:
        """Create runtime from a YAML config file."""
        runtime = cls(config_path=config_path)
        configs = load_operator_configs(config_path, enabled_only=enabled_only)
        for config in configs:
            runtime.operators[config.id] = config
        return runtime

    def register_workflow(
        self, operator_id: str, workflow_id: str, factory: Callable
    ) -> None:
        """Register a LangGraph graph factory for an operator workflow."""
        if operator_id not in self._workflow_factories:
            self._workflow_factories[operator_id] = {}
        self._workflow_factories[operator_id][workflow_id] = factory

    def get_workflow_factory(
        self, operator_id: str, workflow_id: str
    ) -> Callable | None:
        """Get the graph factory for a specific workflow."""
        return self._workflow_factories.get(operator_id, {}).get(workflow_id)

    def activate(
        self, operator_id: str, trigger_id: str, input_data: dict[str, Any]
    ) -> dict[str, Any]:
        """Activate: resolve trigger -> workflow -> run graph."""
        config = self.operators.get(operator_id)
        if not config:
            raise ValueError(f"Unknown operator: {operator_id}")

        trigger = next(
            (t for t in config.triggers if t.id == trigger_id), None
        )
        if not trigger:
            raise ValueError(
                f"Unknown trigger '{trigger_id}' for operator '{operator_id}'"
            )

        factory = self.get_workflow_factory(operator_id, trigger.workflow)
        if not factory:
            raise ValueError(
                f"No graph factory registered for "
                f"{operator_id}/{trigger.workflow}"
            )

        graph = factory()
        return graph.invoke(input_data)

    def list_operators(self) -> list[OperatorConfig]:
        """List all registered operators."""
        return list(self.operators.values())

    def get_operator(self, operator_id: str) -> OperatorConfig | None:
        """Get a single operator config by ID."""
        return self.operators.get(operator_id)

    def summary(self) -> dict[str, Any]:
        """System summary: operator counts, node counts, trigger counts."""
        total_workflows = 0
        total_nodes = 0
        total_triggers = 0
        logic_nodes = 0
        llm_nodes = 0

        for op in self.operators.values():
            total_triggers += len(op.triggers)
            for wf in op.workflows:
                total_workflows += 1
                for node in wf.nodes:
                    total_nodes += 1
                    if node.type.value == "logic":
                        logic_nodes += 1
                    elif node.type.value == "llm":
                        llm_nodes += 1

        return {
            "operators": len(self.operators),
            "workflows": total_workflows,
            "triggers": total_triggers,
            "nodes": total_nodes,
            "logic_nodes": logic_nodes,
            "llm_nodes": llm_nodes,
        }
```

**Step 8: Run all Task 8 tests**

```bash
pytest tests/test_config_models.py tests/test_operator_runtime.py -v
```

Expected: all PASS

**Step 9: Commit**

```bash
git add v4/openvibe-sdk/src/openvibe_sdk/models.py v4/openvibe-sdk/src/openvibe_sdk/config.py v4/openvibe-sdk/src/openvibe_sdk/runtime.py v4/openvibe-sdk/tests/test_config_models.py v4/openvibe-sdk/tests/test_operator_runtime.py
git commit -m "feat(sdk): add config models, YAML loader, OperatorRuntime"
```

---

## Task 9: Role + _RoleAwareLLM

**Files:**
- Create: `v4/openvibe-sdk/src/openvibe_sdk/role.py`
- Create: `v4/openvibe-sdk/tests/test_role.py`

**Step 1: Write the failing tests**

`tests/test_role.py`:
```python
import tempfile
from pathlib import Path

import pytest

from openvibe_sdk.llm import LLMResponse
from openvibe_sdk.memory.in_memory import InMemoryStore
from openvibe_sdk.operator import Operator, llm_node
from openvibe_sdk.role import Role, _RoleAwareLLM


# --- Fakes ---

class FakeLLM:
    def __init__(self, content="output"):
        self.content = content
        self.last_system = None

    def call(self, *, system, messages, **kwargs):
        self.last_system = system
        return LLMResponse(content=self.content)


# --- Operators ---

class RevenueOps(Operator):
    operator_id = "revenue_ops"

    @llm_node(model="sonnet", output_key="score")
    def qualify(self, state):
        """You are a lead qualifier."""
        return f"Score: {state['lead']}"


class ContentEngine(Operator):
    operator_id = "content_engine"

    @llm_node(model="haiku", output_key="draft")
    def write(self, state):
        """You are a writer."""
        return f"Write about: {state['topic']}"


# --- Role ---

class CRO(Role):
    role_id = "cro"
    soul = "You are the CRO. Data-driven and strategic."
    operators = [RevenueOps, ContentEngine]


class EmptyRole(Role):
    role_id = "empty"
    operators = []


# --- Tests ---


def test_role_has_id_and_soul():
    role = CRO(llm=FakeLLM())
    assert role.role_id == "cro"
    assert role.soul == "You are the CRO. Data-driven and strategic."


def test_get_operator():
    role = CRO(llm=FakeLLM())
    op = role.get_operator("revenue_ops")
    assert isinstance(op, RevenueOps)


def test_get_operator_caches():
    role = CRO(llm=FakeLLM())
    op1 = role.get_operator("revenue_ops")
    op2 = role.get_operator("revenue_ops")
    assert op1 is op2


def test_get_operator_unknown():
    role = CRO(llm=FakeLLM())
    with pytest.raises(ValueError, match="has no operator"):
        role.get_operator("nonexistent")


def test_operator_gets_role_aware_llm():
    llm = FakeLLM()
    role = CRO(llm=llm)
    op = role.get_operator("revenue_ops")
    assert isinstance(op.llm, _RoleAwareLLM)


def test_role_aware_llm_injects_soul():
    llm = FakeLLM()
    role = CRO(llm=llm)
    op = role.get_operator("revenue_ops")

    op.qualify({"lead": "Acme"})

    # System prompt should include soul + original docstring
    system = llm.last_system
    assert "You are the CRO" in system
    assert "You are a lead qualifier." in system


def test_role_aware_llm_injects_memories():
    llm = FakeLLM()
    memory = InMemoryStore()
    memory.store("cro", "m1", "Webinar leads convert 2x")
    memory.store("cro", "m2", "Enterprise needs VP sponsor")

    role = CRO(llm=llm, memory=memory)
    op = role.get_operator("revenue_ops")

    op.qualify({"lead": "test"})

    system = llm.last_system
    assert "Webinar leads convert 2x" in system
    assert "Enterprise needs VP sponsor" in system


def test_build_system_prompt_soul_only():
    role = CRO(llm=FakeLLM())
    prompt = role.build_system_prompt("Base prompt.")
    assert "You are the CRO" in prompt
    assert "Base prompt." in prompt


def test_build_system_prompt_no_soul():
    role = EmptyRole(llm=FakeLLM())
    prompt = role.build_system_prompt("Just base.")
    assert prompt == "Just base."


def test_build_system_prompt_with_memory():
    memory = InMemoryStore()
    memory.store("cro", "m1", "Important fact")

    role = CRO(llm=FakeLLM(), memory=memory)
    prompt = role.build_system_prompt("Base.", context="fact")
    assert "Important fact" in prompt
    assert "Relevant Memories" in prompt


def test_soul_from_file():
    with tempfile.TemporaryDirectory() as tmpdir:
        soul_path = Path(tmpdir) / "soul.md"
        soul_path.write_text("You are a visionary leader.")

        class FileRole(Role):
            role_id = "file_role"
            soul = str(soul_path)
            operators = []

        role = FileRole(llm=FakeLLM())
        prompt = role.build_system_prompt("Base.")
        assert "visionary leader" in prompt


def test_role_no_memory_no_crash():
    role = CRO(llm=FakeLLM())
    prompt = role.build_system_prompt("Base.", context="anything")
    # No memory provider — should just skip memory section
    assert "Base." in prompt
    assert "Relevant Memories" not in prompt
```

**Step 2: Run tests to verify they fail**

```bash
pytest tests/test_role.py -v
```

Expected: FAIL — `ModuleNotFoundError: No module named 'openvibe_sdk.role'`

**Step 3: Implement Role + _RoleAwareLLM**

`src/openvibe_sdk/role.py`:
```python
"""Role — identity layer (WHO the agent is)."""

from __future__ import annotations

from typing import Any

from openvibe_sdk.llm import LLMProvider, LLMResponse
from openvibe_sdk.memory import MemoryProvider
from openvibe_sdk.operator import Operator


class _RoleAwareLLM:
    """LLM wrapper that injects Role identity and memory into every call."""

    def __init__(self, role: Role, inner: LLMProvider) -> None:
        self._role = role
        self._inner = inner

    def call(
        self, *, system: str, messages: list[dict], **kwargs: Any
    ) -> LLMResponse:
        context = ""
        if messages:
            first_content = messages[0].get("content", "")
            context = (
                first_content
                if isinstance(first_content, str)
                else str(first_content)
            )
        augmented_system = self._role.build_system_prompt(system, context)
        return self._inner.call(
            system=augmented_system, messages=messages, **kwargs
        )


class Role:
    """Identity layer — WHO the agent is.

    Subclass and set role_id, soul, and operators.
    """

    role_id: str = ""
    soul: str = ""
    operators: list[type[Operator]] = []

    def __init__(
        self,
        llm: LLMProvider | None = None,
        memory: MemoryProvider | None = None,
        config: dict | None = None,
    ) -> None:
        self.llm = llm
        self.memory = memory
        self.config = config or {}
        self._operator_instances: dict[str, Operator] = {}

    def get_operator(self, operator_id: str) -> Operator:
        """Get or create an Operator instance with Role-aware LLM."""
        if operator_id not in self._operator_instances:
            for op_class in self.operators:
                if op_class.operator_id == operator_id:
                    wrapped_llm = (
                        _RoleAwareLLM(self, self.llm) if self.llm else None
                    )
                    self._operator_instances[operator_id] = op_class(
                        llm=wrapped_llm
                    )
                    break
            else:
                raise ValueError(
                    f"Role '{self.role_id}' has no operator '{operator_id}'"
                )
        return self._operator_instances[operator_id]

    def build_system_prompt(
        self, base_prompt: str, context: str = ""
    ) -> str:
        """Augment system prompt with soul + recalled memories."""
        soul_text = self._load_soul()
        memories = ""
        if self.memory and context:
            recalled = self.memory.recall(self.role_id, context)
            if recalled:
                memories = "\n## Relevant Memories\n" + "\n".join(
                    f"- {m.content}" for m in recalled
                )
        parts = [p for p in [soul_text, memories, base_prompt] if p]
        return "\n\n".join(parts)

    def _load_soul(self) -> str:
        if not self.soul:
            return ""
        if self.soul.endswith((".md", ".yaml", ".txt")):
            from openvibe_sdk.config import load_prompt

            return load_prompt(self.soul)
        return self.soul
```

**Step 4: Run tests to verify they pass**

```bash
pytest tests/test_role.py -v
```

Expected: all PASS

**Step 5: Commit**

```bash
git add v4/openvibe-sdk/src/openvibe_sdk/role.py v4/openvibe-sdk/tests/test_role.py
git commit -m "feat(sdk): add Role + _RoleAwareLLM — identity layer with soul + memory injection"
```

---

## Task 10: RoleRuntime + Public API + Integration Test

**Files:**
- Modify: `v4/openvibe-sdk/src/openvibe_sdk/runtime.py`
- Modify: `v4/openvibe-sdk/src/openvibe_sdk/__init__.py`
- Create: `v4/openvibe-sdk/tests/test_role_runtime.py`
- Create: `v4/openvibe-sdk/tests/test_integration.py`

### Part A: RoleRuntime

**Step 1: Write the failing tests**

`tests/test_role_runtime.py`:
```python
from unittest.mock import MagicMock

import pytest

from openvibe_sdk.llm import LLMResponse
from openvibe_sdk.memory.in_memory import InMemoryStore
from openvibe_sdk.operator import Operator, llm_node
from openvibe_sdk.role import Role
from openvibe_sdk.runtime import RoleRuntime


# --- Fakes ---

class FakeLLM:
    def __init__(self, content="result"):
        self.content = content
        self.calls = []

    def call(self, *, system, messages, **kwargs):
        self.calls.append({"system": system, "messages": messages, **kwargs})
        return LLMResponse(content=self.content)


# --- Operators ---

class RevenueOps(Operator):
    operator_id = "revenue_ops"

    @llm_node(model="sonnet", output_key="score")
    def qualify(self, state):
        """You qualify leads."""
        return f"Score: {state.get('lead', '')}"


class ContentEngine(Operator):
    operator_id = "content_engine"

    @llm_node(model="haiku", output_key="draft")
    def write(self, state):
        """You write content."""
        return f"Write about: {state.get('topic', '')}"


# --- Roles ---

class CRO(Role):
    role_id = "cro"
    soul = "You are the CRO."
    operators = [RevenueOps, ContentEngine]


class CMO(Role):
    role_id = "cmo"
    soul = "You are the CMO."
    operators = [ContentEngine]


# --- Tests ---


def test_role_runtime_registers_roles():
    runtime = RoleRuntime(roles=[CRO, CMO], llm=FakeLLM())
    assert len(runtime.list_roles()) == 2


def test_get_role():
    runtime = RoleRuntime(roles=[CRO], llm=FakeLLM())
    role = runtime.get_role("cro")
    assert role.role_id == "cro"


def test_get_role_unknown():
    runtime = RoleRuntime(roles=[CRO], llm=FakeLLM())
    with pytest.raises(ValueError, match="Unknown role"):
        runtime.get_role("nonexistent")


def test_activate():
    llm = FakeLLM(content="85")
    runtime = RoleRuntime(roles=[CRO], llm=llm)

    # Register a graph factory that uses the operator
    def qualify_factory(operator):
        mock_graph = MagicMock()
        mock_graph.invoke.return_value = operator.qualify({"lead": "Acme"})
        return mock_graph

    runtime.register_workflow("revenue_ops", "qualify", qualify_factory)

    result = runtime.activate("cro", "revenue_ops", "qualify", {"lead": "Acme"})
    assert result["score"] == "85"


def test_activate_unknown_role():
    runtime = RoleRuntime(roles=[CRO], llm=FakeLLM())
    with pytest.raises(ValueError, match="Unknown role"):
        runtime.activate("missing", "revenue_ops", "qualify", {})


def test_activate_unknown_operator():
    runtime = RoleRuntime(roles=[CRO], llm=FakeLLM())
    runtime.register_workflow("missing_op", "wf", lambda op: MagicMock())
    with pytest.raises(ValueError, match="has no operator"):
        runtime.activate("cro", "missing_op", "wf", {})


def test_activate_unknown_workflow():
    runtime = RoleRuntime(roles=[CRO], llm=FakeLLM())
    with pytest.raises(ValueError, match="No workflow"):
        runtime.activate("cro", "revenue_ops", "missing_wf", {})


def test_role_injects_memory():
    llm = FakeLLM(content="scored")
    memory = InMemoryStore()
    memory.store("cro", "m1", "Webinar leads convert 2x")

    runtime = RoleRuntime(roles=[CRO], llm=llm, memory=memory)

    def qualify_factory(operator):
        mock_graph = MagicMock()
        mock_graph.invoke.return_value = operator.qualify({"lead": "Acme"})
        return mock_graph

    runtime.register_workflow("revenue_ops", "qualify", qualify_factory)
    runtime.activate("cro", "revenue_ops", "qualify", {"lead": "Acme"})

    # The FakeLLM should have received soul + memory in system prompt
    system = llm.calls[0]["system"]
    assert "You are the CRO" in system
    assert "Webinar leads convert 2x" in system
```

**Step 2: Run tests to verify they fail**

```bash
pytest tests/test_role_runtime.py -v
```

Expected: FAIL — `ImportError: cannot import name 'RoleRuntime' from 'openvibe_sdk.runtime'`

**Step 3: Add RoleRuntime to runtime.py**

Append to `src/openvibe_sdk/runtime.py`:

```python
from openvibe_sdk.llm import LLMProvider
from openvibe_sdk.memory import MemoryProvider
from openvibe_sdk.operator import Operator
from openvibe_sdk.role import Role


class RoleRuntime:
    """Manages Roles + connects infrastructure.

    Workflow factories receive an Operator instance (with Role-aware LLM).
    Factory signature: (operator: Operator) -> CompiledGraph
    """

    def __init__(
        self,
        roles: list[type[Role]],
        llm: LLMProvider,
        memory: MemoryProvider | None = None,
        scheduler: Any = None,
    ) -> None:
        self.llm = llm
        self.memory = memory
        self.scheduler = scheduler
        self._roles: dict[str, Role] = {}
        self._workflow_factories: dict[str, dict[str, Callable]] = {}

        for role_class in roles:
            role = role_class(llm=llm, memory=memory)
            self._roles[role.role_id] = role

    def get_role(self, role_id: str) -> Role:
        """Get a Role by ID."""
        role = self._roles.get(role_id)
        if not role:
            raise ValueError(f"Unknown role: {role_id}")
        return role

    def register_workflow(
        self,
        operator_id: str,
        workflow_id: str,
        factory: Callable,
    ) -> None:
        """Register a graph factory.

        Factory signature: (operator: Operator) -> CompiledGraph
        """
        if operator_id not in self._workflow_factories:
            self._workflow_factories[operator_id] = {}
        self._workflow_factories[operator_id][workflow_id] = factory

    def activate(
        self,
        role_id: str,
        operator_id: str,
        workflow_id: str,
        input_data: dict,
    ) -> dict:
        """Activate: Role -> Operator -> workflow -> result."""
        role = self.get_role(role_id)
        operator = role.get_operator(operator_id)

        factories = self._workflow_factories.get(operator_id, {})
        factory = factories.get(workflow_id)
        if not factory:
            raise ValueError(
                f"No workflow '{workflow_id}' registered for "
                f"operator '{operator_id}'"
            )

        graph = factory(operator)
        return graph.invoke(input_data)

    def list_roles(self) -> list[Role]:
        """List all registered roles."""
        return list(self._roles.values())
```

**Step 4: Run tests to verify they pass**

```bash
pytest tests/test_role_runtime.py -v
```

Expected: all PASS

### Part B: Public API __init__.py

**Step 5: Wire up the public API**

`src/openvibe_sdk/__init__.py`:
```python
"""OpenVibe SDK — 4-layer framework for human+agent collaboration."""

from openvibe_sdk.operator import Operator, llm_node, agent_node
from openvibe_sdk.role import Role
from openvibe_sdk.runtime import OperatorRuntime, RoleRuntime

__all__ = [
    "Operator",
    "llm_node",
    "agent_node",
    "Role",
    "OperatorRuntime",
    "RoleRuntime",
]
```

### Part C: Integration test

**Step 6: Write integration test**

`tests/test_integration.py`:
```python
"""Integration test — full example using all 4 layers."""

from openvibe_sdk import (
    Operator,
    Role,
    RoleRuntime,
    agent_node,
    llm_node,
)
from openvibe_sdk.llm import LLMResponse, ToolCall
from openvibe_sdk.memory.in_memory import InMemoryStore


# --- Fake LLM for integration test ---

class IntegrationLLM:
    """Fake LLM that tracks all calls and returns canned responses."""

    def __init__(self):
        self.calls = []

    def call(self, *, system, messages, **kwargs):
        self.calls.append({"system": system, "messages": messages, **kwargs})

        # Determine which node is calling based on system prompt
        if "research analyst" in system.lower():
            # First call: use tool
            if len([c for c in self.calls if "research analyst" in c["system"].lower()]) == 1:
                return LLMResponse(
                    content="",
                    tool_calls=[
                        ToolCall(
                            id="tc_1",
                            name="fake_search",
                            input={"query": "company info"},
                        )
                    ],
                    stop_reason="tool_use",
                )
            # Second call: return text
            return LLMResponse(content="Acme is a B2B SaaS company.")

        if "qualifier" in system.lower():
            return LLMResponse(content='{"score": 85, "tier": "high"}')

        return LLMResponse(content="default response")


# --- Tools ---

def fake_search(query: str) -> str:
    """Search for company information."""
    return f"Found: {query} - Acme Corp, B2B SaaS, 200 employees"


# --- Layer 2: Operators ---

class CompanyIntel(Operator):
    operator_id = "company_intel"

    @agent_node(tools=[fake_search], output_key="research")
    def research(self, state):
        """You are a research analyst. Research the company thoroughly."""
        return f"Research: {state['company']}"

    @llm_node(model="sonnet", output_key="qualification")
    def qualify(self, state):
        """You are a lead qualifier. Score the prospect."""
        return f"Qualify based on: {state.get('research', 'unknown')}"


# --- Layer 3: Role ---

class CRO(Role):
    role_id = "cro"
    soul = "You are the CRO. Aggressive but data-driven."
    operators = [CompanyIntel]


# --- Integration Test ---

def test_full_stack():
    """Test the full 4-layer stack: Role -> Operator -> decorators -> LLM."""
    llm = IntegrationLLM()
    memory = InMemoryStore()
    memory.store("cro", "insight_1", "Webinar leads convert 2x vs cold")

    runtime = RoleRuntime(roles=[CRO], llm=llm, memory=memory)

    # Get the operator through the role to test Role-aware LLM
    role = runtime.get_role("cro")
    operator = role.get_operator("company_intel")

    # Test @agent_node (research with tool use)
    state = {"company": "Acme Corp"}
    result = operator.research(state)
    assert "research" in result
    assert isinstance(result["research"], str)

    # Test @llm_node (qualification)
    result["research"] = "Acme is a B2B SaaS company."
    result = operator.qualify(result)
    assert "qualification" in result

    # Verify soul injection happened
    # All calls should have CRO soul in system prompt
    for call in llm.calls:
        assert "CRO" in call["system"]

    # Verify memory injection happened
    # At least one call should include the memory
    memory_found = any(
        "Webinar leads convert 2x" in call["system"] for call in llm.calls
    )
    assert memory_found


def test_public_api_exports():
    """Verify all 6 exports are available from top-level package."""
    from openvibe_sdk import (
        Operator,
        llm_node,
        agent_node,
        Role,
        OperatorRuntime,
        RoleRuntime,
    )
    assert Operator is not None
    assert llm_node is not None
    assert agent_node is not None
    assert Role is not None
    assert OperatorRuntime is not None
    assert RoleRuntime is not None
```

**Step 7: Run all tests**

```bash
pytest tests/ -v
```

Expected: all PASS. Target: ~60+ tests across all files.

**Step 8: Commit**

```bash
git add v4/openvibe-sdk/src/openvibe_sdk/ v4/openvibe-sdk/tests/
git commit -m "feat(sdk): add RoleRuntime, public API, integration test — SDK V1 complete"
```

---

## Summary

| Task | Layer | What | Tests |
|------|-------|------|-------|
| 1 | - | Scaffold: dirs, pyproject.toml | 1 |
| 2 | 0 | LLM types + LLMProvider protocol | 7 |
| 3 | 0 | AnthropicProvider | 4 |
| 4 | 0 | Memory protocol + InMemoryStore | 10 |
| 5 | 1 | Tool schema converter | 6 |
| 6 | 1+2 | Operator + @llm_node | 11 |
| 7 | 1 | @agent_node | 11 |
| 8 | 2 | Config models + YAML loader + OperatorRuntime | 16 |
| 9 | 3 | Role + _RoleAwareLLM | 12 |
| 10 | 3 | RoleRuntime + public API + integration | ~10 |

**Total: ~88 tests, 10 tasks, 10 commits.**

### Package structure at completion

```
v4/openvibe-sdk/
├── pyproject.toml
├── src/openvibe_sdk/
│   ├── __init__.py           # 6 exports: Operator, llm_node, agent_node, Role, OperatorRuntime, RoleRuntime
│   ├── operator.py           # Operator + @llm_node + @agent_node
│   ├── role.py               # Role + _RoleAwareLLM
│   ├── runtime.py            # OperatorRuntime + RoleRuntime
│   ├── models.py             # OperatorConfig, WorkflowConfig, NodeConfig, TriggerConfig
│   ├── config.py             # YAML loader, prompt reader
│   ├── tools.py              # function_to_schema converter
│   ├── llm/
│   │   ├── __init__.py       # LLMResponse, ToolCall, LLMProvider protocol, MODEL_ALIASES
│   │   └── anthropic.py      # AnthropicProvider
│   └── memory/
│       ├── __init__.py       # MemoryProvider protocol, MemoryEntry
│       └── in_memory.py      # InMemoryStore
└── tests/
    ├── __init__.py
    ├── test_imports.py
    ├── test_llm_types.py
    ├── test_anthropic_provider.py
    ├── test_memory.py
    ├── test_tools.py
    ├── test_llm_node.py
    ├── test_agent_node.py
    ├── test_config_models.py
    ├── test_operator_runtime.py
    ├── test_role.py
    ├── test_role_runtime.py
    └── test_integration.py
```

### Public API

```python
from openvibe_sdk import (
    Operator,      # Base class — inherit for self.llm + self.config
    llm_node,      # Decorator — single LLM call, auto parse + state update
    agent_node,    # Decorator — LLM + tools loop until done
    Role,          # Identity — soul + operators + memory
    OperatorRuntime,  # Layer 2 runtime — YAML config, dispatch activations
    RoleRuntime,      # Layer 3 runtime — roles + infrastructure wiring
)
```

---

*Plan created: 2026-02-17*
