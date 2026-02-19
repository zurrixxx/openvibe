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
    from vibe_inc.roles.d2c_growth.linkedin_ad_ops import LinkedInAdOps
    assert hasattr(LinkedInAdOps.campaign_create, "_is_agent_node")
    assert LinkedInAdOps.campaign_create._is_agent_node is True
    assert "linkedin_ads_create" in LinkedInAdOps.campaign_create._node_config["tools"]


def test_campaign_create_output_key():
    from vibe_inc.roles.d2c_growth.linkedin_ad_ops import LinkedInAdOps

    llm = FakeAgentLLM([_text_response("Campaign created: Vibe Bot B2B")])
    op = LinkedInAdOps(llm=llm)
    result = op.campaign_create({"brief": {"product": "bot", "audience": "CTOs"}})

    assert "campaign_result" in result


# --- daily_optimize ---

def test_daily_optimize_is_agent_node():
    from vibe_inc.roles.d2c_growth.linkedin_ad_ops import LinkedInAdOps
    assert hasattr(LinkedInAdOps.daily_optimize, "_is_agent_node")
    assert "linkedin_ads_analytics" in LinkedInAdOps.daily_optimize._node_config["tools"]


def test_daily_optimize_min_data_days():
    """daily_optimize system prompt must enforce 14-day minimum data window."""
    from vibe_inc.roles.d2c_growth.linkedin_ad_ops import LinkedInAdOps

    llm = FakeAgentLLM([_text_response("No changes — insufficient data")])
    op = LinkedInAdOps(llm=llm)
    op.daily_optimize({"date": "2026-02-20"})

    system_prompt = llm.calls[0]["system"]
    assert "14 days" in system_prompt


# --- audience_management ---

def test_audience_management_is_agent_node():
    from vibe_inc.roles.d2c_growth.linkedin_ad_ops import LinkedInAdOps
    assert hasattr(LinkedInAdOps.audience_management, "_is_agent_node")
    assert LinkedInAdOps.audience_management._is_agent_node is True
    assert "linkedin_ads_audiences" in LinkedInAdOps.audience_management._node_config["tools"]


# --- weekly_report ---

def test_weekly_report_output_key():
    from vibe_inc.roles.d2c_growth.linkedin_ad_ops import LinkedInAdOps

    llm = FakeAgentLLM([_text_response("Weekly: CPL $135, 42 leads")])
    op = LinkedInAdOps(llm=llm)
    result = op.weekly_report({"week": "2026-W08"})

    assert "report" in result


# --- lead_quality_review ---

def test_lead_quality_review_output_key():
    from vibe_inc.roles.d2c_growth.linkedin_ad_ops import LinkedInAdOps

    llm = FakeAgentLLM([_text_response("MQL rate: 28%, CPL: $142")])
    op = LinkedInAdOps(llm=llm)
    result = op.lead_quality_review({"period": "last_7d"})

    assert "lead_quality_result" in result
