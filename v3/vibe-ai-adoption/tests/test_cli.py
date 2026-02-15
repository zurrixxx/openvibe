"""Tests for CLI."""
import os
from unittest.mock import patch

from vibe_ai_ops.cli import list_agents, get_agent_info, get_system_summary


@patch.dict(os.environ, {"ANTHROPIC_API_KEY": "sk-ant-test-key"})
def test_list_agents():
    agents = list_agents(config_path="config/agents.yaml")
    assert len(agents) == 20
    assert all("id" in a and "name" in a for a in agents)


@patch.dict(os.environ, {"ANTHROPIC_API_KEY": "sk-ant-test-key"})
def test_list_agents_filter_by_engine():
    agents = list_agents(config_path="config/agents.yaml", engine="marketing")
    assert len(agents) == 6
    assert all(a["engine"] == "marketing" for a in agents)


@patch.dict(os.environ, {"ANTHROPIC_API_KEY": "sk-ant-test-key"})
def test_get_agent_info():
    info = get_agent_info("s1", config_path="config/agents.yaml")
    assert info is not None
    assert info["id"] == "s1"
    assert info["name"] == "Lead Qualification"
    assert info["architecture"] == "temporal_langgraph_crewai"
    assert info["has_crew"] is True


@patch.dict(os.environ, {"ANTHROPIC_API_KEY": "sk-ant-test-key"})
def test_get_agent_info_not_found():
    info = get_agent_info("x99", config_path="config/agents.yaml")
    assert info is None


@patch.dict(os.environ, {"ANTHROPIC_API_KEY": "sk-ant-test-key"})
def test_get_system_summary():
    summary = get_system_summary(config_path="config/agents.yaml")
    assert summary["total_agents"] == 20
    assert summary["deep_dive_count"] == 3
    assert summary["validation_count"] == 17
    assert summary["cron_count"] > 0
    assert set(summary["engines"]) == {"marketing", "sales", "cs", "intelligence"}
