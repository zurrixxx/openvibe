from openvibe_sdk.llm import LLMResponse


class FakeLLM:
    def call(self, *, system, messages, **kwargs):
        return LLMResponse(content="done")


def test_email_campaign_create_graph_compiles():
    from vibe_inc.roles.d2c_growth.email_workflows import create_email_campaign_create_graph
    from vibe_inc.roles.d2c_growth.email_ops import EmailOps

    op = EmailOps(llm=FakeLLM())
    graph = create_email_campaign_create_graph(op)
    assert graph is not None


def test_email_flow_optimize_graph_compiles():
    from vibe_inc.roles.d2c_growth.email_workflows import create_email_flow_optimize_graph
    from vibe_inc.roles.d2c_growth.email_ops import EmailOps

    op = EmailOps(llm=FakeLLM())
    graph = create_email_flow_optimize_graph(op)
    assert graph is not None


def test_email_segment_refresh_graph_compiles():
    from vibe_inc.roles.d2c_growth.email_workflows import create_email_segment_refresh_graph
    from vibe_inc.roles.d2c_growth.email_ops import EmailOps

    op = EmailOps(llm=FakeLLM())
    graph = create_email_segment_refresh_graph(op)
    assert graph is not None


def test_email_lifecycle_report_graph_compiles():
    from vibe_inc.roles.d2c_growth.email_workflows import create_email_lifecycle_report_graph
    from vibe_inc.roles.d2c_growth.email_ops import EmailOps

    op = EmailOps(llm=FakeLLM())
    graph = create_email_lifecycle_report_graph(op)
    assert graph is not None
