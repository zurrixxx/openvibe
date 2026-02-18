from openvibe_sdk.registry import (
    Participant, InMemoryRegistry, InMemoryTransport,
)
from openvibe_sdk.models import RoleMessage
from datetime import datetime, timezone


def test_registry_register_and_get():
    reg = InMemoryRegistry()
    p = Participant(id="cro", type="role", name="CRO", domains=["revenue"])
    reg.register_participant(p)
    found = reg.get("vibe-team", "cro")
    assert found is None  # not in workspace yet

    reg.register_participant(p, workspace="vibe-team")
    found = reg.get("vibe-team", "cro")
    assert found is not None
    assert found.id == "cro"


def test_registry_find_by_domain():
    reg = InMemoryRegistry()
    p = Participant(id="cro", type="role", domains=["revenue", "pipeline"])
    reg.register_participant(p, workspace="vibe-team")
    results = reg.find_by_domain("vibe-team", "revenue")
    assert len(results) == 1
    assert results[0].id == "cro"


def test_registry_find_by_domain_no_match():
    reg = InMemoryRegistry()
    results = reg.find_by_domain("vibe-team", "marketing")
    assert results == []


def test_registry_list_roles():
    reg = InMemoryRegistry()
    reg.register_participant(Participant(id="cro", type="role"), workspace="ws")
    reg.register_participant(Participant(id="cmo", type="role"), workspace="ws")
    roles = reg.list_roles("ws")
    assert len(roles) == 2


def test_registry_remove():
    reg = InMemoryRegistry()
    reg.register_participant(Participant(id="cro", type="role"), workspace="ws")
    reg.remove("ws", "cro")
    assert reg.get("ws", "cro") is None


def test_transport_send_and_receive():
    transport = InMemoryTransport()
    msg = RoleMessage(id="m-1", type="request", from_id="cro",
                      to_id="bdr", content="qualify this lead",
                      timestamp=datetime.now(timezone.utc))
    transport.send("cro", "bdr", msg)
    inbox = transport.inbox("bdr")
    assert len(inbox) == 1
    assert inbox[0].content == "qualify this lead"


def test_transport_inbox_empty_for_unknown():
    transport = InMemoryTransport()
    assert transport.inbox("nobody") == []
