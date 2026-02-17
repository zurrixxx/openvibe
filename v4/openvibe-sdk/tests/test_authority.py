from openvibe_sdk.models import AuthorityConfig


def test_autonomous_action():
    auth = AuthorityConfig(
        autonomous=["qualify_lead", "trigger_nurture"],
        needs_approval=["change_pricing"],
        forbidden=["sign_contracts"],
    )
    assert auth.can_act("qualify_lead") == "autonomous"


def test_needs_approval_action():
    auth = AuthorityConfig(
        autonomous=["qualify_lead"],
        needs_approval=["change_pricing"],
        forbidden=[],
    )
    assert auth.can_act("change_pricing") == "needs_approval"


def test_forbidden_action():
    auth = AuthorityConfig(
        autonomous=[],
        needs_approval=[],
        forbidden=["sign_contracts"],
    )
    assert auth.can_act("sign_contracts") == "forbidden"


def test_unknown_defaults_to_needs_approval():
    auth = AuthorityConfig(autonomous=["qualify_lead"])
    assert auth.can_act("unknown_action") == "needs_approval"


def test_forbidden_takes_priority():
    auth = AuthorityConfig(
        autonomous=["do_thing"],
        forbidden=["do_thing"],
    )
    assert auth.can_act("do_thing") == "forbidden"
