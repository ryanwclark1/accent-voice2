# accent_bus/resources/queue_extension/event.py
# Copyright 2025 Accent Communications

"""Queue extension events."""

from accent_bus.resources.common.event import TenantEvent
from accent_bus.resources.common.types import UUIDStr


class QueueExtensionAssociatedEvent(TenantEvent):
    """Event for when a queue extension is associated."""

    service = "confd"
    name = "queue_extension_associated"
    routing_key_fmt = "config.queues.extensions.updated"

    def __init__(
        self,
        queue_id: int,
        extension_id: int,
        tenant_uuid: UUIDStr,
    ) -> None:
        """Initialize Event.

        Args:
           queue_id: Queue ID
           extension_id: Extension ID
           tenant_uuid: tenant UUID

        """
        content = {
            "queue_id": queue_id,
            "extension_id": extension_id,
        }
        super().__init__(content, tenant_uuid)


class QueueExtensionDissociatedEvent(TenantEvent):
    """Event for when a queue extension is dissociated."""

    service = "confd"
    name = "queue_extension_dissociated"
    routing_key_fmt = "config.queues.extensions.deleted"

    def __init__(
        self,
        queue_id: int,
        extension_id: int,
        tenant_uuid: UUIDStr,
    ) -> None:
        """Initialize the event.

        Args:
           queue_id: Queue ID
           extension_id: Extension ID
           tenant_uuid: tenant UUID

        """
        content = {
            "queue_id": queue_id,
            "extension_id": extension_id,
        }
        super().__init__(content, tenant_uuid)
