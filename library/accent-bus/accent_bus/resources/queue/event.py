# accent_bus/resources/queue/event.py
# Copyright 2025 Accent Communications

"""Queue events."""

from accent_bus.resources.common.event import TenantEvent
from accent_bus.resources.common.types import UUIDStr


class QueueCreatedEvent(TenantEvent):
    """Event for when a queue is created."""

    service = "confd"
    name = "queue_created"
    routing_key_fmt = "config.queues.created"

    def __init__(self, queue_id: int, tenant_uuid: UUIDStr) -> None:
        """Initialize Event.

        Args:
           queue_id: Queue ID
           tenant_uuid: tenant UUID

        """
        content = {"id": int(queue_id)}
        super().__init__(content, tenant_uuid)


class QueueDeletedEvent(TenantEvent):
    """Event for when a queue is deleted."""

    service = "confd"
    name = "queue_deleted"
    routing_key_fmt = "config.queues.deleted"

    def __init__(self, queue_id: int, tenant_uuid: UUIDStr) -> None:
        """Initialize event.

        Args:
           queue_id: Queue ID
           tenant_uuid: tenant UUID

        """
        content = {"id": int(queue_id)}
        super().__init__(content, tenant_uuid)


class QueueEditedEvent(TenantEvent):
    """Event for when a queue is edited."""

    service = "confd"
    name = "queue_edited"
    routing_key_fmt = "config.queues.edited"

    def __init__(self, queue_id: int, tenant_uuid: UUIDStr) -> None:
        """Initialize the event.

        Args:
           queue_id: Queue ID
           tenant_uuid: tenant UUID

        """
        content = {"id": int(queue_id)}
        super().__init__(content, tenant_uuid)


class QueueFallbackEditedEvent(TenantEvent):
    """Event for when a queue fallback is edited."""

    service = "confd"
    name = "queue_fallback_edited"
    routing_key_fmt = "config.queues.fallbacks.edited"

    def __init__(self, queue_id: int, tenant_uuid: UUIDStr) -> None:
        """Initialize Event.

        Args:
            queue_id (int): The ID of the queue.
            tenant_uuid (UUIDStr): tenant UUID.

        """
        content = {"id": int(queue_id)}
        super().__init__(content, tenant_uuid)
