from __future__ import annotations

from crewai import Crew, Task, Process

from vibe_ai_ops.crews.base import create_crew_agent
from vibe_ai_ops.shared.models import AgentConfig


def create_engagement_crew(config: AgentConfig, system_prompt: str) -> Crew:
    """Create the S3 Engagement crew — 3 agents, 3 sequential tasks."""
    researcher = create_crew_agent(
        config=config,
        role="Buyer Researcher",
        goal="Deep-dive into the buyer's situation, pain points, and trigger events",
        backstory=(
            "You research prospects thoroughly — their company, role, challenges, "
            "and what triggered their interest. You find the specific details "
            "that make outreach feel personal, not templated."
        ),
    )

    copywriter = create_crew_agent(
        config=config,
        role="Outreach Copywriter",
        goal="Write personalized multi-touch outreach sequences that get replies",
        backstory=(
            "You write compelling B2B outreach. Every email references something "
            "specific about the prospect. You never use generic templates. "
            "Your sequences have a clear value-add at each touch."
        ),
    )

    strategist = create_crew_agent(
        config=config,
        role="Engagement Strategist",
        goal="Design the optimal multi-channel engagement strategy and timing",
        backstory=(
            "You plan engagement sequences across email and LinkedIn. "
            "You design behavior-responsive triggers and know when to "
            "hand off to a human. You optimize for meetings booked."
        ),
    )

    research_task = Task(
        description=(
            "Research this qualified lead for personalized outreach.\n\n"
            "Buyer profile: {buyer_profile}\n"
            "Segment: {segment}\n\n"
            "Find: specific pain points, trigger events, mutual connections, "
            "recent activity, and angles for personalization."
        ),
        expected_output="Research notes with specific personalization angles",
        agent=researcher,
    )

    sequence_task = Task(
        description=(
            "Write a 4-touch outreach sequence for this lead.\n\n"
            "Day 1: Personalized initial outreach\n"
            "Day 3: Value-add follow-up\n"
            "Day 7: Different angle\n"
            "Day 14: Final touch\n\n"
            "Each touch must reference specific details from research. "
            "Include email subject, body, and LinkedIn message variants."
        ),
        expected_output="4-touch outreach sequence with personalized email and LinkedIn messages",
        agent=copywriter,
    )

    strategy_task = Task(
        description=(
            "Review and finalize the engagement strategy.\n\n"
            "Add: behavior-responsive triggers (email open → case study, "
            "pricing visit → ROI calculator, etc.), channel timing, "
            "and human handoff package with context.\n\n"
            "Return the complete engagement plan as JSON."
        ),
        expected_output="Complete engagement plan JSON with sequence, triggers, and handoff package",
        agent=strategist,
    )

    return Crew(
        agents=[researcher, copywriter, strategist],
        tasks=[research_task, sequence_task, strategy_task],
        process=Process.sequential,
        verbose=False,
    )
