from openvibe_sdk.system_roles import SYSTEM_ROLES, Coordinator, Archivist, Auditor
from openvibe_sdk.models import RoleInstance


def test_system_roles_are_role_instances():
    for role in SYSTEM_ROLES:
        assert isinstance(role, RoleInstance)


def test_system_role_names():
    names = {r.name for r in SYSTEM_ROLES}
    assert names == {"Coordinator", "Archivist", "Auditor"}


def test_coordinator_purpose():
    assert Coordinator.name == "Coordinator"


def test_archivist_purpose():
    assert Archivist.name == "Archivist"


def test_auditor_purpose():
    assert Auditor.name == "Auditor"
