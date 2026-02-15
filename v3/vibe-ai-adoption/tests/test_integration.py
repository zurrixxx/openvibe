"""Integration test: verify all 3 layers wire together."""
import os
from unittest.mock import patch

from vibe_ai_ops.shared.models import AgentConfig
from vibe_ai_ops.crews.base import create_crew_agent
from vibe_ai_ops.graphs.checkpointer import create_checkpointer
from vibe_ai_ops.temporal.schedules import build_schedule_specs
from vibe_ai_ops.temporal.activities.agent_activity import AgentActivityInput


@patch.dict(os.environ, {"ANTHROPIC_API_KEY": "sk-ant-test-key"})
def test_config_loads_into_all_layers():
    """Config -> CrewAI + LangGraph + Temporal all connect."""
    config = AgentConfig(
        id="m1", name="Segment Research", engine="marketing",
        tier="validation", architecture="temporal_crewai",
        trigger={"type": "cron", "schedule": "0 9 * * 1"},
        output_channel="slack:#marketing-agents",
        prompt_file="marketing/m1_segment_research.md",
    )

    # Layer 3: CrewAI — can create an agent
    agent = create_crew_agent(
        config=config,
        role="Market Research Specialist",
        goal="Identify micro-segments",
        backstory="You are Vibe's market researcher.",
    )
    assert agent.role == "Market Research Specialist"

    # Layer 2: LangGraph — can create a checkpointer
    cp = create_checkpointer(conn_string=None)
    assert cp is not None

    # Layer 1: Temporal — can build schedule specs
    specs = build_schedule_specs([config])
    assert len(specs) == 1
    assert specs[0]["agent_id"] == "m1"

    # Activity input works
    inp = AgentActivityInput(
        agent_id="m1",
        agent_config_path="config/agents.yaml",
        input_data={"segments": ["enterprise-fintech"]},
    )
    assert inp.agent_id == "m1"
