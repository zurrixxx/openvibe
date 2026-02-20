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


# --- campaign_create ---

def test_campaign_create_is_agent_node():
    from vibe_inc.roles.d2c_growth.email_ops import EmailOps
    assert hasattr(EmailOps.campaign_create, "_is_agent_node")
    assert EmailOps.campaign_create._is_agent_node is True
    assert "klaviyo_campaigns" in EmailOps.campaign_create._node_config["tools"]


def test_campaign_create_output_key():
    from vibe_inc.roles.d2c_growth.email_ops import EmailOps

    llm = FakeAgentLLM([_text_response("Campaign created: VIP Flash Sale")])
    op = EmailOps(llm=llm)
    result = op.campaign_create({"brief": {"product": "bot", "segment": "VIP"}})

    assert "campaign_result" in result
    assert result["campaign_result"] == "Campaign created: VIP Flash Sale"


# --- flow_optimize ---

def test_flow_optimize_is_agent_node():
    from vibe_inc.roles.d2c_growth.email_ops import EmailOps
    assert hasattr(EmailOps.flow_optimize, "_is_agent_node")
    assert EmailOps.flow_optimize._is_agent_node is True
    assert "klaviyo_flows" in EmailOps.flow_optimize._node_config["tools"]


def test_flow_optimize_output_key():
    from vibe_inc.roles.d2c_growth.email_ops import EmailOps

    llm = FakeAgentLLM([_text_response("Welcome flow optimized")])
    op = EmailOps(llm=llm)
    result = op.flow_optimize({"flow_id": "welcome"})

    assert "flow_result" in result


# --- segment_refresh ---

def test_segment_refresh_output_key():
    from vibe_inc.roles.d2c_growth.email_ops import EmailOps

    llm = FakeAgentLLM([_text_response("3 segments refreshed")])
    op = EmailOps(llm=llm)
    result = op.segment_refresh({})

    assert "segment_result" in result


# --- lifecycle_report ---

def test_lifecycle_report_output_key():
    from vibe_inc.roles.d2c_growth.email_ops import EmailOps

    llm = FakeAgentLLM([_text_response("Open rate: 28%, RPE: $0.45")])
    op = EmailOps(llm=llm)
    result = op.lifecycle_report({"period": "last_7d"})

    assert "report" in result


# --- list_hygiene ---

def test_list_hygiene_output_key():
    from vibe_inc.roles.d2c_growth.email_ops import EmailOps

    llm = FakeAgentLLM([_text_response("1,200 profiles suppressed")])
    op = EmailOps(llm=llm)
    result = op.list_hygiene({})

    assert "hygiene_result" in result
