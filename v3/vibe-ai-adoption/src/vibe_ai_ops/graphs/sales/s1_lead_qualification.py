from __future__ import annotations

from typing import Any, TypedDict

from langgraph.graph import StateGraph, END


class LeadQualState(TypedDict, total=False):
    contact_id: str
    source: str
    enriched_data: dict[str, Any]
    score: dict[str, Any] | None
    route: str | None
    crm_updated: bool


def _enrich_lead(state: LeadQualState) -> LeadQualState:
    """Node 1: Enrich lead from HubSpot + web research."""
    # Will be wired to HubSpotClient in Task 13
    return state


def _score_lead(state: LeadQualState) -> LeadQualState:
    """Node 2: Score lead using CrewAI Lead Qual crew."""
    # Will be wired to CrewAI crew in Task 13
    return state


def _route_lead(state: LeadQualState) -> LeadQualState:
    """Node 3: Route based on composite score."""
    score = state.get("score", {})
    composite = (
        0.4 * score.get("fit_score", 0)
        + 0.35 * score.get("intent_score", 0)
        + 0.25 * score.get("urgency_score", 0)
    )
    if composite >= 80:
        state["route"] = "sales"
    elif composite >= 50:
        state["route"] = "nurture"
    else:
        state["route"] = "education"
    return state


def _update_crm(state: LeadQualState) -> LeadQualState:
    """Node 4: Update HubSpot with scores and route."""
    # Will be wired to HubSpotClient in Task 13
    state["crm_updated"] = True
    return state


def create_lead_qual_graph(checkpointer=None):
    """Create the Lead Qualification LangGraph workflow."""
    workflow = StateGraph(LeadQualState)

    workflow.add_node("enrich", _enrich_lead)
    workflow.add_node("score", _score_lead)
    workflow.add_node("route", _route_lead)
    workflow.add_node("update_crm", _update_crm)

    workflow.set_entry_point("enrich")
    workflow.add_edge("enrich", "score")
    workflow.add_edge("score", "route")
    workflow.add_edge("route", "update_crm")
    workflow.add_edge("update_crm", END)

    return workflow.compile(checkpointer=checkpointer)
