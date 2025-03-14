# resources/ivr/event.py
from typing import ClassVar

from accent_bus.resources.common.event import TenantEvent


class IVREvent(TenantEvent):
    """Base class for IVR events."""

    service: ClassVar[str] = "confd"
    content: dict


class IVRCreatedEvent(IVREvent):
    """Event for when an IVR is created."""

    name: ClassVar[str] = "ivr_created"
    routing_key_fmt: ClassVar[str] = "config.ivr.created"

    def __init__(self, ivr_id: int, **data):
        content = {"id": ivr_id}
        super().__init__(content=content, **data)


class IVRDeletedEvent(IVREvent):
    """Event for when an IVR is deleted."""

    name: ClassVar[str] = "ivr_deleted"
    routing_key_fmt: ClassVar[str] = "config.ivr.deleted"

    def __init__(self, ivr_id: int, **data):
        content = {"id": ivr_id}
        super().__init__(content=content, **data)


class IVREditedEvent(IVREvent):
    """Event for when an IVR is edited."""

    name: ClassVar[str] = "ivr_edited"
    routing_key_fmt: ClassVar[str] = "config.ivr.edited"

    def __init__(self, ivr_id: int, **data):
        content = {"id": ivr_id}
        super().__init__(content=content, **data)
