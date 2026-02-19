from openvibe_sdk.llm import LLMResponse, ToolCall


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


# --- campaign_create ---

def test_campaign_create_is_agent_node():
    from vibe_inc.roles.d2c_growth.google_ad_ops import GoogleAdOps
    assert hasattr(GoogleAdOps.campaign_create, "_is_agent_node")
    assert GoogleAdOps.campaign_create._is_agent_node is True
    assert "google_ads_query" in GoogleAdOps.campaign_create._node_config["tools"]


def test_campaign_create_uses_brief():
    from vibe_inc.roles.d2c_growth.google_ad_ops import GoogleAdOps

    llm = FakeAgentLLM([_text_response("Campaign created")])
    op = GoogleAdOps(llm=llm)
    result = op.campaign_create({"brief": {"product": "bot", "type": "search"}})

    assert result["campaign_result"] == "Campaign created"
    assert len(llm.calls) == 1


# --- daily_optimize ---

def test_daily_optimize_is_agent_node():
    from vibe_inc.roles.d2c_growth.google_ad_ops import GoogleAdOps
    assert hasattr(GoogleAdOps.daily_optimize, "_is_agent_node")
    assert "google_ads_query" in GoogleAdOps.daily_optimize._node_config["tools"]


def test_daily_optimize_output_key():
    from vibe_inc.roles.d2c_growth.google_ad_ops import GoogleAdOps

    llm = FakeAgentLLM([_text_response("Optimized: paused 3 keywords")])
    op = GoogleAdOps(llm=llm)
    result = op.daily_optimize({"date": "2026-02-20"})

    assert "optimization_result" in result


# --- search_term_mining ---

def test_search_term_mining_is_agent_node():
    from vibe_inc.roles.d2c_growth.google_ad_ops import GoogleAdOps
    assert hasattr(GoogleAdOps.search_term_mining, "_is_agent_node")
    assert GoogleAdOps.search_term_mining._is_agent_node is True


def test_search_term_mining_output_key():
    from vibe_inc.roles.d2c_growth.google_ad_ops import GoogleAdOps

    llm = FakeAgentLLM([_text_response("Found 12 new keyword candidates")])
    op = GoogleAdOps(llm=llm)
    result = op.search_term_mining({"campaign_id": "123"})

    assert "search_terms" in result


# --- weekly_report ---

def test_weekly_report_is_agent_node():
    from vibe_inc.roles.d2c_growth.google_ad_ops import GoogleAdOps
    assert hasattr(GoogleAdOps.weekly_report, "_is_agent_node")
    assert "google_ads_conversions" in GoogleAdOps.weekly_report._node_config["tools"]


def test_weekly_report_output_key():
    from vibe_inc.roles.d2c_growth.google_ad_ops import GoogleAdOps

    llm = FakeAgentLLM([_text_response("Weekly: Bot CPA $280")])
    op = GoogleAdOps(llm=llm)
    result = op.weekly_report({"week": "2026-W08"})

    assert "report" in result


# --- recommendations_review ---

def test_recommendations_review_is_agent_node():
    from vibe_inc.roles.d2c_growth.google_ad_ops import GoogleAdOps
    assert hasattr(GoogleAdOps.recommendations_review, "_is_agent_node")
    assert "google_ads_recommendations" in GoogleAdOps.recommendations_review._node_config["tools"]


def test_recommendations_review_output_key():
    from vibe_inc.roles.d2c_growth.google_ad_ops import GoogleAdOps

    llm = FakeAgentLLM([_text_response("Applied 3 bid recommendations")])
    op = GoogleAdOps(llm=llm)
    result = op.recommendations_review({})

    assert "recommendations_result" in result
