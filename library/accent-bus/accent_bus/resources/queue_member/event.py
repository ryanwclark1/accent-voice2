# accent_bus/resources/queue_member/event.py
# Copyright 2025 Accent Communications

"""Queue member events."""

from accent_bus.resources.common.event import TenantEvent, UserEvent
from accent_bus.resources.common.types import UUIDStr


class QueueMemberAgentAssociatedEvent(TenantEvent):
    """Event for when an agent is associated as a member of a queue."""

    service = "confd"
    name = "queue_member_agent_associated"
    routing_key_fmt = "config.queues.agents.updated"

    def __init__(
        self,
        queue_id: int,
        agent_id: int,
        penalty: int,
        tenant_uuid: UUIDStr,
    ) -> None:
        """Initialize event.

        Args:
            queue_id (int): The ID of the queue.
            agent_id (int): The ID of the agent.
            penalty (int):  agent's penalty.
            tenant_uuid (UUIDStr):  tenant UUID.

        """
        content = {
            "queue_id": queue_id,
            "agent_id": agent_id,
            "penalty": penalty,
        }
        super().__init__(content, tenant_uuid)


class QueueMemberAgentDissociatedEvent(TenantEvent):
    """Event for when an agent is dissociated as a member of a queue."""

    service = "confd"
    name = "queue_member_agent_dissociated"
    routing_key_fmt = "config.queues.agents.deleted"

    def __init__(
        self,
        queue_id: int,
        agent_id: int,
        tenant_uuid: UUIDStr,
    ) -> None:
        """Initialize the event.

        Args:
           queue_id: Queue ID
           agent_id: Agent ID
           tenant_uuid: tenant UUID

        """
        content = {
            "queue_id": queue_id,
            "agent_id": agent_id,
        }
        super().__init__(content, tenant_uuid)


class QueueMemberUserAssociatedEvent(UserEvent):
    """Event for when a user is associated as a member of a queue."""

    service = "confd"
    name = "queue_member_user_associated"
    routing_key_fmt = "config.queues.users.updated"

    def __init__(
        self,
        queue_id: int,
        tenant_uuid: UUIDStr,
        user_uuid: UUIDStr,
    ) -> None:
        """Initialize the event.

        Args:
          queue_id: Queue ID
          tenant_uuid: tenant UUID
          user_uuid: user UUID

        """
        content = {
            "queue_id": queue_id,
            "user_uuid": str(user_uuid),
        }
        super().__init__(content, tenant_uuid, user_uuid)


class QueueMemberUserDissociatedEvent(UserEvent):
    """Event for when a user is dissociated as a member of a queue."""

    service = "confd"
    name = "queue_member_user_dissociated"
    routing_key_fmt = "config.queues.users.deleted"

    def __init__(
        self,
        queue_id: int,
        tenant_uuid: UUIDStr,
        user_uuid: UUIDStr,
    ) -> None:
        """Initialize event.

        Args:
           queue_id: Queue ID
           tenant_uuid: tenant UUID
           user_uuid: user UUID

        """
        content = {
            "queue_id": queue_id,
            "user_uuid": str(user_uuid),
        }
        super().__init__(content, tenant_uuid, user_uuid)
