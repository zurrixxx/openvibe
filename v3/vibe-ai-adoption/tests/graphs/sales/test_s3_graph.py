from vibe_ai_ops.graphs.sales.s3_engagement import (
    create_engagement_graph,
    EngagementState,
)


def test_engagement_state_initial():
    state = EngagementState(contact_id="123", segment="enterprise-fintech")
    assert state["contact_id"] == "123"
    assert state.get("final_plan") is None


def test_engagement_graph_compiles():
    graph = create_engagement_graph()
    assert graph is not None


def test_engagement_graph_runs_all_nodes():
    graph = create_engagement_graph()
    result = graph.invoke({
        "contact_id": "123",
        "segment": "enterprise-fintech",
        "buyer_profile": {"company": "BigCorp", "title": "CTO"},
    })
    assert result["final_plan"]["contact_id"] == "123"
    assert result["final_plan"]["status"] == "ready"
