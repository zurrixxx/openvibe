"""HTTP router for workspaces — legacy /api/v1 and tenant-scoped."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel

from openvibe_platform.store import JSONFileStore
from openvibe_platform.workspace import WorkspaceService
from openvibe_sdk.models import WorkspaceConfig, WorkspacePolicy


class _WorkspaceCreate(BaseModel):
    id: str
    name: str
    owner: str = ""


def make_router(svc: WorkspaceService, store: JSONFileStore | None = None) -> APIRouter:
    """Legacy router at /api/v1/workspaces (shared workspace service)."""
    router = APIRouter(tags=["workspaces"])

    def _save() -> None:
        if store:
            store.save("workspaces.json", [ws.model_dump() for ws in svc.list()])

    @router.get("/workspaces")
    def list_workspaces() -> list[dict]:
        return [ws.model_dump() for ws in svc.list()]

    @router.post("/workspaces", status_code=200)
    def create_workspace(body: _WorkspaceCreate) -> dict:
        try:
            svc.create(WorkspaceConfig(id=body.id, name=body.name, owner=body.owner, policy=WorkspacePolicy()))
        except ValueError:
            raise HTTPException(status_code=409, detail=f"Workspace '{body.id}' already exists")
        _save()
        return {"id": body.id}

    @router.delete("/workspaces/{workspace_id}", status_code=204)
    def delete_workspace(workspace_id: str) -> None:
        svc.delete(workspace_id)
        _save()

    return router


def make_tenant_router() -> APIRouter:
    """Tenant-scoped router at /tenants/{tenant_id}/workspaces."""
    router = APIRouter(tags=["tenant-workspaces"])

    def _get_svc(request: Request, tenant_id: str) -> WorkspaceService:
        svcs: dict[str, WorkspaceService] = request.app.state.tenant_workspace_svcs
        if tenant_id not in svcs:
            raise HTTPException(status_code=404, detail=f"Tenant not found: {tenant_id}")
        return svcs[tenant_id]

    @router.get("/tenants/{tenant_id}/workspaces")
    def list_tenant_workspaces(tenant_id: str, request: Request) -> list[dict]:
        svc = _get_svc(request, tenant_id)
        return [ws.model_dump() for ws in svc.list()]

    @router.post("/tenants/{tenant_id}/workspaces", status_code=200)
    def create_tenant_workspace(tenant_id: str, body: _WorkspaceCreate, request: Request) -> dict:
        svc = _get_svc(request, tenant_id)
        try:
            svc.create(WorkspaceConfig(id=body.id, name=body.name, owner=body.owner, policy=WorkspacePolicy()))
        except ValueError:
            raise HTTPException(status_code=409, detail=f"Workspace '{body.id}' already exists")
        return {"id": body.id}

    @router.delete("/tenants/{tenant_id}/workspaces/{workspace_id}", status_code=204)
    def delete_tenant_workspace(tenant_id: str, workspace_id: str, request: Request) -> None:
        svc = _get_svc(request, tenant_id)
        svc.delete(workspace_id)

    return router
