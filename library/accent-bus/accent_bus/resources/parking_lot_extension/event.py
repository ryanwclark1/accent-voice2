# resources/parking_lot_extension/event.py
from typing import ClassVar

from accent_bus.resources.common.event import TenantEvent


class ParkingLotExtensionEvent(TenantEvent):
    """Base class for Parking Lot Extension events."""

    service: ClassVar[str] = "confd"
    content: dict


class ParkingLotExtensionAssociatedEvent(ParkingLotExtensionEvent):
    """Event for when an extension is associated with a parking lot."""

    name: ClassVar[str] = "parking_lot_extension_associated"
    routing_key_fmt: ClassVar[str] = "config.parkinglots.extensions.updated"

    def __init__(
        self,
        parking_id: int,
        extension_id: int,
        **data,
    ):
        content = {
            "parking_lot_id": parking_id,
            "extension_id": extension_id,
        }
        super().__init__(content=content, **data)


class ParkingLotExtensionDissociatedEvent(ParkingLotExtensionEvent):
    """Event for when an extension is dissociated from a parking lot."""

    name: ClassVar[str] = "parking_lot_extension_dissociated"
    routing_key_fmt: ClassVar[str] = "config.parkinglots.extensions.deleted"

    def __init__(
        self,
        parking_id: int,
        extension_id: int,
        **data,
    ):
        content = {
            "parking_lot_id": parking_id,
            "extension_id": extension_id,
        }
        super().__init__(content=content, **data)
