from vibe_ai_ops.graphs.sales.s1_lead_qualification import (
    create_lead_qual_graph,
    LeadQualState,
)


def test_lead_qual_state_initial():
    state = LeadQualState(
        contact_id="123",
        source="website",
    )
    assert state["contact_id"] == "123"
    assert state.get("enriched_data") is None
    assert state.get("score") is None
    assert state.get("route") is None


def test_graph_compiles():
    graph = create_lead_qual_graph()
    assert graph is not None


def test_graph_routes_education_for_empty_scores():
    """With no scores set, composite is 0 → education route."""
    graph = create_lead_qual_graph()
    result = graph.invoke({
        "contact_id": "123",
        "source": "website",
    })
    assert result["route"] == "education"
    assert result["crm_updated"] is True
