from openvibe_sdk.llm import LLMResponse


def _text_response(content="done"):
    return LLMResponse(content=content, stop_reason="end_turn")


class FakeAgentLLM:
    def __init__(self, responses):
        self.responses = list(responses)
        self.calls = []

    def call(self, *, system, messages, **kwargs):
        self.calls.append({"system": system, "messages": messages, **kwargs})
        return self.responses.pop(0)


# --- product_optimize ---

def test_product_optimize_is_agent_node():
    from vibe_inc.roles.d2c_growth.cro_ops import CROps
    assert hasattr(CROps.product_optimize, "_is_agent_node")
    tools = CROps.product_optimize._node_config["tools"]
    assert "shopify_products" in tools


def test_product_optimize_output_key():
    from vibe_inc.roles.d2c_growth.cro_ops import CROps

    llm = FakeAgentLLM([_text_response("Bot PDP has 2.1% CVR, Dot 0.8%")])
    op = CROps(llm=llm)
    result = op.product_optimize({"product_id": "123"})
    assert "product_result" in result


# --- discount_strategy ---

def test_discount_strategy_is_agent_node():
    from vibe_inc.roles.d2c_growth.cro_ops import CROps
    assert hasattr(CROps.discount_strategy, "_is_agent_node")
    tools = CROps.discount_strategy._node_config["tools"]
    assert "shopify_discounts" in tools


def test_discount_strategy_output_key():
    from vibe_inc.roles.d2c_growth.cro_ops import CROps

    llm = FakeAgentLLM([_text_response("LAUNCH10 has 12% redemption, positive ROI")])
    op = CROps(llm=llm)
    result = op.discount_strategy({})
    assert "discount_result" in result


def test_discount_strategy_mentions_margin():
    from vibe_inc.roles.d2c_growth.cro_ops import CROps

    llm = FakeAgentLLM([_text_response()])
    op = CROps(llm=llm)
    op.discount_strategy({})
    system = llm.calls[0]["system"]
    assert "margin" in system.lower() or "40%" in system


# --- conversion_report ---

def test_conversion_report_is_agent_node():
    from vibe_inc.roles.d2c_growth.cro_ops import CROps
    assert hasattr(CROps.conversion_report, "_is_agent_node")
    tools = CROps.conversion_report._node_config["tools"]
    assert "ab_test_read" in tools
    assert "analytics_query_metrics" in tools


def test_conversion_report_output_key():
    from vibe_inc.roles.d2c_growth.cro_ops import CROps

    llm = FakeAgentLLM([_text_response("Overall CVR: 1.2%, Bot: 1.5%, Dot: 0.9%")])
    op = CROps(llm=llm)
    result = op.conversion_report({"period": "last_7_days"})
    assert "conversion_report" in result


def test_conversion_report_mentions_progressive_disclosure():
    from vibe_inc.roles.d2c_growth.cro_ops import CROps

    llm = FakeAgentLLM([_text_response()])
    op = CROps(llm=llm)
    op.conversion_report({})
    system = llm.calls[0]["system"]
    assert "progressive" in system.lower() or "headline" in system.lower()
