from openvibe_sdk.llm import LLMResponse, ToolCall


def _text_response(content="done"):
    return LLMResponse(content=content, stop_reason="end_turn")


def _tool_response(tool_name, tool_input=None):
    return LLMResponse(
        content="I'll use a tool.",
        tool_calls=[ToolCall(id="tc_1", name=tool_name, input=tool_input or {})],
        stop_reason="tool_use",
    )


class FakeAgentLLM:
    """Fake LLM that returns pre-configured responses in sequence."""
    def __init__(self, responses):
        self.responses = list(responses)
        self.calls = []

    def call(self, *, system, messages, **kwargs):
        self.calls.append({"system": system, "messages": messages, **kwargs})
        return self.responses.pop(0)


# --- Task 7: campaign_create ---

def test_campaign_create_is_agent_node():
    """campaign_create must be an agent_node with tools."""
    from vibe_inc.roles.d2c_growth.ad_ops import AdOps
    assert hasattr(AdOps.campaign_create, "_is_agent_node")
    assert AdOps.campaign_create._is_agent_node is True
    assert "meta_ads_create" in AdOps.campaign_create._node_config["tools"]


def test_campaign_create_uses_brief():
    """campaign_create sends the brief to the LLM."""
    from vibe_inc.roles.d2c_growth.ad_ops import AdOps

    llm = FakeAgentLLM([_text_response("Campaign created: Bot Foundation")])
    op = AdOps(llm=llm)
    result = op.campaign_create({"brief": {"product": "bot", "narrative": "foundation"}})

    assert result["campaign_result"] == "Campaign created: Bot Foundation"
    assert len(llm.calls) == 1
    assert "brief" in llm.calls[0]["messages"][-1]["content"]


def test_campaign_create_docstring_is_system_prompt():
    """The docstring becomes the LLM system prompt."""
    from vibe_inc.roles.d2c_growth.ad_ops import AdOps

    llm = FakeAgentLLM([_text_response()])
    op = AdOps(llm=llm)
    op.campaign_create({"brief": {}})

    assert "performance marketing" in llm.calls[0]["system"].lower()


# --- Task 8: daily_optimize ---

def test_daily_optimize_is_agent_node():
    from vibe_inc.roles.d2c_growth.ad_ops import AdOps
    assert hasattr(AdOps.daily_optimize, "_is_agent_node")
    assert "meta_ads_read" in AdOps.daily_optimize._node_config["tools"]


def test_daily_optimize_reads_performance():
    from vibe_inc.roles.d2c_growth.ad_ops import AdOps

    llm = FakeAgentLLM([_text_response("Optimized: paused 2 underperformers")])
    op = AdOps(llm=llm)
    result = op.daily_optimize({"date": "2026-02-19"})

    assert "optimization_result" in result
    assert len(llm.calls) == 1


def test_daily_optimize_system_prompt_mentions_thresholds():
    from vibe_inc.roles.d2c_growth.ad_ops import AdOps

    llm = FakeAgentLLM([_text_response()])
    op = AdOps(llm=llm)
    op.daily_optimize({"date": "2026-02-19"})

    system = llm.calls[0]["system"]
    assert "20%" in system or "threshold" in system.lower()


# --- Task 9: weekly_report ---

def test_weekly_report_is_agent_node():
    from vibe_inc.roles.d2c_growth.ad_ops import AdOps
    assert hasattr(AdOps.weekly_report, "_is_agent_node")


def test_weekly_report_output_key():
    from vibe_inc.roles.d2c_growth.ad_ops import AdOps

    llm = FakeAgentLLM([_text_response("Weekly: Bot CAC $380, Dot CAC $270")])
    op = AdOps(llm=llm)
    result = op.weekly_report({"week": "2026-W08"})

    assert "report" in result
