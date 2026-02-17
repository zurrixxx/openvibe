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
