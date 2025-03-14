# accent_bus/resources/user_agent/event.py
# Copyright 2025 Accent Communications

"""User agent events."""

from accent_bus.resources.common.event import UserEvent
from accent_bus.resources.common.types import UUIDStr


class UserAgentAssociatedEvent(UserEvent):
    """Event for when a user agent is associated."""

    service = "confd"
    name = "user_agent_associated"
    routing_key_fmt = "config.users.{user_uuid}.agents.updated"

    def __init__(
        self,
        agent_id: int,
        tenant_uuid: UUIDStr,
        user_uuid: UUIDStr,
    ) -> None:
        """Initialize Event.

        Args:
          agent_id: Agent ID
          tenant_uuid: tenant UUID
          user_uuid: user UUID

        """
        content = {
            "user_uuid": str(user_uuid),
            "agent_id": agent_id,
        }
        super().__init__(content, tenant_uuid, user_uuid)


class UserAgentDissociatedEvent(UserEvent):
    """Event for when a user agent is dissociated."""

    service = "confd"
    name = "user_agent_dissociated"
    routing_key_fmt = "config.users.{user_uuid}.agents.deleted"

    def __init__(
        self,
        agent_id: int,
        tenant_uuid: UUIDStr,
        user_uuid: UUIDStr,
    ) -> None:
        """Initialize the event.

        Args:
            agent_id (int):  agent ID.
            tenant_uuid (UUIDStr):  tenant UUID.
            user_uuid (UUIDStr):  user UUID.

        """
        content = {
            "user_uuid": str(user_uuid),
            "agent_id": agent_id,
        }
        super().__init__(content, tenant_uuid, user_uuid)
