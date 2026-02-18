"""Tests for Role SDK completeness — respond, memory_fs, reflect, list_operators."""

from datetime import datetime, timezone

from openvibe_sdk.llm import LLMResponse
from openvibe_sdk.memory.access import ClearanceProfile
from openvibe_sdk.memory.agent_memory import AgentMemory
from openvibe_sdk.memory.filesystem import MemoryFilesystem
from openvibe_sdk.memory.types import Classification, Episode, Insight
from openvibe_sdk.models import AuthorityConfig
from openvibe_sdk.operator import Operator, llm_node
from openvibe_sdk.role import Role
from openvibe_sdk.runtime import RoleRuntime


class FakeLLM:
    def __init__(self, content="output"):
        self.content = content
        self.last_system = None
        self.last_messages = None

    def call(self, *, system, messages, **kwargs):
        self.last_system = system
        self.last_messages = messages
        return LLMResponse(content=self.content, tokens_in=10, tokens_out=20)


class RevenueOps(Operator):
    operator_id = "revenue_ops"

    @llm_node(model="sonnet", output_key="score")
    def qualify(self, state):
        """You are a lead qualifier."""
        return f"Score: {state.get('lead', '')}"


class CRO(Role):
    role_id = "cro"
    soul = "You are the CRO. Data-driven, aggressive but measured."
    operators = [RevenueOps]
    authority = AuthorityConfig(
        autonomous=["qualify_lead"],
        needs_approval=["change_pricing"],
        forbidden=["sign_contracts"],
    )
    clearance = ClearanceProfile(
        agent_id="cro",
        domain_clearance={"sales": Classification.CONFIDENTIAL},
    )


class MinimalRole(Role):
    role_id = "minimal"
    soul = "You are a test agent."
    operators = []


# --- respond() ---

def test_respond_basic():
    llm = FakeLLM(content="Pipeline looks strong at $2M.")
    agent_mem = AgentMemory(agent_id="cro")
    role = CRO(llm=llm, agent_memory=agent_mem)
    response = role.respond("How's the pipeline?")
    assert response.content == "Pipeline looks strong at $2M."
    assert llm.last_system is not None
    assert "CRO" in llm.last_system  # soul injected
    assert llm.last_messages[0]["content"] == "How's the pipeline?"


def test_respond_includes_soul():
    llm = FakeLLM()
    role = MinimalRole(llm=llm)
    role.respond("hello")
    assert "test agent" in llm.last_system


def test_respond_records_episode():
    llm = FakeLLM(content="Pipeline is $2M.")
    agent_mem = AgentMemory(agent_id="cro")
    role = CRO(llm=llm, agent_memory=agent_mem)
    role.respond("How's the pipeline?")
    episodes = agent_mem.recall_episodes()
    assert len(episodes) == 1
    assert episodes[0].action == "respond"
    assert "pipeline" in episodes[0].input_summary.lower()


def test_respond_includes_memory_context():
    llm = FakeLLM(content="Yes, VP sponsors help.")
    agent_mem = AgentMemory(agent_id="cro")
    agent_mem.store_insight(Insight(
        id="ins1", agent_id="cro",
        content="VP sponsor predicts conversion",
        confidence=0.9, evidence_count=5, source_episode_ids=[],
        created_at=datetime.now(timezone.utc), domain="sales",
    ))
    role = CRO(llm=llm, agent_memory=agent_mem)
    role.respond("VP sponsor")
    # Memory should appear in system prompt
    assert "VP sponsor" in llm.last_system


def test_respond_no_llm_raises():
    role = MinimalRole(llm=None)
    try:
        role.respond("hello")
        assert False, "Should have raised"
    except ValueError as e:
        assert "LLM" in str(e)


# --- memory_fs ---

def test_memory_fs_returns_filesystem():
    agent_mem = AgentMemory(agent_id="cro")
    role = CRO(llm=FakeLLM(), agent_memory=agent_mem)
    fs = role.memory_fs
    assert isinstance(fs, MemoryFilesystem)


def test_memory_fs_is_cached():
    agent_mem = AgentMemory(agent_id="cro")
    role = CRO(llm=FakeLLM(), agent_memory=agent_mem)
    fs1 = role.memory_fs
    fs2 = role.memory_fs
    assert fs1 is fs2


def test_memory_fs_has_soul():
    agent_mem = AgentMemory(agent_id="cro")
    role = CRO(llm=FakeLLM(), agent_memory=agent_mem)
    content = role.memory_fs.read("/identity/soul.md")
    assert "CRO" in content


def test_memory_fs_none_without_agent_memory():
    role = MinimalRole(llm=FakeLLM())
    assert role.memory_fs is None


# --- reflect() ---

def test_reflect_compresses_episodes():
    llm = FakeLLM(content='[{"content": "Leads from webinars convert 2x", "confidence": 0.8}]')
    agent_mem = AgentMemory(agent_id="cro")
    # Add some episodes to reflect on
    for i in range(3):
        agent_mem.record_episode(Episode(
            id=f"ep{i}", agent_id="cro", operator_id="revenue_ops",
            node_name="qualify", timestamp=datetime.now(timezone.utc),
            action="qualify_lead", input_summary=f"Lead {i}",
            output_summary=f"Score: {80 + i}", outcome={"score": 80 + i},
            duration_ms=100, tokens_in=10, tokens_out=20,
        ))
    role = CRO(llm=llm, agent_memory=agent_mem)
    new_insights = role.reflect()
    assert len(new_insights) >= 1
    assert "webinar" in new_insights[0].content.lower()


def test_reflect_no_agent_memory_returns_empty():
    role = MinimalRole(llm=FakeLLM())
    assert role.reflect() == []


# --- list_operators() ---

def test_list_operators():
    role = CRO(llm=FakeLLM())
    ops = role.list_operators()
    assert ops == ["revenue_ops"]


def test_list_operators_empty():
    role = MinimalRole(llm=FakeLLM())
    assert role.list_operators() == []


# --- RoleRuntime always creates AgentMemory ---

def test_runtime_always_creates_agent_memory():
    """RoleRuntime should create AgentMemory for all roles, not just those with clearance."""
    runtime = RoleRuntime(roles=[MinimalRole], llm=FakeLLM())
    role = runtime.get_role("minimal")
    assert role.agent_memory is not None


def test_runtime_role_has_memory_fs():
    """Roles from RoleRuntime should have working memory_fs."""
    runtime = RoleRuntime(roles=[MinimalRole], llm=FakeLLM())
    role = runtime.get_role("minimal")
    fs = role.memory_fs
    assert fs is not None
    entries = fs.browse("/")
    assert "identity" in entries
