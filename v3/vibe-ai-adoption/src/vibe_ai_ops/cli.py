from __future__ import annotations

import argparse
import json
import sys
from typing import Any

from vibe_ai_ops.shared.config import load_agent_configs
from vibe_ai_ops.shared.models import AgentConfig, ArchitectureType
from vibe_ai_ops.main import CREW_REGISTRY


def list_agents(
    config_path: str = "config/agents.yaml",
    engine: str | None = None,
) -> list[dict[str, Any]]:
    """List all agents, optionally filtered by engine."""
    configs = load_agent_configs(config_path, enabled_only=True)
    if engine:
        configs = [c for c in configs if c.engine == engine]
    return [
        {
            "id": c.id,
            "name": c.name,
            "engine": c.engine,
            "tier": c.tier.value,
            "architecture": c.architecture.value,
            "trigger": c.trigger.type.value,
            "schedule": c.trigger.schedule,
        }
        for c in configs
    ]


def get_agent_info(
    agent_id: str,
    config_path: str = "config/agents.yaml",
) -> dict[str, Any] | None:
    """Get detailed info for a single agent."""
    configs = load_agent_configs(config_path)
    config = next((c for c in configs if c.id == agent_id), None)
    if not config:
        return None
    return {
        "id": config.id,
        "name": config.name,
        "engine": config.engine,
        "tier": config.tier.value,
        "architecture": config.architecture.value,
        "trigger": config.trigger.type.value,
        "schedule": config.trigger.schedule,
        "output_channel": config.output_channel,
        "model": config.model,
        "max_tokens": config.max_tokens,
        "temperature": config.temperature,
        "has_crew": config.id in CREW_REGISTRY,
        "enabled": config.enabled,
    }


def get_system_summary(
    config_path: str = "config/agents.yaml",
) -> dict[str, Any]:
    """Get a summary of the entire agent system."""
    configs = load_agent_configs(config_path, enabled_only=True)
    deep_dive = [c for c in configs if c.architecture == ArchitectureType.TEMPORAL_LANGGRAPH_CREWAI]
    validation = [c for c in configs if c.architecture == ArchitectureType.TEMPORAL_CREWAI]
    cron = [c for c in configs if c.trigger.type.value == "cron"]
    engines = sorted(set(c.engine for c in configs))

    return {
        "total_agents": len(configs),
        "deep_dive_count": len(deep_dive),
        "validation_count": len(validation),
        "cron_count": len(cron),
        "engines": engines,
        "deep_dive_agents": [c.id for c in deep_dive],
        "registered_crews": len(CREW_REGISTRY),
    }


def _cmd_list(args: argparse.Namespace) -> None:
    agents = list_agents(engine=args.engine)
    if not agents:
        print("No agents found.")
        return
    # Table format
    print(f"{'ID':<5} {'Name':<25} {'Engine':<12} {'Tier':<12} {'Trigger':<10} {'Schedule'}")
    print("-" * 85)
    for a in agents:
        schedule = a["schedule"] or ""
        print(f"{a['id']:<5} {a['name']:<25} {a['engine']:<12} {a['tier']:<12} {a['trigger']:<10} {schedule}")
    print(f"\n{len(agents)} agents")


def _cmd_info(args: argparse.Namespace) -> None:
    info = get_agent_info(args.agent_id)
    if not info:
        print(f"Agent '{args.agent_id}' not found.")
        sys.exit(1)
    for k, v in info.items():
        print(f"  {k}: {v}")


def _cmd_summary(args: argparse.Namespace) -> None:
    summary = get_system_summary()
    print(f"Total agents:     {summary['total_agents']}")
    print(f"Deep-dive:        {summary['deep_dive_count']} ({', '.join(summary['deep_dive_agents'])})")
    print(f"Validation:       {summary['validation_count']}")
    print(f"Cron-scheduled:   {summary['cron_count']}")
    print(f"Engines:          {', '.join(summary['engines'])}")
    print(f"Registered crews: {summary['registered_crews']}")


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(prog="vibe-ai-ops", description="Vibe AI Ops CLI")
    sub = parser.add_subparsers(dest="command")

    # list
    p_list = sub.add_parser("list", help="List all agents")
    p_list.add_argument("--engine", help="Filter by engine (marketing|sales|cs|intelligence)")
    p_list.set_defaults(func=_cmd_list)

    # info
    p_info = sub.add_parser("info", help="Show agent details")
    p_info.add_argument("agent_id", help="Agent ID (e.g. s1, m3)")
    p_info.set_defaults(func=_cmd_info)

    # summary
    p_summary = sub.add_parser("summary", help="System summary")
    p_summary.set_defaults(func=_cmd_summary)

    args = parser.parse_args(argv)
    if not args.command:
        parser.print_help()
        sys.exit(1)
    args.func(args)


if __name__ == "__main__":
    main()
