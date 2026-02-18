"""HTTP router for /tenants."""
from __future__ import annotations

from fastapi import APIRouter, HTTPException, Request

from openvibe_platform.tenant import TenantNotFound

router = APIRouter(prefix="/tenants", tags=["tenants"])


@router.get("")
def list_tenants(request: Request) -> list[dict]:
    return request.app.state.tenant_store.list()


@router.get("/{tenant_id}")
def get_tenant(tenant_id: str, request: Request) -> dict:
    try:
        return request.app.state.tenant_store.get(tenant_id)
    except TenantNotFound:
        raise HTTPException(status_code=404, detail=f"Tenant not found: {tenant_id}")
