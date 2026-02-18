from datetime import datetime, timezone
from openvibe_sdk.role import Role
from openvibe_sdk.models import (
    AuthorityConfig, RoleTemplate, RoleSpec, TrustProfile
)
from openvibe_sdk.registry import InMemoryRegistry, Participant


class CRORole(Role):
    role_id = "cro"
    soul = "You are CRO."
    workspace = "vibe-team"
    domains = ["revenue"]
    reports_to = "charles"
    authority = AuthorityConfig(autonomous=["qualify_lead"])


BDR_TEMPLATE = RoleTemplate(
    template_id="bdr",
    name_pattern="bdr-{territory}",
    soul_template="You are a BDR covering {territory}.",
    domains=["revenue"],
    authority=AuthorityConfig(autonomous=["qualify_lead"]),
    operator_ids=["revenue_ops"],
    parameters=["territory"],
    allowed_spawners=["cro"],
)


def test_spawn_creates_role_spec_and_registers():
    registry = InMemoryRegistry()
    cro = CRORole()
    cro._registry = registry

    new_id = cro.spawn(BDR_TEMPLATE, params={"territory": "APAC"})
    assert new_id == "bdr-apac"

    registered = registry.get("vibe-team", "bdr-apac")
    assert registered is not None
    assert registered.id == "bdr-apac"


def test_spawn_fills_soul_template():
    registry = InMemoryRegistry()
    cro = CRORole()
    cro._registry = registry

    new_id = cro.spawn(BDR_TEMPLATE, params={"territory": "EMEA"})
    spec = cro._last_spawned_spec
    assert "EMEA" in spec.soul


def test_spawn_permission_check():
    registry = InMemoryRegistry()

    class CMORole(Role):
        role_id = "cmo"
        workspace = "vibe-team"
        domains = ["marketing"]

    cmo = CMORole()
    cmo._registry = registry

    import pytest
    with pytest.raises(PermissionError):
        cmo.spawn(BDR_TEMPLATE, params={"territory": "APAC"})


def test_spawn_sets_parent():
    registry = InMemoryRegistry()
    cro = CRORole()
    cro._registry = registry

    cro.spawn(BDR_TEMPLATE, params={"territory": "SEA"})
    spec = cro._last_spawned_spec
    assert spec.parent_role_id == "cro"
    assert spec.reports_to == "cro"
