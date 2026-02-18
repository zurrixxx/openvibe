from datetime import datetime, timezone
from openvibe_sdk.models import (
    Event, RoutingDecision, RoleMessage,
    WorkspaceConfig, WorkspacePolicy,
    RoleTemplate, RoleSpec,
    RoleLifecycle, RoleStatus,
    TrustProfile,
    Objective, KeyResult,
)


def test_event_creation():
    e = Event(
        id="e-1", type="lead.created", source="hubspot",
        domain="revenue", payload={"lead_id": "123"},
        timestamp=datetime.now(timezone.utc),
    )
    assert e.domain == "revenue"
    assert e.type == "lead.created"


def test_routing_decision_delegate():
    d = RoutingDecision(action="delegate", reason="matched operator",
                        operator_id="revenue_ops", trigger_id="qualify")
    assert d.action == "delegate"
    assert d.operator_id == "revenue_ops"


def test_routing_decision_escalate():
    d = RoutingDecision(action="escalate", reason="needs approval",
                        target_role_id="ceo", message="approve this deal")
    assert d.target_role_id == "ceo"


def test_role_message():
    m = RoleMessage(id="m-1", type="request", from_id="cro",
                    to_id="bdr-apac", content="qualify this lead")
    assert m.from_id == "cro"


def test_workspace_config():
    ws = WorkspaceConfig(id="vibe-team", name="Vibe AI Team", owner="charles",
                         policy=WorkspacePolicy())
    assert ws.policy.default_trust == 0.3
    assert ws.policy.spawn_requires_approval is False


def test_role_status_enum():
    assert RoleStatus.ACTIVE == "active"
    assert RoleStatus.TESTING == "testing"


def test_role_lifecycle():
    lc = RoleLifecycle(status=RoleStatus.ACTIVE,
                       created_at=datetime.now(timezone.utc),
                       created_by="charles")
    assert lc.status == RoleStatus.ACTIVE
    assert lc.memory_policy == "archive"


def test_trust_profile_default():
    t = TrustProfile()
    assert t.trust_for("qualify_lead") == 0.3  # default


def test_trust_profile_known_capability():
    t = TrustProfile(scores={"qualify_lead": 0.8})
    assert t.trust_for("qualify_lead") == 0.8


def test_objective_progress():
    kr = KeyResult(id="kr-1", description="100 leads", target=100, current=42, unit="leads")
    assert abs(kr.progress - 0.42) < 0.001


def test_objective_full_progress():
    kr = KeyResult(id="kr-2", description="done", target=10, current=15)
    assert kr.progress == 1.0  # capped at 1.0


def test_role_template():
    t = RoleTemplate(
        template_id="bdr",
        name_pattern="BDR - {territory}",
        soul_template="You are a BDR covering {territory}.",
        domains=["revenue"],
        authority=None,
        operator_ids=["revenue_ops"],
        parameters=["territory"],
        allowed_spawners=["cro"],
    )
    assert "territory" in t.parameters


def test_role_spec():
    from openvibe_sdk.models import AuthorityConfig
    spec = RoleSpec(
        role_id="bdr-apac", workspace="vibe-team",
        soul="You are a BDR covering APAC.",
        domains=["revenue"], reports_to="cro",
        operator_ids=["revenue_ops"],
        authority=AuthorityConfig(autonomous=["qualify_lead"]),
        parent_role_id="cro",
    )
    assert spec.parent_role_id == "cro"
