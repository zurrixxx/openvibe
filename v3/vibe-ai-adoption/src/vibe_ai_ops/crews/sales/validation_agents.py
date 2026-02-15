from __future__ import annotations

from crewai import Crew

from vibe_ai_ops.crews.base import create_validation_crew
from vibe_ai_ops.shared.models import AgentConfig


def create_s2_crew(config: AgentConfig, system_prompt: str) -> Crew:
    """S2 Buyer Intelligence — single agent validation crew."""
    return create_validation_crew(
        config=config,
        role="Buyer Intelligence Specialist",
        goal="Continuously research and profile qualified leads and prospects",
        backstory=system_prompt,
        task_description=(
            "Research this lead/prospect. Produce a comprehensive buyer profile covering: "
            "company deep-dive (business model, revenue, growth, tech stack, competitors, news), "
            "person deep-dive (career, communication style, decision role), "
            "competitive positioning, and pre-call brief if meeting scheduled.\n\n"
            "Lead data: {lead_data}"
        ),
        expected_output="Comprehensive buyer profile JSON with all sections",
    )


def create_s4_crew(config: AgentConfig, system_prompt: str) -> Crew:
    """S4 Deal Support — single agent validation crew."""
    return create_validation_crew(
        config=config,
        role="Deal Support Specialist",
        goal="Provide everything an AE needs to advance and close active deals",
        backstory=system_prompt,
        task_description=(
            "Support this active deal. Based on the request type, produce:\n"
            "- Pre-call prep: buyer profile, suggested agenda, objection handling\n"
            "- Post-call: summary, action items, follow-up draft, risk assessment\n"
            "- Proposal: custom proposal with ROI projection\n"
            "- Stall intervention: re-engagement strategy\n\n"
            "Deal data: {deal_data}"
        ),
        expected_output="Deal support document JSON with content and recommended actions",
    )


def create_s5_crew(config: AgentConfig, system_prompt: str) -> Crew:
    """S5 Nurture — single agent validation crew."""
    return create_validation_crew(
        config=config,
        role="Lead Nurture Specialist",
        goal="Build long-term relationships with leads not yet ready to buy",
        backstory=system_prompt,
        task_description=(
            "Create or update a nurture plan for this lead (scored 50-79).\n"
            "Progress through stages: educational → solution-aware → product-aware → decision-ready.\n"
            "Monitor behavior signals and escalate when score crosses 80.\n"
            "Every touch must add value — never 'just checking in'.\n\n"
            "Lead data: {lead_data}"
        ),
        expected_output="Nurture plan JSON with current stage, next touch, score update",
    )


SALES_CREW_REGISTRY = {
    "s2": create_s2_crew,
    "s4": create_s4_crew,
    "s5": create_s5_crew,
}
