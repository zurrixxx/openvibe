"""WorkspaceMemory — shared org-level fact store with access control."""

from __future__ import annotations

from datetime import datetime, timezone

from openvibe_sdk.memory.access import ClearanceProfile
from openvibe_sdk.memory.in_memory import InMemoryFactStore
from openvibe_sdk.memory.stores import FactStore
from openvibe_sdk.memory.types import Fact


class WorkspaceMemory:
    """Shared org-level fact store with access control.

    Wraps a FactStore and filters results by clearance.
    V2: InMemoryFactStore backend. V3+: Postgres/pgvector.
    """

    def __init__(self, fact_store: FactStore | None = None) -> None:
        self._store: FactStore = fact_store or InMemoryFactStore()

    def store_fact(self, fact: Fact) -> None:
        self._store.store(fact)

    def query(
        self,
        clearance: ClearanceProfile,
        entity: str | None = None,
        domain: str | None = None,
        tags: list[str] | None = None,
        query: str = "",
        limit: int = 10,
    ) -> list[Fact]:
        # Over-fetch to account for filtering
        candidates = self._store.query(
            entity=entity,
            domain=domain,
            tags=tags,
            query=query,
            limit=limit * 3,
        )
        filtered = [f for f in candidates if clearance.can_access(f)]
        # Track access
        now = datetime.now(timezone.utc)
        for f in filtered[:limit]:
            f.access_count += 1
            f.last_accessed = now
        return filtered[:limit]

    def update_fact(self, fact: Fact) -> None:
        self._store.update(fact)
