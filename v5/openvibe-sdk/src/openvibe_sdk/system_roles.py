"""System roles — built-in roles present in every workspace."""
from __future__ import annotations

from openvibe_sdk.models import RoleInstance

Coordinator = RoleInstance(
    name="Coordinator",
    template_id="system/coordinator",
    soul={"identity": {
        "name": "Coordinator",
        "role": "Routes tasks, manages approvals, handles escalation",
    }},
    capabilities=[],
)

Archivist = RoleInstance(
    name="Archivist",
    template_id="system/archivist",
    soul={"identity": {
        "name": "Archivist",
        "role": "Manages memory, knowledge base, episodic retention",
    }},
    capabilities=[],
)

Auditor = RoleInstance(
    name="Auditor",
    template_id="system/auditor",
    soul={"identity": {
        "name": "Auditor",
        "role": "Tracks deliverables, metrics, feedback loop",
    }},
    capabilities=[],
)

SYSTEM_ROLES: list[RoleInstance] = [Coordinator, Archivist, Auditor]
