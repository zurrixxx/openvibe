from openvibe_sdk.llm import LLMResponse, ToolCall


def _text_response(content="done"):
    return LLMResponse(content=content, stop_reason="end_turn")


class FakeAgentLLM:
    def __init__(self, responses):
        self.responses = list(responses)
        self.calls = []

    def call(self, *, system, messages, **kwargs):
        self.calls.append({"system": system, "messages": messages, **kwargs})
        return self.responses.pop(0)


# --- Task 10: experiment_analyze ---

def test_experiment_analyze_is_agent_node():
    from vibe_inc.roles.d2c_growth.cro_ops import CROps
    assert hasattr(CROps.experiment_analyze, "_is_agent_node")
    assert "analytics_query_metrics" in CROps.experiment_analyze._node_config["tools"]


def test_experiment_analyze_returns_analysis():
    from vibe_inc.roles.d2c_growth.cro_ops import CROps

    llm = FakeAgentLLM([_text_response("Foundation variant leads: CVR 2.1% vs 1.3% control")])
    op = CROps(llm=llm)
    result = op.experiment_analyze({"product": "bot"})

    assert "analysis" in result


def test_experiment_analyze_mentions_significance():
    from vibe_inc.roles.d2c_growth.cro_ops import CROps

    llm = FakeAgentLLM([_text_response()])
    op = CROps(llm=llm)
    op.experiment_analyze({"product": "bot"})

    system = llm.calls[0]["system"]
    assert "significance" in system.lower() or "confidence" in system.lower()


# --- Task 11: funnel_diagnose ---

def test_funnel_diagnose_is_agent_node():
    from vibe_inc.roles.d2c_growth.cro_ops import CROps
    assert hasattr(CROps.funnel_diagnose, "_is_agent_node")


def test_funnel_diagnose_returns_diagnosis():
    from vibe_inc.roles.d2c_growth.cro_ops import CROps

    llm = FakeAgentLLM([_text_response("Biggest drop: checkout initiation (3.1% → 0.8%)")])
    op = CROps(llm=llm)
    result = op.funnel_diagnose({"product": "bot"})

    assert "diagnosis" in result


# --- Task 12: page_optimize ---

def test_page_optimize_is_agent_node():
    from vibe_inc.roles.d2c_growth.cro_ops import CROps
    assert hasattr(CROps.page_optimize, "_is_agent_node")
    tools = CROps.page_optimize._node_config["tools"]
    assert "shopify_page_read" in tools
    assert "shopify_page_update" in tools


def test_page_optimize_returns_result():
    from vibe_inc.roles.d2c_growth.cro_ops import CROps

    llm = FakeAgentLLM([_text_response("Updated headline: 'The room that remembers'")])
    op = CROps(llm=llm)
    result = op.page_optimize({
        "page_id": "123",
        "optimization": "headline",
        "rationale": "Foundation narrative winning in A/B test",
    })

    assert "optimization_result" in result


def test_page_optimize_mentions_approval():
    from vibe_inc.roles.d2c_growth.cro_ops import CROps

    llm = FakeAgentLLM([_text_response()])
    op = CROps(llm=llm)
    op.page_optimize({"page_id": "123", "optimization": "cta"})

    system = llm.calls[0]["system"]
    assert "approval" in system.lower() or "review" in system.lower()
