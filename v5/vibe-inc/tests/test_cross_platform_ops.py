from openvibe_sdk.llm import LLMResponse


def _text_response(content="done"):
    return LLMResponse(content=content, stop_reason="end_turn")


class FakeAgentLLM:
    """Fake LLM that returns pre-configured responses in sequence."""
    def __init__(self, responses):
        self.responses = list(responses)
        self.calls = []

    def call(self, *, system, messages, **kwargs):
        self.calls.append({"system": system, "messages": messages, **kwargs})
        return self.responses.pop(0)


# --- unified_cac_report ---

def test_unified_cac_report_is_agent_node():
    from vibe_inc.roles.d2c_growth.cross_platform_ops import CrossPlatformOps
    assert hasattr(CrossPlatformOps.unified_cac_report, "_is_agent_node")
    assert CrossPlatformOps.unified_cac_report._is_agent_node is True
    assert "unified_metrics_read" in CrossPlatformOps.unified_cac_report._node_config["tools"]


def test_unified_cac_report_output_key():
    from vibe_inc.roles.d2c_growth.cross_platform_ops import CrossPlatformOps

    llm = FakeAgentLLM([_text_response("Blended CAC: $345, trending down 8%")])
    op = CrossPlatformOps(llm=llm)
    result = op.unified_cac_report({"period": "last_7d"})

    assert "report" in result
    assert result["report"] == "Blended CAC: $345, trending down 8%"


# --- budget_rebalance ---

def test_budget_rebalance_is_agent_node():
    from vibe_inc.roles.d2c_growth.cross_platform_ops import CrossPlatformOps
    assert hasattr(CrossPlatformOps.budget_rebalance, "_is_agent_node")
    assert CrossPlatformOps.budget_rebalance._is_agent_node is True
    assert "budget_allocator" in CrossPlatformOps.budget_rebalance._node_config["tools"]


def test_budget_rebalance_mentions_approval():
    from vibe_inc.roles.d2c_growth.cross_platform_ops import CrossPlatformOps

    llm = FakeAgentLLM([_text_response("Rebalance proposed")])
    op = CrossPlatformOps(llm=llm)
    op.budget_rebalance({"total_budget": 5000})

    system_prompt = llm.calls[0]["system"].lower()
    assert "approval" in system_prompt or "human" in system_prompt


# --- platform_health_check ---

def test_platform_health_check_output_key():
    from vibe_inc.roles.d2c_growth.cross_platform_ops import CrossPlatformOps

    llm = FakeAgentLLM([_text_response("All platforms healthy, overall score: 82")])
    op = CrossPlatformOps(llm=llm)
    result = op.platform_health_check({})

    assert "health_result" in result
