import os
from unittest.mock import patch

from vibe_ai_ops.crews.sales.s3_engagement import create_engagement_crew
from vibe_ai_ops.shared.models import AgentConfig


def _make_config():
    return AgentConfig(
        id="s3", name="Engagement", engine="sales",
        tier="deep_dive", architecture="temporal_langgraph_crewai",
        trigger={"type": "event", "event_source": "s1:qualified"},
        output_channel="slack:#sales-agents",
        prompt_file="sales/s3_engagement.md",
    )


@patch.dict(os.environ, {"ANTHROPIC_API_KEY": "sk-ant-test-key"})
def test_create_engagement_crew():
    crew = create_engagement_crew(_make_config(), "You create outreach sequences.")
    assert len(crew.agents) == 3
    assert len(crew.tasks) == 3


@patch.dict(os.environ, {"ANTHROPIC_API_KEY": "sk-ant-test-key"})
def test_crew_agents_have_distinct_roles():
    crew = create_engagement_crew(_make_config(), "Engagement agent.")
    roles = [a.role for a in crew.agents]
    assert "Buyer Researcher" in roles
    assert "Outreach Copywriter" in roles
    assert "Engagement Strategist" in roles
