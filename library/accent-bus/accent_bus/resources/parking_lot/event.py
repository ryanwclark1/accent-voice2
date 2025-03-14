# accent_bus/resources/parking_lot/event.py
# Copyright 2025 Accent Communications

"""Parking lot events."""

from accent_bus.resources.common.event import TenantEvent
from accent_bus.resources.common.types import UUIDStr


class ParkingLotCreatedEvent(TenantEvent):
    """Event for when a parking lot is created."""

    service = "confd"
    name = "parking_lot_created"
    routing_key_fmt = "config.parkinglots.created"

    def __init__(self, parking_id: int, tenant_uuid: UUIDStr) -> None:
        """Initialize event.

        Args:
          parking_id: Parking ID
          tenant_uuid: tenant UUID

        """
        content = {"id": int(parking_id)}
        super().__init__(content, tenant_uuid)


class ParkingLotDeletedEvent(TenantEvent):
    """Event for when a parking lot is deleted."""

    service = "confd"
    name = "parking_lot_deleted"
    routing_key_fmt = "config.parkinglots.deleted"

    def __init__(self, parking_id: int, tenant_uuid: UUIDStr) -> None:
        """Initialize Event.

        Args:
           parking_id: Parking ID
           tenant_uuid: tenant UUID

        """
        content = {"id": int(parking_id)}
        super().__init__(content, tenant_uuid)


class ParkingLotEditedEvent(TenantEvent):
    """Event for when a parking lot is edited."""

    service = "confd"
    name = "parking_lot_edited"
    routing_key_fmt = "config.parkinglots.edited"

    def __init__(self, parking_id: int, tenant_uuid: UUIDStr) -> None:
        """Initialize the event.

        Args:
           parking_id: Parking Lot ID
           tenant_uuid: tenant UUID

        """
        content = {"id": int(parking_id)}
        super().__init__(content, tenant_uuid)
