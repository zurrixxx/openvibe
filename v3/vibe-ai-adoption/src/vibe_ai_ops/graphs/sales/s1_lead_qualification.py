from __future__ import annotations

import json
import os
from typing import Any, TypedDict

from langgraph.graph import StateGraph, END

from vibe_ai_ops.shared.hubspot_client import HubSpotClient
from vibe_ai_ops.shared.models import AgentConfig
from vibe_ai_ops.shared.config import load_prompt
from vibe_ai_ops.crews.sales.s1_lead_qualification import create_lead_qual_crew


# Module-level client — initialized lazily, mockable in tests
hubspot_client: HubSpotClient | None = None


def _get_hubspot() -> HubSpotClient:
    global hubspot_client
    if hubspot_client is None:
        hubspot_client = HubSpotClient(api_key=os.environ.get("HUBSPOT_API_KEY"))
    return hubspot_client


def crew_kickoff(config: AgentConfig, prompt: str, lead_data: dict) -> str:
    """Run the S1 CrewAI crew and return raw output."""
    crew = create_lead_qual_crew(config, system_prompt=prompt)
    result = crew.kickoff(inputs={"lead_data": json.dumps(lead_data)})
    return str(result)


class LeadQualState(TypedDict, total=False):
    contact_id: str
    source: str
    enriched_data: dict[str, Any]
    score: dict[str, Any] | None
    route: str | None
    crm_updated: bool


def _enrich_lead(state: LeadQualState) -> LeadQualState:
    """Node 1: Enrich lead from HubSpot."""
    hs = _get_hubspot()
    contact_id = state.get("contact_id", "")
    if contact_id:
        state["enriched_data"] = hs.get_contact(contact_id)
    return state


def _score_lead(state: LeadQualState) -> LeadQualState:
    """Node 2: Score lead using CrewAI Lead Qual crew."""
    config = AgentConfig(
        id="s1", name="Lead Qualification", engine="sales",
        tier="deep_dive", architecture="temporal_langgraph_crewai",
        trigger={"type": "webhook", "event_source": "hubspot:new_lead"},
        output_channel="slack:#sales-agents",
        prompt_file="sales/s1_lead_qualification.md",
        temperature=0.3,
    )

    try:
        prompt = load_prompt("sales/s1_lead_qualification.md")
    except FileNotFoundError:
        prompt = "You are a lead qualification specialist."

    lead_data = state.get("enriched_data", {})
    raw = crew_kickoff(config, prompt, lead_data)

    try:
        score = json.loads(raw)
        state["score"] = score
    except (json.JSONDecodeError, TypeError):
        state["score"] = {
            "fit_score": 0, "intent_score": 0, "urgency_score": 0,
            "reasoning": f"Failed to parse crew output: {raw[:200]}",
            "route": "education",
        }
    return state


def _route_lead(state: LeadQualState) -> LeadQualState:
    """Node 3: Route based on composite score."""
    score = state.get("score") or {}
    composite = (
        0.4 * score.get("fit_score", 0)
        + 0.35 * score.get("intent_score", 0)
        + 0.25 * score.get("urgency_score", 0)
    )

    if score.get("fit_score", 0) < 20:
        state["route"] = "disqualify"
    elif composite >= 80:
        state["route"] = "sales"
    elif composite >= 50:
        state["route"] = "nurture"
    else:
        state["route"] = "education"
    return state


def _update_crm(state: LeadQualState) -> LeadQualState:
    """Node 4: Update HubSpot with scores and route."""
    hs = _get_hubspot()
    contact_id = state.get("contact_id", "")
    score = state.get("score") or {}
    route = state.get("route", "")

    if contact_id:
        hs.update_contact(contact_id, {
            "hs_lead_status": route.upper(),
            "lead_score": str(int(
                0.4 * score.get("fit_score", 0)
                + 0.35 * score.get("intent_score", 0)
                + 0.25 * score.get("urgency_score", 0)
            )),
        })
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
