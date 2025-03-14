# resources/incall/event.py
from typing import ClassVar

from resources.common.event import TenantEvent


class IncallEvent(TenantEvent):
    """Base class for Incall events."""

    service: ClassVar[str] = "confd"
    content: dict


class IncallCreatedEvent(IncallEvent):
    """Event for when an incall is created."""

    name: ClassVar[str] = "incall_created"
    routing_key_fmt: ClassVar[str] = "config.incalls.created"

    def __init__(self, incall_id: int, **data):
        content = {"id": incall_id}
        super().__init__(content=content, **data)


class IncallDeletedEvent(IncallEvent):
    """Event for when an incall is deleted."""

    name: ClassVar[str] = "incall_deleted"
    routing_key_fmt: ClassVar[str] = "config.incalls.deleted"

    def __init__(self, incall_id: int, **data):
        content = {"id": incall_id}
        super().__init__(content=content, **data)


class IncallEditedEvent(IncallEvent):
    """Event for when an incall is edited."""

    name: ClassVar[str] = "incall_edited"
    routing_key_fmt: ClassVar[str] = "config.incalls.edited"

    def __init__(self, incall_id: int, **data):
        content = {"id": incall_id}
        super().__init__(content=content, **data)
