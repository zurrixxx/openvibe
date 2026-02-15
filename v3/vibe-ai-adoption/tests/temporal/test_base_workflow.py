import pytest
from unittest.mock import patch

from vibe_ai_ops.temporal.activities.agent_activity import (
    run_validation_agent,
    AgentActivityInput,
    AgentActivityOutput,
)


@pytest.mark.asyncio
async def test_agent_activity_input_model():
    inp = AgentActivityInput(
        agent_id="m1",
        agent_config_path="config/agents.yaml",
        input_data={"segments": ["enterprise-fintech"]},
    )
    assert inp.agent_id == "m1"


@pytest.mark.asyncio
@patch("vibe_ai_ops.temporal.activities.agent_activity._execute_agent")
async def test_run_validation_agent(mock_execute):
    mock_execute.return_value = AgentActivityOutput(
        agent_id="m1",
        status="success",
        content="Segment analysis for enterprise-fintech...",
        cost_usd=0.03,
        duration_seconds=4.5,
    )

    result = await run_validation_agent(AgentActivityInput(
        agent_id="m1",
        agent_config_path="config/agents.yaml",
        input_data={"segments": ["enterprise-fintech"]},
    ))

    assert result.status == "success"
    assert result.agent_id == "m1"
