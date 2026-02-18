"""RoleRegistry and RoleTransport protocols + in-memory implementations."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Protocol, runtime_checkable

from openvibe_sdk.models import RoleMessage, RoleSpec


@dataclass
class Participant:
    """A role or human that can be found in the registry."""
    id: str
    type: str = "role"          # "role" | "human"
    name: str = ""
    domains: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)


@runtime_checkable
class RoleRegistry(Protocol):
    def get(self, workspace: str, role_id: str) -> Participant | None: ...
    def list_roles(self, workspace: str) -> list[Participant]: ...
    def find_by_domain(self, workspace: str, domain: str) -> list[Participant]: ...
    def register_participant(self, participant: Participant, workspace: str = "") -> None: ...
    def remove(self, workspace: str, role_id: str) -> None: ...


@runtime_checkable
class RoleTransport(Protocol):
    def send(self, from_id: str, to_id: str, message: RoleMessage) -> None: ...
    def inbox(self, role_id: str) -> list[RoleMessage]: ...


class InMemoryRegistry:
    """Dict-backed registry for tests and single-process deployments."""

    def __init__(self) -> None:
        # workspace -> role_id -> Participant
        self._store: dict[str, dict[str, Participant]] = {}

    def get(self, workspace: str, role_id: str) -> Participant | None:
        return self._store.get(workspace, {}).get(role_id)

    def list_roles(self, workspace: str) -> list[Participant]:
        return list(self._store.get(workspace, {}).values())

    def find_by_domain(self, workspace: str, domain: str) -> list[Participant]:
        return [
            p for p in self._store.get(workspace, {}).values()
            if domain in p.domains
        ]

    def register_participant(self, participant: Participant, workspace: str = "") -> None:
        if workspace not in self._store:
            self._store[workspace] = {}
        self._store[workspace][participant.id] = participant

    def remove(self, workspace: str, role_id: str) -> None:
        self._store.get(workspace, {}).pop(role_id, None)


class InMemoryTransport:
    """In-process message transport for tests."""

    def __init__(self) -> None:
        self._inboxes: dict[str, list[RoleMessage]] = {}

    def send(self, from_id: str, to_id: str, message: RoleMessage) -> None:
        if to_id not in self._inboxes:
            self._inboxes[to_id] = []
        self._inboxes[to_id].append(message)

    def inbox(self, role_id: str) -> list[RoleMessage]:
        return self._inboxes.get(role_id, [])
