# accent_bus/resources/call_pickup/event.py
# Copyright 2025 Accent Communications

"""Call pickup events."""

from accent_bus.resources.common.event import TenantEvent
from accent_bus.resources.common.types import UUIDStr


class CallPickupCreatedEvent(TenantEvent):
    """Event for when a call pickup is created."""

    service = "confd"
    name = "call_pickup_created"
    routing_key_fmt = "config.callpickup.created"

    def __init__(self, call_pickup_id: int, tenant_uuid: UUIDStr) -> None:
        """Initialize the event.

        Args:
            call_pickup_id (int): The ID of the call pickup.
            tenant_uuid (UUIDStr):  tenant UUID.

        """
        content = {"id": call_pickup_id}
        super().__init__(content, tenant_uuid)


class CallPickupDeletedEvent(TenantEvent):
    """Event for when a call pickup is deleted."""

    service = "confd"
    name = "call_pickup_deleted"
    routing_key_fmt = "config.callpickup.deleted"

    def __init__(self, call_pickup_id: int, tenant_uuid: UUIDStr) -> None:
        """Initialize Event.

        Args:
           call_pickup_id: Call Pickup ID
           tenant_uuid: tenant UUID

        """
        content = {"id": call_pickup_id}
        super().__init__(content, tenant_uuid)


class CallPickupEditedEvent(TenantEvent):
    """Event for when a call pickup is edited."""

    service = "confd"
    name = "call_pickup_edited"
    routing_key_fmt = "config.callpickup.edited"

    def __init__(self, call_pickup_id: int, tenant_uuid: UUIDStr) -> None:
        """Initialize the event.

        Args:
           call_pickup_id: Call Pickup ID
           tenant_uuid: tenant UUID

        """
        content = {"id": call_pickup_id}
        super().__init__(content, tenant_uuid)
