from fastapi import APIRouter
from openvibe_platform.human_loop import HumanLoopService
from openvibe_platform.store import JSONFileStore


def make_router(svc: HumanLoopService, store: JSONFileStore | None = None) -> APIRouter:
    router = APIRouter()

    @router.get("/deliverables")
    def list_deliverables() -> list:
        return []

    return router
