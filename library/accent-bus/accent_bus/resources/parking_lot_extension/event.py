# accent_bus/resources/parking_lot_extension/event.py
# Copyright 2025 Accent Communications

"""Parking lot extension events."""

from accent_bus.resources.common.event import TenantEvent
from accent_bus.resources.common.types import UUIDStr


class ParkingLotExtensionAssociatedEvent(TenantEvent):
    """Event for when a parking lot extension is associated."""

    service = "confd"
    name = "parking_lot_extension_associated"
    routing_key_fmt = "config.parkinglots.extensions.updated"

    def __init__(
        self,
        parking_id: int,
        extension_id: int,
        tenant_uuid: UUIDStr,
    ) -> None:
        """Initialize the event.

        Args:
           parking_id: Parking Lot ID
           extension_id: Extension ID
           tenant_uuid: tenant UUID

        """
        content = {
            "parking_lot_id": parking_id,
            "extension_id": extension_id,
        }
        super().__init__(content, tenant_uuid)


class ParkingLotExtensionDissociatedEvent(TenantEvent):
    """Event for when a parking lot extension is dissociated."""

    service = "confd"
    name = "parking_lot_extension_dissociated"
    routing_key_fmt = "config.parkinglots.extensions.deleted"

    def __init__(
        self,
        parking_id: int,
        extension_id: int,
        tenant_uuid: UUIDStr,
    ) -> None:
        """Initialize event.

        Args:
          parking_id: Parking Lot ID
          extension_id: Extension ID
          tenant_uuid: tenant UUID

        """
        content = {
            "parking_lot_id": parking_id,
            "extension_id": extension_id,
        }
        super().__init__(content, tenant_uuid)
