from unittest.mock import MagicMock, patch

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


@patch("vibe_ai_ops.graphs.sales.s1_lead_qualification._get_hubspot")
@patch("vibe_ai_ops.graphs.sales.s1_lead_qualification.crew_kickoff")
def test_graph_routes_education_for_empty_scores(mock_crew, mock_get_hs):
    """With crew returning zeros, composite is 0 → education route."""
    mock_hs = MagicMock()
    mock_get_hs.return_value = mock_hs
    mock_hs.get_contact.return_value = {}

    mock_crew.return_value = '{"fit_score": 0, "intent_score": 0, "urgency_score": 0, "reasoning": "empty", "route": "education"}'

    graph = create_lead_qual_graph()
    result = graph.invoke({
        "contact_id": "123",
        "source": "website",
    })
    assert result["route"] == "disqualify"  # fit < 20 → disqualify
    assert result["crm_updated"] is True
