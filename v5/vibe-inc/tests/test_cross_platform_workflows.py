from openvibe_sdk.llm import LLMResponse


class FakeLLM:
    def call(self, *, system, messages, **kwargs):
        return LLMResponse(content="done")


def test_unified_cac_report_graph_compiles_and_invokes():
    from vibe_inc.roles.d2c_growth.cross_platform_workflows import create_unified_cac_report_graph
    from vibe_inc.roles.d2c_growth.cross_platform_ops import CrossPlatformOps

    op = CrossPlatformOps(llm=FakeLLM())
    graph = create_unified_cac_report_graph(op)
    assert graph is not None
    result = graph.invoke({"period": "last_7d"})
    assert "report" in result


def test_budget_rebalance_graph_compiles_and_invokes():
    from vibe_inc.roles.d2c_growth.cross_platform_workflows import create_budget_rebalance_graph
    from vibe_inc.roles.d2c_growth.cross_platform_ops import CrossPlatformOps

    op = CrossPlatformOps(llm=FakeLLM())
    graph = create_budget_rebalance_graph(op)
    assert graph is not None
    result = graph.invoke({"total_budget": 10000.0})
    assert "rebalance_result" in result


def test_platform_health_check_graph_compiles_and_invokes():
    from vibe_inc.roles.d2c_growth.cross_platform_workflows import create_platform_health_check_graph
    from vibe_inc.roles.d2c_growth.cross_platform_ops import CrossPlatformOps

    op = CrossPlatformOps(llm=FakeLLM())
    graph = create_platform_health_check_graph(op)
    assert graph is not None
    result = graph.invoke({})
    assert "health_result" in result
