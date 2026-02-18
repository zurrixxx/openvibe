from fastapi import APIRouter
from openvibe_platform.store import JSONFileStore
from openvibe_sdk.registry import InMemoryRegistry


def make_router(registry: InMemoryRegistry, store: JSONFileStore | None = None) -> APIRouter:
    return APIRouter()
