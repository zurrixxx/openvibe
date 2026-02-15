"""End-to-end test for S1 Lead Qualification through all 3 layers."""
import json
from unittest.mock import MagicMock, patch

from vibe_ai_ops.graphs.sales.s1_lead_qualification import create_lead_qual_graph
from vibe_ai_ops.graphs.checkpointer import create_checkpointer


@patch("vibe_ai_ops.graphs.sales.s1_lead_qualification._get_hubspot")
@patch("vibe_ai_ops.graphs.sales.s1_lead_qualification.crew_kickoff")
def test_s1_full_pipeline_sales_route(mock_crew, mock_get_hs):
    """S1: HubSpot enrich → CrewAI score → route=sales → CRM update."""
    mock_hs = MagicMock()
    mock_get_hs.return_value = mock_hs
    mock_hs.get_contact.return_value = {
        "email": "jane@bigcorp.com",
        "firstname": "Jane",
        "lastname": "Smith",
        "company": "BigCorp",
        "jobtitle": "CTO",
    }

    mock_crew.return_value = json.dumps({
        "fit_score": 90, "intent_score": 80, "urgency_score": 70,
        "reasoning": "CTO at large corp, requested demo", "route": "sales",
    })

    graph = create_lead_qual_graph(checkpointer=create_checkpointer())
    result = graph.invoke(
        {"contact_id": "123", "source": "website"},
        config={"configurable": {"thread_id": "test-s1-123"}},
    )

    assert result["route"] == "sales"
    assert result["crm_updated"] is True
    mock_hs.get_contact.assert_called_once_with("123")
    mock_hs.update_contact.assert_called_once()


@patch("vibe_ai_ops.graphs.sales.s1_lead_qualification._get_hubspot")
@patch("vibe_ai_ops.graphs.sales.s1_lead_qualification.crew_kickoff")
def test_s1_nurture_route(mock_crew, mock_get_hs):
    """Mid-score leads route to nurture."""
    mock_hs = MagicMock()
    mock_get_hs.return_value = mock_hs
    mock_hs.get_contact.return_value = {"company": "SmallCo", "jobtitle": "Manager"}

    mock_crew.return_value = json.dumps({
        "fit_score": 60, "intent_score": 55, "urgency_score": 50,
        "reasoning": "Moderate fit", "route": "nurture",
    })

    graph = create_lead_qual_graph()
    result = graph.invoke({"contact_id": "456", "source": "webinar"})

    assert result["route"] == "nurture"


@patch("vibe_ai_ops.graphs.sales.s1_lead_qualification._get_hubspot")
@patch("vibe_ai_ops.graphs.sales.s1_lead_qualification.crew_kickoff")
def test_s1_disqualify_low_fit(mock_crew, mock_get_hs):
    """Fit < 20 → disqualify regardless of other scores."""
    mock_hs = MagicMock()
    mock_get_hs.return_value = mock_hs
    mock_hs.get_contact.return_value = {"company": "Consumer", "jobtitle": "Student"}

    mock_crew.return_value = json.dumps({
        "fit_score": 10, "intent_score": 90, "urgency_score": 90,
        "reasoning": "No ICP match", "route": "disqualify",
    })

    graph = create_lead_qual_graph()
    result = graph.invoke({"contact_id": "789", "source": "cold"})

    assert result["route"] == "disqualify"
