from fastapi import APIRouter
from openvibe_platform.human_loop import HumanLoopService
from openvibe_platform.store import JSONFileStore


def make_router(svc: HumanLoopService, store: JSONFileStore | None = None) -> APIRouter:
    return APIRouter()
