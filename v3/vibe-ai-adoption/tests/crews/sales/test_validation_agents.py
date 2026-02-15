import os
from unittest.mock import patch

from vibe_ai_ops.crews.sales.validation_agents import (
    create_s2_crew,
    create_s4_crew,
    create_s5_crew,
    SALES_CREW_REGISTRY,
)
from vibe_ai_ops.shared.models import AgentConfig


def _make_config(agent_id: str, name: str):
    return AgentConfig(
        id=agent_id, name=name, engine="sales",
        tier="validation", architecture="temporal_crewai",
        trigger={"type": "cron", "schedule": "0 7 * * *"},
        output_channel="slack:#sales-agents",
        prompt_file=f"sales/{agent_id}_{name.lower().replace(' ', '_')}.md",
    )


@patch.dict(os.environ, {"ANTHROPIC_API_KEY": "sk-ant-test-key"})
def test_create_s2_crew():
    crew = create_s2_crew(_make_config("s2", "Buyer Intelligence"), "You research buyers.")
    assert len(crew.agents) == 1
    assert len(crew.tasks) == 1


@patch.dict(os.environ, {"ANTHROPIC_API_KEY": "sk-ant-test-key"})
def test_create_s4_crew():
    crew = create_s4_crew(_make_config("s4", "Deal Support"), "You support deals.")
    assert len(crew.agents) == 1
    assert len(crew.tasks) == 1


@patch.dict(os.environ, {"ANTHROPIC_API_KEY": "sk-ant-test-key"})
def test_create_s5_crew():
    crew = create_s5_crew(_make_config("s5", "Nurture"), "You nurture leads.")
    assert len(crew.agents) == 1
    assert len(crew.tasks) == 1


def test_registry_has_all_sales_validation_agents():
    assert set(SALES_CREW_REGISTRY.keys()) == {"s2", "s4", "s5"}
