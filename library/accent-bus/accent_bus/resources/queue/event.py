# resources/queue/event.py
from typing import ClassVar

from accent_bus.resources.common.event import TenantEvent


class QueueEvent(TenantEvent):
    """Base class for Queue events."""

    service: ClassVar[str] = "confd"
    content: dict


class QueueCreatedEvent(QueueEvent):
    """Event for when a queue is created."""

    name: ClassVar[str] = "queue_created"
    routing_key_fmt: ClassVar[str] = "config.queues.created"

    def __init__(self, queue_id: int, **data):
        content = {"id": int(queue_id)}
        super().__init__(content=content, **data)


class QueueDeletedEvent(QueueEvent):
    """Event for when a queue is deleted."""

    name: ClassVar[str] = "queue_deleted"
    routing_key_fmt: ClassVar[str] = "config.queues.deleted"

    def __init__(self, queue_id: int, **data):
        content = {"id": int(queue_id)}
        super().__init__(content=content, **data)


class QueueEditedEvent(QueueEvent):
    """Event for when a queue is edited."""

    name: ClassVar[str] = "queue_edited"
    routing_key_fmt: ClassVar[str] = "config.queues.edited"

    def __init__(self, queue_id: int, **data):
        content = {"id": int(queue_id)}
        super().__init__(content=content, **data)


class QueueFallbackEditedEvent(QueueEvent):
    """Event for queue fallback is edited."""

    name: ClassVar[str] = "queue_fallback_edited"
    routing_key_fmt: ClassVar[str] = "config.queues.fallbacks.edited"

    def __init__(self, queue_id: int, **data):
        content = {"id": int(queue_id)}
        super().__init__(content=content, **data)
