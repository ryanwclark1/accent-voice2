# resources/paging/event.py
from typing import ClassVar

from accent_bus.resources.common.event import TenantEvent


class PagingEvent(TenantEvent):
    """Base class for Paging events."""

    service: ClassVar[str] = "confd"
    content: dict


class PagingCreatedEvent(PagingEvent):
    """Event for when a paging group is created."""

    name: ClassVar[str] = "paging_created"
    routing_key_fmt: ClassVar[str] = "config.pagings.created"

    def __init__(self, paging_id: int, **data):
        content = {"id": paging_id}
        super().__init__(content=content, **data)


class PagingDeletedEvent(PagingEvent):
    """Event for when a paging group is deleted."""

    name: ClassVar[str] = "paging_deleted"
    routing_key_fmt: ClassVar[str] = "config.pagings.deleted"

    def __init__(self, paging_id: int, **data):
        content = {"id": paging_id}
        super().__init__(content=content, **data)


class PagingEditedEvent(PagingEvent):
    """Event for when a paging group is edited."""

    name: ClassVar[str] = "paging_edited"
    routing_key_fmt: ClassVar[str] = "config.pagings.edited"

    def __init__(self, paging_id: int, **data):
        content = {"id": paging_id}
        super().__init__(content=content, **data)
