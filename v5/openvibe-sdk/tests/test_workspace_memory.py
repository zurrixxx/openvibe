from openvibe_sdk.memory.access import ClearanceProfile
from openvibe_sdk.memory.types import Classification, Fact
from openvibe_sdk.memory.workspace import WorkspaceMemory


def test_store_and_query():
    ws = WorkspaceMemory()
    profile = ClearanceProfile(
        agent_id="cro",
        domain_clearance={"revenue": Classification.CONFIDENTIAL},
    )
    ws.store_fact(Fact(
        id="f1", content="Acme data", domain="revenue",
        classification=Classification.INTERNAL,
    ))
    results = ws.query(clearance=profile, domain="revenue")
    assert len(results) == 1
    assert results[0].content == "Acme data"


def test_query_filters_by_clearance():
    ws = WorkspaceMemory()
    ws.store_fact(Fact(
        id="f1", content="Public info", classification=Classification.PUBLIC,
    ))
    ws.store_fact(Fact(
        id="f2", content="Revenue secret", domain="revenue",
        classification=Classification.CONFIDENTIAL,
    ))
    # CMO has no revenue clearance
    cmo_profile = ClearanceProfile(
        agent_id="cmo",
        domain_clearance={"marketing": Classification.INTERNAL},
    )
    results = ws.query(clearance=cmo_profile)
    assert len(results) == 1
    assert results[0].id == "f1"  # only public


def test_query_by_entity():
    ws = WorkspaceMemory()
    profile = ClearanceProfile(agent_id="cro", domain_clearance={})
    ws.store_fact(Fact(id="f1", content="Acme info", entity="acme",
                       classification=Classification.PUBLIC))
    ws.store_fact(Fact(id="f2", content="Beta info", entity="beta",
                       classification=Classification.PUBLIC))
    results = ws.query(clearance=profile, entity="acme")
    assert len(results) == 1


def test_query_tracks_access():
    ws = WorkspaceMemory()
    profile = ClearanceProfile(agent_id="cro", domain_clearance={})
    ws.store_fact(Fact(id="f1", content="tracked", classification=Classification.PUBLIC))
    results = ws.query(clearance=profile)
    assert results[0].access_count == 1
    assert results[0].last_accessed is not None


def test_update_fact():
    ws = WorkspaceMemory()
    f = Fact(id="f1", content="Original", classification=Classification.PUBLIC)
    ws.store_fact(f)
    f.content = "Updated"
    ws.update_fact(f)
    profile = ClearanceProfile(agent_id="cro", domain_clearance={})
    results = ws.query(clearance=profile, query="Updated")
    assert len(results) == 1


def test_query_respects_limit():
    ws = WorkspaceMemory()
    profile = ClearanceProfile(agent_id="cro", domain_clearance={})
    for i in range(20):
        ws.store_fact(Fact(id=f"f{i}", content=f"fact {i}",
                           classification=Classification.PUBLIC))
    results = ws.query(clearance=profile, limit=5)
    assert len(results) == 5
