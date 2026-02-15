from __future__ import annotations

from crewai import Crew

from vibe_ai_ops.crews.base import create_validation_crew
from vibe_ai_ops.shared.models import AgentConfig


def create_c1_crew(config: AgentConfig, system_prompt: str) -> Crew:
    """C1 Onboarding — single agent validation crew."""
    return create_validation_crew(
        config=config,
        role="Customer Onboarding Specialist",
        goal="Create and execute personalized onboarding journeys for new customers",
        backstory=system_prompt,
        task_description=(
            "Create a 30-day onboarding plan for this new customer.\n"
            "Customize to their use case and deal context.\n"
            "Include: timeline, feature walkthroughs, success milestones, stuck detection.\n\n"
            "Customer data: {customer_data}"
        ),
        expected_output="Personalized onboarding plan JSON with timeline and success criteria",
    )


def create_c2_crew(config: AgentConfig, system_prompt: str) -> Crew:
    """C2 Success Advisor — single agent validation crew."""
    return create_validation_crew(
        config=config,
        role="Customer Success Advisor",
        goal="Provide proactive guidance to help customers realize value",
        backstory=system_prompt,
        task_description=(
            "Analyze this customer's usage and generate proactive recommendations.\n"
            "Compare features used vs available, identify adoption gaps, "
            "and suggest specific actions to increase value.\n\n"
            "Usage data: {usage_data}"
        ),
        expected_output="Success report JSON with usage summary, recommendations, and health indicator",
    )


def create_c3_crew(config: AgentConfig, system_prompt: str) -> Crew:
    """C3 Health Intelligence — single agent validation crew."""
    return create_validation_crew(
        config=config,
        role="Customer Health Analyst",
        goal="Monitor customer health daily and predict churn with 30-60 day lead time",
        backstory=system_prompt,
        task_description=(
            "Compute health score for this customer.\n"
            "Components: Usage (40%), Engagement (20%), Support (20%), Business (20%).\n"
            "Identify predictive signals and intervention triggers.\n\n"
            "Customer metrics: {metrics}"
        ),
        expected_output="Health score JSON with components, trend, churn risk, and intervention triggers",
    )


def create_c4_crew(config: AgentConfig, system_prompt: str) -> Crew:
    """C4 Expansion — single agent validation crew."""
    return create_validation_crew(
        config=config,
        role="Customer Expansion Specialist",
        goal="Identify upsell and expansion opportunities with custom proposals",
        backstory=system_prompt,
        task_description=(
            "Scan this customer for expansion signals.\n"
            "Check: usage limits, team growth, new use cases, renewal timing.\n"
            "If opportunity found, generate custom proposal with ROI projection.\n\n"
            "Account data: {account_data}"
        ),
        expected_output="Expansion opportunity JSON with signals, proposal, and timing recommendation",
    )


def create_c5_crew(config: AgentConfig, system_prompt: str) -> Crew:
    """C5 Customer Voice — single agent validation crew."""
    return create_validation_crew(
        config=config,
        role="Customer Voice Analyst",
        goal="Aggregate and synthesize all customer signals into actionable intelligence",
        backstory=system_prompt,
        task_description=(
            "Aggregate customer signals from support, NPS, calls, usage, social, community.\n"
            "Produce weekly synthesis: top 10 pain points (ranked by revenue impact), "
            "feature requests by segment, competitive mentions, success/failure patterns.\n\n"
            "Signal data: {signal_data}"
        ),
        expected_output="Weekly customer voice report JSON with pain points, requests, and action items",
    )


CS_CREW_REGISTRY = {
    "c1": create_c1_crew,
    "c2": create_c2_crew,
    "c3": create_c3_crew,
    "c4": create_c4_crew,
    "c5": create_c5_crew,
}
