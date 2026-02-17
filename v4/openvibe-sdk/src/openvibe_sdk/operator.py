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
