"""Tests for MemoryFilesystem — virtual filesystem interface over memory stores."""

from datetime import datetime, timezone

from openvibe_sdk.memory.agent_memory import AgentMemory
from openvibe_sdk.memory.filesystem import MemoryFilesystem
from openvibe_sdk.memory.types import Episode, Insight
from openvibe_sdk.memory.workspace import WorkspaceMemory
from openvibe_sdk.memory.types import Classification, Fact


# --- Browse ---

def test_browse_root():
    mem = AgentMemory(agent_id="cro")
    fs = MemoryFilesystem(role_id="cro", agent_memory=mem, soul="You are the CRO.")
    entries = fs.browse("/")
    assert "identity" in entries
    assert "knowledge" in entries
    assert "experience" in entries
    assert "references" in entries


def test_browse_identity():
    mem = AgentMemory(agent_id="cro")
    fs = MemoryFilesystem(role_id="cro", agent_memory=mem, soul="You are the CRO.")
    entries = fs.browse("/identity/")
    assert "soul.md" in entries


def test_browse_knowledge_lists_domains():
    mem = AgentMemory(agent_id="cro")
    mem.store_insight(Insight(
        id="ins1", agent_id="cro", content="Revenue insight",
        confidence=0.8, evidence_count=3, source_episode_ids=[],
        created_at=datetime.now(timezone.utc), domain="revenue",
    ))
    mem.store_insight(Insight(
        id="ins2", agent_id="cro", content="Marketing insight",
        confidence=0.7, evidence_count=2, source_episode_ids=[],
        created_at=datetime.now(timezone.utc), domain="marketing",
    ))
    fs = MemoryFilesystem(role_id="cro", agent_memory=mem)
    entries = fs.browse("/knowledge/")
    assert "revenue" in entries
    assert "marketing" in entries


def test_browse_knowledge_domain():
    mem = AgentMemory(agent_id="cro")
    mem.store_insight(Insight(
        id="ins1", agent_id="cro", content="VP sponsor predicts conversion",
        confidence=0.9, evidence_count=5, source_episode_ids=[],
        created_at=datetime.now(timezone.utc), domain="revenue",
        tags=["qualification"],
    ))
    fs = MemoryFilesystem(role_id="cro", agent_memory=mem)
    entries = fs.browse("/knowledge/revenue/")
    assert len(entries) >= 1


# --- Read ---

def test_read_identity_soul():
    mem = AgentMemory(agent_id="cro")
    fs = MemoryFilesystem(role_id="cro", agent_memory=mem, soul="You are the CRO.")
    content = fs.read("/identity/soul.md")
    assert content == "You are the CRO."


def test_read_knowledge_insight():
    mem = AgentMemory(agent_id="cro")
    mem.store_insight(Insight(
        id="ins1", agent_id="cro", content="VP sponsor predicts conversion",
        confidence=0.9, evidence_count=5, source_episode_ids=[],
        created_at=datetime.now(timezone.utc), domain="revenue",
    ))
    fs = MemoryFilesystem(role_id="cro", agent_memory=mem)
    content = fs.read("/knowledge/revenue/ins1")
    assert "VP sponsor predicts conversion" in content


def test_read_missing_returns_empty():
    mem = AgentMemory(agent_id="cro")
    fs = MemoryFilesystem(role_id="cro", agent_memory=mem)
    content = fs.read("/knowledge/nonexistent/nothing")
    assert content == ""


# --- Search ---

def test_search_scoped():
    mem = AgentMemory(agent_id="cro")
    mem.store_insight(Insight(
        id="ins1", agent_id="cro", content="VP sponsor predicts conversion",
        confidence=0.9, evidence_count=5, source_episode_ids=[],
        created_at=datetime.now(timezone.utc), domain="revenue",
    ))
    mem.store_insight(Insight(
        id="ins2", agent_id="cro", content="Brand voice matters",
        confidence=0.8, evidence_count=3, source_episode_ids=[],
        created_at=datetime.now(timezone.utc), domain="marketing",
    ))
    fs = MemoryFilesystem(role_id="cro", agent_memory=mem)
    results = fs.search("VP sponsor", scope="/knowledge/revenue/")
    assert len(results) == 1
    assert "VP sponsor" in results[0]["content"]


def test_search_global():
    mem = AgentMemory(agent_id="cro")
    mem.store_insight(Insight(
        id="ins1", agent_id="cro", content="VP sponsor predicts conversion",
        confidence=0.9, evidence_count=5, source_episode_ids=[],
        created_at=datetime.now(timezone.utc), domain="revenue",
    ))
    fs = MemoryFilesystem(role_id="cro", agent_memory=mem)
    results = fs.search("VP sponsor")
    assert len(results) >= 1


# --- Write ---

def test_write_knowledge():
    mem = AgentMemory(agent_id="cro")
    fs = MemoryFilesystem(role_id="cro", agent_memory=mem)
    fs.write("/knowledge/revenue/new-principle", "Enterprise deals need VP sponsor")
    results = mem.recall_insights(domain="revenue")
    assert len(results) == 1
    assert "VP sponsor" in results[0].content


def test_write_experience():
    mem = AgentMemory(agent_id="cro")
    fs = MemoryFilesystem(role_id="cro", agent_memory=mem)
    fs.write("/experience/2026-02/qualified-acme", "Qualified Acme Corp at 85")
    results = mem.recall_episodes()
    assert len(results) == 1


# --- Observable traces ---

def test_traces_recorded():
    mem = AgentMemory(agent_id="cro")
    fs = MemoryFilesystem(role_id="cro", agent_memory=mem, soul="CRO soul")
    fs.browse("/")
    fs.read("/identity/soul.md")
    fs.search("test")
    traces = fs.traces
    assert len(traces) == 3
    assert traces[0].action == "browse"
    assert traces[1].action == "read"
    assert traces[2].action == "search"


def test_clear_traces():
    mem = AgentMemory(agent_id="cro")
    fs = MemoryFilesystem(role_id="cro", agent_memory=mem)
    fs.browse("/")
    assert len(fs.traces) == 1
    fs.clear_traces()
    assert len(fs.traces) == 0
