"""MemoryAssembler — builds memory context string for LLM calls.

Assembles from agent insights (L3) + workspace facts + recent episodes (L2).
Filters by clearance. Respects token budget.
"""

from __future__ import annotations

from openvibe_sdk.memory.access import ClearanceProfile
from openvibe_sdk.memory.agent_memory import AgentMemory


class MemoryAssembler:
    """Builds memory context string from scope.

    Priority: insights (L3) > workspace facts > recent episodes (L2).
    """

    def __init__(
        self,
        agent_memory: AgentMemory,
        clearance: ClearanceProfile,
    ) -> None:
        self._memory = agent_memory
        self._clearance = clearance

    def assemble(
        self,
        scope: dict,
        token_budget: int = 2000,
    ) -> str:
        """Build memory context from scope.

        scope keys: entity, domain, tags, query (all optional).
        """
        entity = scope.get("entity")
        domain = scope.get("domain")
        tags = scope.get("tags")
        query = scope.get("query", "")

        parts: list[str] = []

        # Priority 1: Agent insights (L3) — highest signal
        insights = self._memory.recall_insights(
            entity=entity, domain=domain, tags=tags,
            query=query, limit=5,
        )
        if insights:
            lines = [
                f"- {i.content} (confidence: {i.confidence:.1f})"
                for i in insights
            ]
            parts.append("## Insights\n" + "\n".join(lines))

        # Priority 2: Workspace facts — filtered by clearance
        if self._memory.workspace:
            facts = self._memory.workspace.query(
                clearance=self._clearance,
                entity=entity, domain=domain, tags=tags,
                query=query, limit=10,
            )
            if facts:
                lines = [f"- {f.content}" for f in facts]
                parts.append("## Context\n" + "\n".join(lines))

        # Priority 3: Recent episodes (L2)
        episodes = self._memory.recall_episodes(
            entity=entity, domain=domain, tags=tags, limit=3,
        )
        if episodes:
            lines = [f"- {e.action}: {e.output_summary}" for e in episodes]
            parts.append("## Recent Activity\n" + "\n".join(lines))

        result = "\n\n".join(parts)

        # Token budget (rough: 4 chars per token)
        max_chars = token_budget * 4
        if len(result) > max_chars:
            result = result[:max_chars]

        return result
