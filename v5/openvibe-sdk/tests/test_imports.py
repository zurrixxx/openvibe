def test_package_importable():
    import openvibe_sdk
    assert openvibe_sdk.__doc__ is not None


def test_v3_exports():
    from openvibe_sdk import (
        Event, RoutingDecision, RoleMessage,
        WorkspaceConfig, WorkspacePolicy,
        RoleTemplate, RoleSpec,
        RoleLifecycle, RoleStatus,
        TrustProfile, Objective, KeyResult,
        InMemoryRegistry, InMemoryTransport, Participant,
    )


def test_version_is_1_0_0():
    import openvibe_sdk
    assert openvibe_sdk.__version__ == "1.0.0"
