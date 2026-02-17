"""Tests for @agent_node — Pi-style tool loop decorator."""

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


def search(query: str) -> str:
    """Search for information."""
    return f"Results for: {query}"


def calculator(expression: str) -> str:
    """Evaluate a math expression."""
    return str(eval(expression))


class ResearchOp(Operator):
    operator_id = "research"

    @agent_node(tools=[search], output_key="findings")
    def investigate(self, state):
        """You are a research analyst."""
        return f"Investigate: {state['topic']}"


def test_agent_node_no_tools_returns_immediately():
    llm = FakeAgentLLM([_text_response("final answer")])
    op = ResearchOp(llm=llm)
    state = {"topic": "AI"}
    result = op.investigate(state)
    assert result["findings"] == "final answer"
    assert len(llm.calls) == 1


def test_agent_node_tool_loop():
    llm = FakeAgentLLM([
        _tool_response("search", {"query": "AI trends"}),
        _text_response("AI is growing fast"),
    ])
    op = ResearchOp(llm=llm)
    state = {"topic": "AI"}
    result = op.investigate(state)
    assert result["findings"] == "AI is growing fast"
    assert len(llm.calls) == 2
    second_messages = llm.calls[1]["messages"]
    assert len(second_messages) == 3


def test_agent_node_multi_step_loop():
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
    calls = []

    def tracking_search(query: str) -> str:
        calls.append(query)
        return f"Results for: {query}"

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
    class LimitedOp(Operator):
        @agent_node(tools=[search], output_key="out", max_steps=2)
        def investigate(self, state):
            """You research things."""
            return "go"

    llm = FakeAgentLLM([
        _tool_response("search", {"query": "1"}),
        _tool_response("search", {"query": "2"}),
        _tool_response("search", {"query": "3"}),
    ])
    op = LimitedOp(llm=llm)
    result = op.investigate({"x": 1})
    assert len(llm.calls) == 2


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
    llm = FakeAgentLLM([
        _tool_response("nonexistent_tool", {"x": 1}),
        _text_response("ok"),
    ])
    op = ResearchOp(llm=llm)
    result = op.investigate({"topic": "x"})
    assert result["findings"] == "ok"
