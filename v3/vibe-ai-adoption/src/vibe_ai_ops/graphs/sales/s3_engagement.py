from __future__ import annotations

from typing import Any, TypedDict

from langgraph.graph import StateGraph, END


class EngagementState(TypedDict, total=False):
    contact_id: str
    buyer_profile: dict[str, Any]
    segment: str
    research_notes: str
    outreach_sequence: list[dict[str, Any]]
    personalized_sequence: list[dict[str, Any]]
    final_plan: dict[str, Any]


def _research_buyer(state: EngagementState) -> EngagementState:
    """Node 1: Deep research on the buyer for personalization."""
    # Will be wired to CrewAI researcher agent
    return state


def _generate_sequence(state: EngagementState) -> EngagementState:
    """Node 2: Generate multi-touch outreach sequence."""
    # Will be wired to CrewAI copywriter agent
    return state


def _personalize(state: EngagementState) -> EngagementState:
    """Node 3: Personalize each touch with research insights."""
    # Will be wired to CrewAI strategist agent
    return state


def _format(state: EngagementState) -> EngagementState:
    """Node 4: Format final engagement plan with triggers and handoff."""
    state["final_plan"] = {
        "contact_id": state.get("contact_id", ""),
        "sequence": state.get("personalized_sequence", []),
        "status": "ready",
    }
    return state


def create_engagement_graph(checkpointer=None):
    """Create the S3 Engagement LangGraph workflow."""
    workflow = StateGraph(EngagementState)

    workflow.add_node("research_buyer", _research_buyer)
    workflow.add_node("generate_sequence", _generate_sequence)
    workflow.add_node("personalize", _personalize)
    workflow.add_node("format", _format)

    workflow.set_entry_point("research_buyer")
    workflow.add_edge("research_buyer", "generate_sequence")
    workflow.add_edge("generate_sequence", "personalize")
    workflow.add_edge("personalize", "format")
    workflow.add_edge("format", END)

    return workflow.compile(checkpointer=checkpointer)
