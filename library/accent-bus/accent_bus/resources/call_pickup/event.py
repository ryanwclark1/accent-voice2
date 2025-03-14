# resources/call_pickup/event.py
from typing import ClassVar

from resources.common.event import TenantEvent


class CallPickupEvent(TenantEvent):
    """Base class for Call Pickup events."""

    service: ClassVar[str] = "confd"
    content: dict


class CallPickupCreatedEvent(CallPickupEvent):
    """Event for when a call pickup is created."""

    name: ClassVar[str] = "call_pickup_created"
    routing_key_fmt: ClassVar[str] = "config.callpickup.created"

    def __init__(self, call_pickup_id: int, **data):
        content = {"id": call_pickup_id}
        super().__init__(content=content, **data)


class CallPickupDeletedEvent(CallPickupEvent):
    """Event for when a call pickup is deleted."""

    name: ClassVar[str] = "call_pickup_deleted"
    routing_key_fmt: ClassVar[str] = "config.callpickup.deleted"

    def __init__(self, call_pickup_id: int, **data):
        content = {"id": call_pickup_id}
        super().__init__(content=content, **data)


class CallPickupEditedEvent(CallPickupEvent):
    """Event for when a call pickup is edited."""

    name: ClassVar[str] = "call_pickup_edited"
    routing_key_fmt: ClassVar[str] = "config.callpickup.edited"

    def __init__(self, call_pickup_id: int, **data):
        content = {"id": call_pickup_id}
        super().__init__(content=content, **data)
