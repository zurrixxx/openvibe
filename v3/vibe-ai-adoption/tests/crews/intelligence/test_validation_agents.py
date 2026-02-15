import os
from unittest.mock import patch

from vibe_ai_ops.crews.intelligence.validation_agents import (
    create_r1_crew, create_r2_crew, create_r3_crew, create_r4_crew,
    INTELLIGENCE_CREW_REGISTRY,
)
from vibe_ai_ops.shared.models import AgentConfig


def _make_config(agent_id: str, name: str):
    return AgentConfig(
        id=agent_id, name=name, engine="intelligence",
        tier="validation", architecture="temporal_crewai",
        trigger={"type": "cron", "schedule": "0 6 * * *"},
        output_channel="slack:#revenue-intelligence",
        prompt_file=f"intelligence/{agent_id}_{name.lower().replace(' ', '_')}.md",
    )


@patch.dict(os.environ, {"ANTHROPIC_API_KEY": "sk-ant-test-key"})
def test_create_r1_crew():
    crew = create_r1_crew(_make_config("r1", "Funnel Monitor"), "You monitor funnels.")
    assert len(crew.agents) == 1 and len(crew.tasks) == 1


@patch.dict(os.environ, {"ANTHROPIC_API_KEY": "sk-ant-test-key"})
def test_create_r2_crew():
    crew = create_r2_crew(_make_config("r2", "Deal Risk"), "You score deal risk.")
    assert len(crew.agents) == 1 and len(crew.tasks) == 1


@patch.dict(os.environ, {"ANTHROPIC_API_KEY": "sk-ant-test-key"})
def test_create_r3_crew():
    crew = create_r3_crew(_make_config("r3", "Conversation Analysis"), "You analyze calls.")
    assert len(crew.agents) == 1 and len(crew.tasks) == 1


@patch.dict(os.environ, {"ANTHROPIC_API_KEY": "sk-ant-test-key"})
def test_create_r4_crew():
    crew = create_r4_crew(_make_config("r4", "NL Revenue"), "You answer revenue questions.")
    assert len(crew.agents) == 1 and len(crew.tasks) == 1


def test_intelligence_registry_has_all_agents():
    assert set(INTELLIGENCE_CREW_REGISTRY.keys()) == {"r1", "r2", "r3", "r4"}
