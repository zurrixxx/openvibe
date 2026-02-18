"""Tests for V2 memory types: Classification, Fact, Episode, Insight, RetrievalTrace."""

from datetime import datetime, timezone

from openvibe_sdk.memory.types import (
    Classification,
    Episode,
    Fact,
    Insight,
    RetrievalTrace,
)


def test_classification_values():
    assert Classification.PUBLIC == "public"
    assert Classification.INTERNAL == "internal"
    assert Classification.CONFIDENTIAL == "confidential"
    assert Classification.RESTRICTED == "restricted"


def test_fact_creation():
    f = Fact(id="f1", content="Acme has 200 employees")
    assert f.id == "f1"
    assert f.content == "Acme has 200 employees"
    assert f.entity == ""
    assert f.domain == ""
    assert f.tags == []
    assert f.confidence == 1.0
    assert f.importance == 0.0
    assert f.access_count == 0
    assert f.classification == Classification.INTERNAL
    assert f.source == ""
    assert f.created_at is not None
    assert f.updated_at is not None
    assert f.last_accessed is None
    assert f.supersedes is None


def test_fact_with_addressing():
    f = Fact(
        id="f2",
        content="Acme scored 85",
        entity="acme_corp",
        domain="revenue",
        tags=["qualification", "scoring"],
        classification=Classification.CONFIDENTIAL,
        source="revenue_ops",
    )
    assert f.entity == "acme_corp"
    assert f.domain == "revenue"
    assert f.tags == ["qualification", "scoring"]
    assert f.classification == Classification.CONFIDENTIAL


def test_episode_creation():
    now = datetime.now(timezone.utc)
    ep = Episode(
        id="ep1",
        agent_id="cro",
        operator_id="revenue_ops",
        node_name="qualify",
        timestamp=now,
        action="qualify_lead",
        input_summary="Score lead Acme",
        output_summary='{"score": 85}',
        outcome={"score": 85},
        duration_ms=450,
        tokens_in=100,
        tokens_out=200,
    )
    assert ep.id == "ep1"
    assert ep.agent_id == "cro"
    assert ep.entity == ""
    assert ep.domain == ""
    assert ep.tags == []


def test_episode_with_addressing():
    now = datetime.now(timezone.utc)
    ep = Episode(
        id="ep2",
        agent_id="cro",
        operator_id="revenue_ops",
        node_name="qualify",
        timestamp=now,
        action="qualify_lead",
        input_summary="Score lead",
        output_summary="85",
        outcome={},
        duration_ms=100,
        tokens_in=10,
        tokens_out=20,
        entity="acme_corp",
        domain="revenue",
        tags=["qualification"],
    )
    assert ep.entity == "acme_corp"
    assert ep.domain == "revenue"


def test_insight_creation():
    now = datetime.now(timezone.utc)
    ins = Insight(
        id="ins1",
        agent_id="cro",
        content="Webinar leads convert 2x vs cold",
        confidence=0.8,
        evidence_count=5,
        source_episode_ids=["ep1", "ep2"],
        created_at=now,
    )
    assert ins.content == "Webinar leads convert 2x vs cold"
    assert ins.confidence == 0.8
    assert ins.status == "active"


def test_insight_defaults():
    now = datetime.now(timezone.utc)
    ins = Insight(
        id="ins2",
        agent_id="cro",
        content="test",
        confidence=0.5,
        evidence_count=1,
        source_episode_ids=[],
        created_at=now,
    )
    assert ins.last_confirmed is None
    assert ins.status == "active"
    assert ins.entity == ""
    assert ins.domain == ""
    assert ins.tags == []


def test_retrieval_trace():
    t = RetrievalTrace(
        action="search",
        path="/knowledge/sales/",
        query="VP sponsor",
        results_count=2,
        tokens_loaded=340,
    )
    assert t.action == "search"
    assert t.path == "/knowledge/sales/"
    assert t.duration_ms == 0
    assert t.timestamp is not None
