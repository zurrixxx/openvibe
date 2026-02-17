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
