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
