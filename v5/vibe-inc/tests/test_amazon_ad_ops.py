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


# --- campaign_create ---

def test_campaign_create_is_agent_node():
    from vibe_inc.roles.d2c_growth.amazon_ad_ops import AmazonAdOps
    assert hasattr(AmazonAdOps.campaign_create, "_is_agent_node")
    assert AmazonAdOps.campaign_create._is_agent_node is True
    assert "amazon_ads_campaigns" in AmazonAdOps.campaign_create._node_config["tools"]


def test_campaign_create_output_key():
    from vibe_inc.roles.d2c_growth.amazon_ad_ops import AmazonAdOps

    llm = FakeAgentLLM([_text_response("Campaign created")])
    op = AmazonAdOps(llm=llm)
    result = op.campaign_create({"brief": {"product": "bot", "asin": "B0EXAMPLE"}})

    assert "campaign_result" in result


# --- daily_optimize ---

def test_daily_optimize_is_agent_node():
    from vibe_inc.roles.d2c_growth.amazon_ad_ops import AmazonAdOps
    assert hasattr(AmazonAdOps.daily_optimize, "_is_agent_node")
    assert "amazon_ads_report" in AmazonAdOps.daily_optimize._node_config["tools"]


def test_daily_optimize_mentions_acos():
    from vibe_inc.roles.d2c_growth.amazon_ad_ops import AmazonAdOps

    llm = FakeAgentLLM([_text_response()])
    op = AmazonAdOps(llm=llm)
    op.daily_optimize({"date": "2026-02-20"})

    assert "acos" in llm.calls[0]["system"].lower()


# --- search_term_harvesting ---

def test_search_term_harvesting_is_agent_node():
    from vibe_inc.roles.d2c_growth.amazon_ad_ops import AmazonAdOps
    assert hasattr(AmazonAdOps.search_term_harvesting, "_is_agent_node")
    assert "amazon_ads_search_terms" in AmazonAdOps.search_term_harvesting._node_config["tools"]


def test_search_term_harvesting_output_key():
    from vibe_inc.roles.d2c_growth.amazon_ad_ops import AmazonAdOps

    llm = FakeAgentLLM([_text_response("Harvested 8 keywords")])
    op = AmazonAdOps(llm=llm)
    result = op.search_term_harvesting({"campaign_id": "123"})

    assert "search_terms_result" in result


# --- weekly_report ---

def test_weekly_report_is_agent_node():
    from vibe_inc.roles.d2c_growth.amazon_ad_ops import AmazonAdOps
    assert hasattr(AmazonAdOps.weekly_report, "_is_agent_node")


def test_weekly_report_output_key():
    from vibe_inc.roles.d2c_growth.amazon_ad_ops import AmazonAdOps

    llm = FakeAgentLLM([_text_response("Weekly: Bot ACOS 18%")])
    op = AmazonAdOps(llm=llm)
    result = op.weekly_report({"week": "2026-W08"})

    assert "report" in result


# --- competitive_analysis ---

def test_competitive_analysis_is_agent_node():
    from vibe_inc.roles.d2c_growth.amazon_ad_ops import AmazonAdOps
    assert hasattr(AmazonAdOps.competitive_analysis, "_is_agent_node")
    assert AmazonAdOps.competitive_analysis._is_agent_node is True


def test_competitive_analysis_output_key():
    from vibe_inc.roles.d2c_growth.amazon_ad_ops import AmazonAdOps

    llm = FakeAgentLLM([_text_response("Market share analysis complete")])
    op = AmazonAdOps(llm=llm)
    result = op.competitive_analysis({})

    assert "competitive_result" in result
