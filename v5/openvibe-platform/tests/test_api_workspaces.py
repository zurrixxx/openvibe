"""Tests for workspace endpoints (legacy /api/v1 and tenant-scoped)."""


def test_list_empty(client):
    r = client.get("/api/v1/workspaces")
    assert r.status_code == 200
    assert r.json() == []


def test_create_and_list(client):
    r = client.post("/api/v1/workspaces", json={"id": "ws1", "name": "WS One", "owner": "alice"})
    assert r.status_code == 200
    assert r.json()["id"] == "ws1"
    items = client.get("/api/v1/workspaces").json()
    assert any(w["id"] == "ws1" for w in items)


def test_create_duplicate_returns_409(client):
    client.post("/api/v1/workspaces", json={"id": "ws1", "name": "WS One", "owner": "alice"})
    r = client.post("/api/v1/workspaces", json={"id": "ws1", "name": "WS One", "owner": "alice"})
    assert r.status_code == 409


def test_delete(client):
    client.post("/api/v1/workspaces", json={"id": "ws1", "name": "WS One", "owner": "alice"})
    r = client.delete("/api/v1/workspaces/ws1")
    assert r.status_code == 204
    items = client.get("/api/v1/workspaces").json()
    assert not any(w["id"] == "ws1" for w in items)


# Tenant-scoped workspace tests

def test_tenant_workspace_create_and_list(client):
    r = client.post("/tenants/vibe-inc/workspaces", json={"id": "gtm", "name": "GTM"})
    assert r.status_code == 200
    resp = client.get("/tenants/vibe-inc/workspaces")
    assert resp.status_code == 200
    names = [w["name"] for w in resp.json()]
    assert "GTM" in names


def test_tenant_workspace_isolation(client):
    client.post("/tenants/vibe-inc/workspaces", json={"id": "marketing", "name": "Marketing"})
    resp = client.get("/tenants/astrocrest/workspaces")
    assert resp.status_code == 200
    names = [w["name"] for w in resp.json()]
    assert "Marketing" not in names
