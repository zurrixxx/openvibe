from openvibe_sdk.llm import LLMResponse


class FakeLLM:
    def call(self, *, system, messages, **kwargs):
        return LLMResponse(content="done")


# --- MetaAdOps workflows ---


def test_meta_daily_optimize_graph_compiles():
    from vibe_inc.roles.d2c_growth.workflows import create_meta_daily_optimize_graph
    from vibe_inc.roles.d2c_growth.meta_ad_ops import MetaAdOps

    op = MetaAdOps(llm=FakeLLM())
    graph = create_meta_daily_optimize_graph(op)
    assert graph is not None


def test_meta_daily_optimize_graph_invokes():
    from vibe_inc.roles.d2c_growth.workflows import create_meta_daily_optimize_graph
    from vibe_inc.roles.d2c_growth.meta_ad_ops import MetaAdOps

    op = MetaAdOps(llm=FakeLLM())
    graph = create_meta_daily_optimize_graph(op)
    result = graph.invoke({"date": "2026-02-19"})
    assert "optimization_result" in result


def test_meta_campaign_create_graph_compiles():
    from vibe_inc.roles.d2c_growth.workflows import create_meta_campaign_create_graph
    from vibe_inc.roles.d2c_growth.meta_ad_ops import MetaAdOps

    op = MetaAdOps(llm=FakeLLM())
    graph = create_meta_campaign_create_graph(op)
    assert graph is not None


def test_meta_audience_refresh_graph_compiles():
    from vibe_inc.roles.d2c_growth.workflows import create_meta_audience_refresh_graph
    from vibe_inc.roles.d2c_growth.meta_ad_ops import MetaAdOps

    op = MetaAdOps(llm=FakeLLM())
    graph = create_meta_audience_refresh_graph(op)
    assert graph is not None


def test_meta_audience_refresh_graph_invokes():
    from vibe_inc.roles.d2c_growth.workflows import create_meta_audience_refresh_graph
    from vibe_inc.roles.d2c_growth.meta_ad_ops import MetaAdOps

    op = MetaAdOps(llm=FakeLLM())
    graph = create_meta_audience_refresh_graph(op)
    result = graph.invoke({"action": "review"})
    assert "audience_result" in result


# --- GoogleAdOps workflows ---


def test_google_daily_optimize_graph_compiles():
    from vibe_inc.roles.d2c_growth.workflows import create_google_daily_optimize_graph
    from vibe_inc.roles.d2c_growth.google_ad_ops import GoogleAdOps

    op = GoogleAdOps(llm=FakeLLM())
    graph = create_google_daily_optimize_graph(op)
    assert graph is not None


def test_google_campaign_create_graph_compiles():
    from vibe_inc.roles.d2c_growth.workflows import create_google_campaign_create_graph
    from vibe_inc.roles.d2c_growth.google_ad_ops import GoogleAdOps

    op = GoogleAdOps(llm=FakeLLM())
    graph = create_google_campaign_create_graph(op)
    assert graph is not None


def test_google_search_term_mining_graph_invokes():
    from vibe_inc.roles.d2c_growth.workflows import create_google_search_term_mining_graph
    from vibe_inc.roles.d2c_growth.google_ad_ops import GoogleAdOps

    op = GoogleAdOps(llm=FakeLLM())
    graph = create_google_search_term_mining_graph(op)
    result = graph.invoke({"campaign_id": "123"})
    assert "search_terms" in result


def test_google_recommendations_review_graph_compiles():
    from vibe_inc.roles.d2c_growth.workflows import create_google_recommendations_review_graph
    from vibe_inc.roles.d2c_growth.google_ad_ops import GoogleAdOps

    op = GoogleAdOps(llm=FakeLLM())
    graph = create_google_recommendations_review_graph(op)
    assert graph is not None


# --- CROps workflows ---


def test_experiment_analyze_graph_compiles():
    from vibe_inc.roles.d2c_growth.workflows import create_experiment_analyze_graph
    from vibe_inc.roles.d2c_growth.cro_ops import CROps

    op = CROps(llm=FakeLLM())
    graph = create_experiment_analyze_graph(op)
    assert graph is not None
