from __future__ import annotations

from crewai import Crew

from vibe_ai_ops.crews.base import create_validation_crew
from vibe_ai_ops.shared.models import AgentConfig


def create_r1_crew(config: AgentConfig, system_prompt: str) -> Crew:
    """R1 Funnel Monitor — single agent validation crew."""
    return create_validation_crew(
        config=config,
        role="Revenue Funnel Monitor",
        goal="Real-time monitoring of the complete revenue funnel across all engines",
        backstory=system_prompt,
        task_description=(
            "Analyze funnel metrics across Marketing → Sales → CS.\n"
            "Track: impressions, clicks, leads, meetings, proposals, closed deals, "
            "onboarding, health, expansion, churn.\n"
            "Detect anomalies deviating >2 std dev from baseline.\n\n"
            "Metrics data: {metrics}"
        ),
        expected_output="Funnel summary JSON with anomalies, attribution, and recommendations",
    )


def create_r2_crew(config: AgentConfig, system_prompt: str) -> Crew:
    """R2 Deal Risk & Forecast — single agent validation crew."""
    return create_validation_crew(
        config=config,
        role="Deal Risk & Forecast Analyst",
        goal="Score deal risk, forecast revenue, and provide coaching intelligence",
        backstory=system_prompt,
        task_description=(
            "Analyze all active deals. Score risk (0-100) based on: activity gaps, "
            "stage SLA breach, missing elements, buyer behavior, historical patterns.\n"
            "Generate system forecast and compare to rep submissions.\n\n"
            "Deal data: {deal_data}"
        ),
        expected_output="Risk scores + forecast JSON with deal narratives and recommended actions",
    )


def create_r3_crew(config: AgentConfig, system_prompt: str) -> Crew:
    """R3 Conversation Analysis — single agent validation crew."""
    return create_validation_crew(
        config=config,
        role="Conversation Analysis Specialist",
        goal="Score and analyze rep calls to identify coaching opportunities",
        backstory=system_prompt,
        task_description=(
            "Analyze this week's call transcripts. Score: discovery quality, "
            "value prop delivery, objection handling, next steps, active listening.\n"
            "Generate per-rep coaching packs (3 improve, 3 well-done).\n"
            "Identify team patterns and training gaps.\n\n"
            "Call data: {call_data}"
        ),
        expected_output="Weekly coaching report JSON with per-rep packs and team patterns",
    )


def create_r4_crew(config: AgentConfig, system_prompt: str) -> Crew:
    """R4 NL Revenue Interface — single agent validation crew."""
    return create_validation_crew(
        config=config,
        role="Revenue Intelligence Analyst",
        goal="Answer ad-hoc questions about revenue metrics using natural language",
        backstory=system_prompt,
        task_description=(
            "Answer this revenue question using data from all 3 engines.\n"
            "Query: {query}\n\n"
            "Return structured data with tables, summaries, or trend analysis as appropriate."
        ),
        expected_output="Answer JSON with data, visualization hint, and follow-up suggestions",
    )


INTELLIGENCE_CREW_REGISTRY = {
    "r1": create_r1_crew,
    "r2": create_r2_crew,
    "r3": create_r3_crew,
    "r4": create_r4_crew,
}
