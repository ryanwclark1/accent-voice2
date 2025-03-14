# resources/parking_lot/event.py
from typing import ClassVar

from accent_bus.resources.common.event import TenantEvent


class ParkingLotEvent(TenantEvent):
    """Base class for Parking Lot events."""

    service: ClassVar[str] = "confd"
    content: dict


class ParkingLotCreatedEvent(ParkingLotEvent):
    """Event for when a parking lot is created."""

    name: ClassVar[str] = "parking_lot_created"
    routing_key_fmt: ClassVar[str] = "config.parkinglots.created"

    def __init__(self, parking_id: int, **data):
        content = {"id": int(parking_id)}
        super().__init__(content=content, **data)


class ParkingLotDeletedEvent(ParkingLotEvent):
    """Event for when a parking lot is deleted."""

    name: ClassVar[str] = "parking_lot_deleted"
    routing_key_fmt: ClassVar[str] = "config.parkinglots.deleted"

    def __init__(self, parking_id: int, **data):
        content = {"id": int(parking_id)}
        super().__init__(content=content, **data)


class ParkingLotEditedEvent(ParkingLotEvent):
    """Event for when a parking lot is edited."""

    name: ClassVar[str] = "parking_lot_edited"
    routing_key_fmt: ClassVar[str] = "config.parkinglots.edited"

    def __init__(self, parking_id: int, **data):
        content = {"id": int(parking_id)}
        super().__init__(content=content, **data)
