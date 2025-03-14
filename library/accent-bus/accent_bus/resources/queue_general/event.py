# resources/queue_general/event.py
from typing import ClassVar

from accent_bus.resources.common.event import ServiceEvent


class QueueGeneralEvent(ServiceEvent):
    """Base class for general Queue configuration events."""

    service: ClassVar[str] = "confd"
    content: dict = {}  # ServiceEvent needs a content attribute


class QueueGeneralEditedEvent(QueueGeneralEvent):
    """Event for when the general queue configuration is edited."""

    name: ClassVar[str] = "queue_general_edited"
    routing_key_fmt: ClassVar[str] = "config.queue_general.edited"
