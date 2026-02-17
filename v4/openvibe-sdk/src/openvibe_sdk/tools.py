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
