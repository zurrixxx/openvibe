"""Memory data types — Fact, Episode, Insight, Classification, RetrievalTrace."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any


class Classification(str, Enum):
    """Access classification for memory entries."""

    PUBLIC = "public"
    INTERNAL = "internal"
    CONFIDENTIAL = "confidential"
    RESTRICTED = "restricted"


@dataclass
class Fact:
    """Atomic unit of knowledge. Base unit of all memory (L1).

    A fact is a single, verifiable piece of information with addressing
    metadata (entity, domain, tags) that enables precise recall.
    """

    id: str
    content: str

    # Addressing (enables precise recall)
    entity: str = ""
    domain: str = ""
    tags: list[str] = field(default_factory=list)

    # Relevance signals
    confidence: float = 1.0
    importance: float = 0.0
    last_accessed: datetime | None = None
    access_count: int = 0

    # Access control
    classification: Classification = Classification.INTERNAL

    # Provenance
    source: str = ""
    created_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    updated_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    supersedes: str | None = None


@dataclass
class Episode:
    """Structured record of a node execution (L2).

    An episode captures what happened during a single agent action,
    including input/output, cost, and addressing metadata.
    """

    id: str
    agent_id: str
    operator_id: str
    node_name: str
    timestamp: datetime
    action: str
    input_summary: str
    output_summary: str
    outcome: dict[str, Any]
    duration_ms: int
    tokens_in: int
    tokens_out: int

    # Addressing
    entity: str = ""
    domain: str = ""
    tags: list[str] = field(default_factory=list)


@dataclass
class Insight:
    """Pattern discovered across episodes (L3).

    An insight is a higher-order observation derived from multiple
    episodes, with confidence tracking and lifecycle status.
    """

    id: str
    agent_id: str
    content: str
    confidence: float
    evidence_count: int
    source_episode_ids: list[str]
    created_at: datetime
    last_confirmed: datetime | None = None
    status: str = "active"

    # Addressing
    entity: str = ""
    domain: str = ""
    tags: list[str] = field(default_factory=list)


@dataclass
class RetrievalTrace:
    """Observable trace of a memory access.

    Captures the what/where/how of every memory operation for
    debugging, cost tracking, and optimization.
    """

    action: str  # "browse" | "read" | "search" | "write"
    path: str
    query: str = ""
    results_count: int = 0
    tokens_loaded: int = 0
    timestamp: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    duration_ms: int = 0
