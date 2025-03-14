# accent_bus/resources/agent_skill/event.py
# Copyright 2025 Accent Communications

"""Agent skill events."""

from accent_bus.resources.common.event import TenantEvent
from accent_bus.resources.common.types import UUIDStr


class AgentSkillAssociatedEvent(TenantEvent):
    """Event for when an agent skill is associated."""

    service = "confd"
    name = "agent_skill_associated"
    routing_key_fmt = "config.agents.skills.updated"

    def __init__(
        self,
        agent_id: int,
        skill_id: int,
        tenant_uuid: UUIDStr,
    ) -> None:
        """Initialize the event.

        Args:
            agent_id (int): The agent ID.
            skill_id (int): The skill ID.
            tenant_uuid (UUIDStr): tenant UUID

        """
        content = {
            "agent_id": agent_id,
            "skill_id": skill_id,
        }
        super().__init__(content, tenant_uuid)


class AgentSkillDissociatedEvent(TenantEvent):
    """Event for when an agent skill is dissociated."""

    service = "confd"
    name = "agent_skill_dissociated"
    routing_key_fmt = "config.agents.skills.deleted"

    def __init__(
        self,
        agent_id: int,
        skill_id: int,
        tenant_uuid: UUIDStr,
    ) -> None:
        """Initialize the event.

        Args:
           agent_id: Agent ID
           skill_id: Skill ID
           tenant_uuid: tenant UUID

        """
        content = {
            "agent_id": agent_id,
            "skill_id": skill_id,
        }
        super().__init__(content, tenant_uuid)
