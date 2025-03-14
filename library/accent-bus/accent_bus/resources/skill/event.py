# accent_bus/resources/skill/event.py
# Copyright 2025 Accent Communications

"""Skill events."""

from accent_bus.resources.common.event import TenantEvent
from accent_bus.resources.common.types import UUIDStr


class SkillCreatedEvent(TenantEvent):
    """Event for when a skill is created."""

    service = "confd"
    name = "skill_created"
    routing_key_fmt = "config.agents.skills.created"

    def __init__(self, skill_id: int, tenant_uuid: UUIDStr) -> None:
        """Initialize the event.

        Args:
           skill_id: Skill ID
           tenant_uuid: tenant UUID

        """
        content = {"id": int(skill_id)}
        super().__init__(content, tenant_uuid)


class SkillDeletedEvent(TenantEvent):
    """Event for when a skill is deleted."""

    service = "confd"
    name = "skill_deleted"
    routing_key_fmt = "config.agents.skills.deleted"

    def __init__(self, skill_id: int, tenant_uuid: UUIDStr) -> None:
        """Initialize Event.

        Args:
          skill_id: Skill ID
          tenant_uuid: tenant UUID

        """
        content = {"id": int(skill_id)}
        super().__init__(content, tenant_uuid)


class SkillEditedEvent(TenantEvent):
    """Event for when a skill is edited."""

    service = "confd"
    name = "skill_edited"
    routing_key_fmt = "config.agents.skills.edited"

    def __init__(self, skill_id: int, tenant_uuid: UUIDStr) -> None:
        """Initialize event.

        Args:
           skill_id: Skill ID
           tenant_uuid: tenant UUID

        """
        content = {"id": int(skill_id)}
        super().__init__(content, tenant_uuid)
