"""MemoryFilesystem — virtual filesystem interface over memory stores.

Provides browse/read/search/write that the LLM uses to navigate its own memory.
Maps virtual paths to AgentMemory store queries.

Path structure:
    /identity/soul.md         -> soul text (read-only)
    /knowledge/{domain}/...   -> insights (InsightStore)
    /experience/{date}/...    -> episodes (EpisodicStore)
    /references/{domain}/...  -> workspace facts (external sources)
"""

from __future__ import annotations

import time
import uuid
from datetime import datetime, timezone
from typing import Any

from openvibe_sdk.memory.agent_memory import AgentMemory
from openvibe_sdk.memory.types import Episode, Insight, RetrievalTrace


class MemoryFilesystem:
    """Virtual filesystem interface over memory stores."""

    # Directories available in V2
    _ROOT_DIRS = ["identity", "knowledge", "experience", "references"]

    def __init__(
        self,
        role_id: str,
        agent_memory: AgentMemory,
        soul: str = "",
    ) -> None:
        self._role_id = role_id
        self._memory = agent_memory
        self._soul = soul
        self._traces: list[RetrievalTrace] = []

    @property
    def traces(self) -> list[RetrievalTrace]:
        return list(self._traces)

    def clear_traces(self) -> None:
        self._traces.clear()

    def browse(self, path: str = "/") -> list[str]:
        """List entries at path."""
        start = time.monotonic()
        path = path.strip("/")
        parts = path.split("/") if path else []

        if not parts:
            entries = list(self._ROOT_DIRS)
        elif parts[0] == "identity":
            entries = ["soul.md"] if self._soul else []
        elif parts[0] == "knowledge":
            entries = self._browse_knowledge(parts[1:])
        elif parts[0] == "experience":
            entries = self._browse_experience(parts[1:])
        elif parts[0] == "references":
            entries = self._browse_references(parts[1:])
        else:
            entries = []

        duration_ms = int((time.monotonic() - start) * 1000)
        self._traces.append(RetrievalTrace(
            action="browse", path=f"/{path}/" if path else "/",
            results_count=len(entries), duration_ms=duration_ms,
        ))
        return entries

    def read(self, path: str) -> str:
        """Read content at path."""
        start = time.monotonic()
        path = path.strip("/")
        parts = path.split("/") if path else []
        content = ""

        if len(parts) >= 2 and parts[0] == "identity" and parts[1] == "soul.md":
            content = self._soul
        elif len(parts) >= 2 and parts[0] == "knowledge":
            content = self._read_knowledge(parts[1:])
        elif len(parts) >= 2 and parts[0] == "experience":
            content = self._read_experience(parts[1:])
        elif len(parts) >= 2 and parts[0] == "references":
            content = self._read_references(parts[1:])

        tokens = len(content) // 4  # rough estimate
        duration_ms = int((time.monotonic() - start) * 1000)
        self._traces.append(RetrievalTrace(
            action="read", path=f"/{path}",
            tokens_loaded=tokens, duration_ms=duration_ms,
        ))
        return content

    def search(self, query: str, scope: str = "/") -> list[dict[str, Any]]:
        """Search within scope. Returns [{path, content, score}]."""
        start = time.monotonic()
        scope = scope.strip("/")
        parts = scope.split("/") if scope else []
        results: list[dict[str, Any]] = []

        domain = parts[1] if len(parts) >= 2 and parts[0] == "knowledge" else None

        # Search insights
        insights = self._memory.recall_insights(
            domain=domain, query=query, limit=10,
        )
        for ins in insights:
            results.append({
                "path": f"/knowledge/{ins.domain or '_'}/{ins.id}",
                "content": ins.content,
                "confidence": ins.confidence,
            })

        # Search episodes (only when scope is global or experience)
        if not parts or parts[0] in ("", "experience"):
            episodes = self._memory.recall_episodes(limit=5)
            for ep in episodes:
                if query.lower() in ep.output_summary.lower():
                    results.append({
                        "path": f"/experience/{ep.id}",
                        "content": ep.output_summary,
                    })

        duration_ms = int((time.monotonic() - start) * 1000)
        self._traces.append(RetrievalTrace(
            action="search", path=f"/{scope}" if scope else "/",
            query=query, results_count=len(results),
            duration_ms=duration_ms,
        ))
        return results

    def write(self, path: str, content: str, **metadata: Any) -> None:
        """Write content at path. Path determines store type."""
        start = time.monotonic()
        path = path.strip("/")
        parts = path.split("/") if path else []

        if len(parts) >= 2 and parts[0] == "knowledge":
            domain = parts[1] if len(parts) >= 2 else ""
            tags = parts[2:-1] if len(parts) > 3 else []
            self._memory.store_insight(Insight(
                id=parts[-1] if len(parts) >= 3 else uuid.uuid4().hex[:8],
                agent_id=self._role_id,
                content=content,
                confidence=metadata.get("confidence", 0.5),
                evidence_count=1,
                source_episode_ids=[],
                created_at=datetime.now(timezone.utc),
                domain=domain,
                tags=tags,
            ))
        elif len(parts) >= 2 and parts[0] == "experience":
            self._memory.record_episode(Episode(
                id=parts[-1] if len(parts) >= 2 else uuid.uuid4().hex[:8],
                agent_id=self._role_id,
                operator_id=metadata.get("operator_id", ""),
                node_name=metadata.get("node_name", ""),
                timestamp=datetime.now(timezone.utc),
                action=parts[-1] if len(parts) >= 2 else "write",
                input_summary="",
                output_summary=content[:200],
                outcome={"content": content},
                duration_ms=0,
                tokens_in=0,
                tokens_out=0,
                domain=metadata.get("domain", ""),
            ))

        duration_ms = int((time.monotonic() - start) * 1000)
        self._traces.append(RetrievalTrace(
            action="write", path=f"/{path}",
            duration_ms=duration_ms,
        ))

    # --- Private helpers ---

    def _browse_knowledge(self, parts: list[str]) -> list[str]:
        """Browse /knowledge/ — lists domains, then insights within domain."""
        if not parts:
            # List all domains
            insights = self._memory.recall_insights(limit=100)
            domains = {i.domain for i in insights if i.domain}
            return sorted(domains)
        # List insights in domain
        domain = parts[0]
        insights = self._memory.recall_insights(domain=domain, limit=50)
        return [i.id for i in insights]

    def _browse_experience(self, parts: list[str]) -> list[str]:
        """Browse /experience/ — lists episodes."""
        episodes = self._memory.recall_episodes(limit=50)
        return [ep.id for ep in episodes]

    def _browse_references(self, parts: list[str]) -> list[str]:
        """Browse /references/ — lists workspace facts (external)."""
        if not self._memory.workspace:
            return []
        # Would need clearance to query — return empty for now
        return []

    def _read_knowledge(self, parts: list[str]) -> str:
        """Read /knowledge/{domain}/{id}."""
        if len(parts) < 2:
            return ""
        domain = parts[0]
        insight_id = parts[1]
        insights = self._memory.recall_insights(domain=domain, limit=100)
        for ins in insights:
            if ins.id == insight_id:
                return f"{ins.content}\n\nConfidence: {ins.confidence}\nEvidence: {ins.evidence_count}"
        return ""

    def _read_experience(self, parts: list[str]) -> str:
        """Read /experience/{id}."""
        if not parts:
            return ""
        ep_id = parts[-1]
        episodes = self._memory.recall_episodes(limit=100)
        for ep in episodes:
            if ep.id == ep_id:
                return (
                    f"Action: {ep.action}\n"
                    f"Input: {ep.input_summary}\n"
                    f"Output: {ep.output_summary}\n"
                    f"Duration: {ep.duration_ms}ms"
                )
        return ""

    def _read_references(self, parts: list[str]) -> str:
        """Read /references/{domain}/{id}."""
        return ""  # requires clearance — implement in V3
