"""Real API end-to-end test — validates the full Role SDK against live Claude.

Exercises the complete CRO lifecycle with real Anthropic API calls:
  respond() → operator @llm_node → episode recording → reflect() → memory recall

Skipped automatically if ANTHROPIC_API_KEY is not set.
Uses haiku for all calls (~$0.01 total).
"""

import os
from datetime import datetime, timezone

import pytest

from openvibe_sdk import (
    AgentMemory,
    AuthorityConfig,
    Classification,
    ClearanceProfile,
    Episode,
    Operator,
    Role,
    RoleRuntime,
    llm_node,
)
from openvibe_sdk.llm.anthropic import AnthropicProvider

pytestmark = pytest.mark.skipif(
    not os.getenv("ANTHROPIC_API_KEY"),
    reason="ANTHROPIC_API_KEY not set",
)


# --- Operator ---

class RevenueOps(Operator):
    operator_id = "revenue_ops"

    @llm_node(model="haiku", output_key="qualification")
    def qualify_lead(self, state):
        """You are a lead qualification expert.
        Score the lead 0-100 based on company size, revenue, and fit.
        Return ONLY a number followed by a brief explanation.
        Example: 85 — Strong fit, VP sponsor, $500K ACV potential."""
        return f"Company: {state.get('company', '?')}, Revenue: {state.get('revenue', '?')}"


# --- Role ---

CRO_SOUL = (
    "You are the CRO of Vibe. Data-driven, aggressive but measured.\n"
    "You care about pipeline velocity, CAC payback, and net revenue retention.\n"
    "Keep responses concise — 1-3 sentences max."
)


class CRO(Role):
    role_id = "cro"
    soul = CRO_SOUL
    operators = [RevenueOps]
    authority = AuthorityConfig(
        autonomous=["qualify_lead", "review_pipeline"],
        needs_approval=["change_pricing"],
        forbidden=["sign_contracts"],
    )
    clearance = ClearanceProfile(
        agent_id="cro",
        domain_clearance={
            "sales": Classification.CONFIDENTIAL,
            "finance": Classification.INTERNAL,
        },
    )


# === Test ===


def test_full_lifecycle_real_api():
    """Full chain: respond → qualify → episodes → reflect → recall.

    ~5 real API calls to Claude haiku. Assertions are behavioral
    (non-empty, correct types, correct counts) — never match exact content.
    """
    llm = AnthropicProvider()
    mem = AgentMemory(agent_id="cro")
    cro = CRO(llm=llm, agent_memory=mem)

    # --- Step 1: respond() with soul injection ---
    r1 = cro.respond("Give me a quick pipeline update.")

    assert isinstance(r1.content, str)
    assert len(r1.content) > 0, "respond() returned empty content"
    assert r1.tokens_in > 0
    assert r1.tokens_out > 0

    # --- Step 2: Operator @llm_node — qualify a lead ---
    op = cro.get_operator("revenue_ops")
    result = op.qualify_lead({"company": "Acme Corp", "revenue": "$50M ARR"})

    assert "qualification" in result, "output_key not written to state"
    assert isinstance(result["qualification"], str)
    assert len(result["qualification"]) > 0

    # --- Step 3: Verify episodes recorded ---
    episodes = mem.recall_episodes()
    assert len(episodes) == 2, f"Expected 2 episodes (respond + qualify), got {len(episodes)}"

    actions = {ep.action for ep in episodes}
    assert "respond" in actions
    assert "qualify_lead" in actions

    # Verify episode has token counts from real API
    for ep in episodes:
        assert ep.tokens_in > 0, f"Episode {ep.action} has no tokens_in"
        assert ep.tokens_out > 0, f"Episode {ep.action} has no tokens_out"

    # --- Step 4: reflect() — compress episodes into insights ---
    # reflect() uses model="sonnet" internally, calls LLM expecting JSON array
    insights = cro.reflect()

    # Real model with only 2 episodes may return 0 insights — that's fine.
    # But if it returns any, they must be valid Insight objects.
    assert isinstance(insights, list)
    for insight in insights:
        assert hasattr(insight, "content")
        assert hasattr(insight, "confidence")
        assert isinstance(insight.content, str)
        assert len(insight.content) > 0

    # --- Step 5: Second respond() — should have insights in context (if any) ---
    r2 = cro.respond("What patterns have you noticed about our leads?")

    assert isinstance(r2.content, str)
    assert len(r2.content) > 0

    # After step 4, we should have 3 episodes total (2 original + 1 from step 5 respond)
    all_episodes = mem.recall_episodes()
    assert len(all_episodes) == 3

    # --- Step 6: memory_fs still works (no API call) ---
    fs = cro.memory_fs
    assert fs is not None

    entries = fs.browse("/")
    assert "identity" in entries
    assert "knowledge" in entries
    assert "experience" in entries

    soul_content = fs.read("/identity/soul.md")
    assert "CRO" in soul_content

    # --- Summary ---
    print(f"\n--- Real API E2E Results ---")
    print(f"respond() #1: {r1.tokens_in}in/{r1.tokens_out}out tokens")
    print(f"qualify_lead: {result['qualification'][:80]}...")
    print(f"Episodes recorded: {len(all_episodes)}")
    print(f"Insights from reflect(): {len(insights)}")
    if insights:
        for i, ins in enumerate(insights):
            print(f"  [{i}] ({ins.confidence:.2f}) {ins.content[:80]}")
    print(f"respond() #2: {r2.tokens_in}in/{r2.tokens_out}out tokens")
    print(f"memory_fs browse(/): {entries}")


def test_reflect_with_seeded_episodes():
    """Seed 8 episodes with a clear pattern, verify reflect() extracts insights
    and the next respond() recalls them.

    Pattern: webinar leads consistently score 80+, cold outbound scores 30-40.
    Claude should detect this contrast.
    """
    llm = AnthropicProvider()
    mem = AgentMemory(agent_id="cro")
    now = datetime.now(timezone.utc)

    # Seed episodes — clear pattern: webinar > cold outbound
    webinar_leads = [
        ("TechCo", "webinar", 88, "Strong — VP attended demo, asked about enterprise plan"),
        ("DataInc", "webinar", 82, "Good — CTO engaged, 200-person eng team, budget approved"),
        ("CloudNow", "webinar", 91, "Excellent — CEO attended, $100M ARR, active eval"),
        ("AIFirst", "webinar", 85, "Strong — Head of Product, pain point match, Q2 budget"),
    ]
    cold_leads = [
        ("SmallBiz", "cold_outbound", 32, "Weak — no budget, small team, no urgency"),
        ("OldCorp", "cold_outbound", 28, "Poor — legacy stack, no champion, long procurement"),
        ("StartupX", "cold_outbound", 38, "Marginal — interested but pre-revenue, no budget"),
        ("MidTier", "cold_outbound", 35, "Weak — junior contact, unclear decision process"),
    ]

    for i, (company, source, score, summary) in enumerate(webinar_leads + cold_leads):
        mem.record_episode(Episode(
            id=f"ep-seed-{i}",
            agent_id="cro",
            operator_id="revenue_ops",
            node_name="qualify_lead",
            timestamp=now,
            action="qualify_lead",
            input_summary=f"{company} (source: {source})",
            output_summary=f"Score: {score} — {summary}",
            outcome={"score": score, "source": source},
            duration_ms=200,
            tokens_in=50,
            tokens_out=80,
            domain="sales",
        ))

    assert len(mem.recall_episodes(limit=50)) == 8

    # --- reflect() should now find patterns ---
    cro = CRO(llm=llm, agent_memory=mem)
    insights = cro.reflect()

    print(f"\n--- Reflect with seeded episodes ---")
    print(f"Episodes seeded: 8 (4 webinar high-score, 4 cold low-score)")
    print(f"Insights produced: {len(insights)}")
    for i, ins in enumerate(insights):
        print(f"  [{i}] ({ins.confidence:.2f}) {ins.content[:100]}")

    assert len(insights) >= 1, "reflect() should extract at least 1 insight from 8 episodes"
    assert all(isinstance(ins.content, str) and len(ins.content) > 0 for ins in insights)
    assert all(0.0 <= ins.confidence <= 1.0 for ins in insights)

    # --- Insights should be stored in memory ---
    stored = mem.recall_insights(domain="sales")
    assert len(stored) >= 1, "Insights not stored in agent memory"

    # --- Insights should appear in memory_fs ---
    fs = cro.memory_fs
    knowledge_entries = fs.browse("/knowledge")
    print(f"memory_fs /knowledge domains: {knowledge_entries}")

    # --- respond() should recall insights ---
    r = cro.respond("Which lead sources are working best?")

    assert isinstance(r.content, str)
    assert len(r.content) > 0
    print(f"respond() with insights: {r.content[:200]}")
    print(f"  tokens: {r.tokens_in}in/{r.tokens_out}out")
