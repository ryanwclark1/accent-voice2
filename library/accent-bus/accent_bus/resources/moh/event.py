# resources/moh/event.py
from typing import ClassVar

from accent_bus.resources.common.event import TenantEvent

from .types import MOHDict


class MOHEvent(TenantEvent):
    """Base class for Music on Hold events."""

    service: ClassVar[str] = "confd"
    content: dict


class MOHCreatedEvent(MOHEvent):
    """Event for when a MOH is created."""

    name: ClassVar[str] = "moh_created"
    routing_key_fmt: ClassVar[str] = "config.moh.created"

    def __init__(self, moh: MOHDict, **data):
        super().__init__(content=moh, **data)


class MOHDeletedEvent(MOHEvent):
    """Event for when a MOH is deleted."""

    name: ClassVar[str] = "moh_deleted"
    routing_key_fmt: ClassVar[str] = "config.moh.deleted"

    def __init__(self, moh: MOHDict, **data):
        super().__init__(content=moh, **data)


class MOHEditedEvent(MOHEvent):
    """Event for when a MOH is edited."""

    name: ClassVar[str] = "moh_edited"
    routing_key_fmt: ClassVar[str] = "config.moh.edited"

    def __init__(self, moh: MOHDict, **data):
        super().__init__(content=moh, **data)
