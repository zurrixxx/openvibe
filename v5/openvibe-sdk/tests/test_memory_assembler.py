from datetime import datetime, timezone

from openvibe_sdk.memory.access import ClearanceProfile
from openvibe_sdk.memory.agent_memory import AgentMemory
from openvibe_sdk.memory.assembler import MemoryAssembler
from openvibe_sdk.memory.types import Classification, Episode, Fact, Insight
from openvibe_sdk.memory.workspace import WorkspaceMemory


def test_assemble_insights():
    mem = AgentMemory(agent_id="cro")
    mem.store_insight(Insight(
        id="ins1", agent_id="cro", content="VP sponsor predicts conversion",
        confidence=0.9, evidence_count=5, source_episode_ids=[],
        created_at=datetime.now(timezone.utc), domain="revenue",
    ))
    profile = ClearanceProfile(agent_id="cro", domain_clearance={})
    assembler = MemoryAssembler(mem, profile)
    result = assembler.assemble({"domain": "revenue"})
    assert "VP sponsor" in result
    assert "Insights" in result


def test_assemble_workspace_facts():
    ws = WorkspaceMemory()
    ws.store_fact(Fact(
        id="f1", content="Acme has 200 employees",
        entity="acme", domain="customer",
        classification=Classification.PUBLIC,
    ))
    mem = AgentMemory(agent_id="cro", workspace=ws)
    profile = ClearanceProfile(agent_id="cro", domain_clearance={})
    assembler = MemoryAssembler(mem, profile)
    result = assembler.assemble({"entity": "acme"})
    assert "200 employees" in result


def test_assemble_recent_episodes():
    mem = AgentMemory(agent_id="cro")
    mem.record_episode(Episode(
        id="ep1", agent_id="cro", operator_id="test", node_name="qualify",
        timestamp=datetime.now(timezone.utc), action="qualify_lead",
        input_summary="Score Acme", output_summary="Score: 85",
        outcome={}, duration_ms=100, tokens_in=10, tokens_out=20,
    ))
    profile = ClearanceProfile(agent_id="cro", domain_clearance={})
    assembler = MemoryAssembler(mem, profile)
    result = assembler.assemble({})
    assert "Recent Activity" in result
    assert "qualify_lead" in result


def test_assemble_priority_order():
    """Insights come before facts come before episodes."""
    ws = WorkspaceMemory()
    ws.store_fact(Fact(
        id="f1", content="Fact content",
        classification=Classification.PUBLIC,
    ))
    mem = AgentMemory(agent_id="cro", workspace=ws)
    mem.store_insight(Insight(
        id="ins1", agent_id="cro", content="Insight content",
        confidence=0.9, evidence_count=5, source_episode_ids=[],
        created_at=datetime.now(timezone.utc),
    ))
    mem.record_episode(Episode(
        id="ep1", agent_id="cro", operator_id="test", node_name="test",
        timestamp=datetime.now(timezone.utc), action="test",
        input_summary="in", output_summary="Episode content",
        outcome={}, duration_ms=100, tokens_in=10, tokens_out=20,
    ))
    profile = ClearanceProfile(agent_id="cro", domain_clearance={})
    assembler = MemoryAssembler(mem, profile)
    result = assembler.assemble({})
    # Insights section should come first
    ins_pos = result.index("Insights")
    ctx_pos = result.index("Context")
    act_pos = result.index("Recent Activity")
    assert ins_pos < ctx_pos < act_pos


def test_assemble_token_budget():
    mem = AgentMemory(agent_id="cro")
    for i in range(50):
        mem.store_insight(Insight(
            id=f"ins{i}", agent_id="cro",
            content=f"A very long insight number {i} " * 20,
            confidence=0.9, evidence_count=5, source_episode_ids=[],
            created_at=datetime.now(timezone.utc),
        ))
    profile = ClearanceProfile(agent_id="cro", domain_clearance={})
    assembler = MemoryAssembler(mem, profile)
    result = assembler.assemble({}, token_budget=100)
    assert len(result) <= 100 * 4  # 4 chars per token


def test_assemble_empty():
    mem = AgentMemory(agent_id="cro")
    profile = ClearanceProfile(agent_id="cro", domain_clearance={})
    assembler = MemoryAssembler(mem, profile)
    result = assembler.assemble({})
    assert result == ""
