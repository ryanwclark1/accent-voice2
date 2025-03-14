# accent_bus/resources/skill_rule/event.py
# Copyright 2025 Accent Communications

"""Skill rule events."""

from accent_bus.resources.common.event import TenantEvent
from accent_bus.resources.common.types import UUIDStr


class SkillRuleCreatedEvent(TenantEvent):
    """Event for when a skill rule is created."""

    service = "confd"
    name = "skill_rule_created"
    routing_key_fmt = "config.queues.skillrules.created"

    def __init__(self, skill_rule_id: int, tenant_uuid: UUIDStr) -> None:
        """Initialize Event.

        Args:
            skill_rule_id (int):  skill rule ID.
            tenant_uuid (UUIDStr): tenant UUID.

        """
        content = {"id": int(skill_rule_id)}
        super().__init__(content, tenant_uuid)


class SkillRuleDeletedEvent(TenantEvent):
    """Event for when a skill rule is deleted."""

    service = "confd"
    name = "skill_rule_deleted"
    routing_key_fmt = "config.queues.skillrules.deleted"

    def __init__(self, skill_rule_id: int, tenant_uuid: UUIDStr) -> None:
        """Initialize event.

        Args:
           skill_rule_id: Skill Rule ID
           tenant_uuid: tenant UUID

        """
        content = {"id": int(skill_rule_id)}
        super().__init__(content, tenant_uuid)


class SkillRuleEditedEvent(TenantEvent):
    """Event for when a skill rule is edited."""

    service = "confd"
    name = "skill_rule_edited"
    routing_key_fmt = "config.queues.skillrules.edited"

    def __init__(self, skill_rule_id: int, tenant_uuid: UUIDStr) -> None:
        """Initialize Event.

        Args:
            skill_rule_id (int): skill rule ID.
            tenant_uuid (UUIDStr): The tenant UUID.

        """
        content = {"id": int(skill_rule_id)}
        super().__init__(content, tenant_uuid)
