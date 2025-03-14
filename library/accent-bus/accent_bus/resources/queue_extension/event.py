# resources/queue_extension/event.py
from typing import ClassVar

from accent_bus.resources.common.event import TenantEvent


class QueueExtensionEvent(TenantEvent):
    """Base class for Queue Extension events."""

    service: ClassVar[str] = "confd"
    content: dict


class QueueExtensionAssociatedEvent(QueueExtensionEvent):
    """Event for when an extension is associated with a queue."""

    name: ClassVar[str] = "queue_extension_associated"
    routing_key_fmt: ClassVar[str] = "config.queues.extensions.updated"

    def __init__(
        self,
        queue_id: int,
        extension_id: int,
        **data,
    ):
        content = {
            "queue_id": queue_id,
            "extension_id": extension_id,
        }
        super().__init__(content=content, **data)


class QueueExtensionDissociatedEvent(QueueExtensionEvent):
    """Event for when an extension is dissociated from a queue."""

    name: ClassVar[str] = "queue_extension_dissociated"
    routing_key_fmt: ClassVar[str] = "config.queues.extensions.deleted"

    def __init__(
        self,
        queue_id: int,
        extension_id: int,
        **data,
    ):
        content = {
            "queue_id": queue_id,
            "extension_id": extension_id,
        }
        super().__init__(content=content, **data)
