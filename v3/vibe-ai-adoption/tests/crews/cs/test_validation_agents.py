import os
from unittest.mock import patch

from vibe_ai_ops.crews.cs.validation_agents import (
    create_c1_crew, create_c2_crew, create_c3_crew,
    create_c4_crew, create_c5_crew, CS_CREW_REGISTRY,
)
from vibe_ai_ops.shared.models import AgentConfig


def _make_config(agent_id: str, name: str):
    return AgentConfig(
        id=agent_id, name=name, engine="cs",
        tier="validation", architecture="temporal_crewai",
        trigger={"type": "cron", "schedule": "0 10 * * 2"},
        output_channel="slack:#cs-agents",
        prompt_file=f"cs/{agent_id}_{name.lower().replace(' ', '_')}.md",
    )


@patch.dict(os.environ, {"ANTHROPIC_API_KEY": "sk-ant-test-key"})
def test_create_c1_crew():
    crew = create_c1_crew(_make_config("c1", "Onboarding"), "You onboard customers.")
    assert len(crew.agents) == 1 and len(crew.tasks) == 1


@patch.dict(os.environ, {"ANTHROPIC_API_KEY": "sk-ant-test-key"})
def test_create_c2_crew():
    crew = create_c2_crew(_make_config("c2", "Success Advisor"), "You advise customers.")
    assert len(crew.agents) == 1 and len(crew.tasks) == 1


@patch.dict(os.environ, {"ANTHROPIC_API_KEY": "sk-ant-test-key"})
def test_create_c3_crew():
    crew = create_c3_crew(_make_config("c3", "Health Intelligence"), "You monitor health.")
    assert len(crew.agents) == 1 and len(crew.tasks) == 1


@patch.dict(os.environ, {"ANTHROPIC_API_KEY": "sk-ant-test-key"})
def test_create_c4_crew():
    crew = create_c4_crew(_make_config("c4", "Expansion"), "You find upsells.")
    assert len(crew.agents) == 1 and len(crew.tasks) == 1


@patch.dict(os.environ, {"ANTHROPIC_API_KEY": "sk-ant-test-key"})
def test_create_c5_crew():
    crew = create_c5_crew(_make_config("c5", "Customer Voice"), "You aggregate signals.")
    assert len(crew.agents) == 1 and len(crew.tasks) == 1


def test_cs_registry_has_all_agents():
    assert set(CS_CREW_REGISTRY.keys()) == {"c1", "c2", "c3", "c4", "c5"}
