from fastapi import APIRouter
from openvibe_platform.store import JSONFileStore
from openvibe_platform.workspace import WorkspaceService


def make_router(svc: WorkspaceService, store: JSONFileStore | None = None) -> APIRouter:
    router = APIRouter()

    @router.get("/workspaces")
    def list_workspaces() -> list:
        return []

    return router
