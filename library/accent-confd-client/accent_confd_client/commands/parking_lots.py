# Copyright 2025 Accent Communications

"""Parking lots command module for the Configuration Daemon API."""

import logging
from typing import Any

from accent_confd_client.crud import MultiTenantCommand
from accent_confd_client.relations import ParkingLotExtensionRelation
from accent_confd_client.util import extract_id

# Configure standard logging
logger = logging.getLogger(__name__)


class ParkingLotRelation:
    """Relations for parking lots."""

    def __init__(self, builder: Any, parking_lot_id: str) -> None:
        """Initialize parking lot relations.

        Args:
            builder: Client instance
            parking_lot_id: Parking lot ID

        """
        self.parking_lot_id = parking_lot_id
        self.parking_lot_extension = ParkingLotExtensionRelation(builder)

    @extract_id
    def add_extension(self, extension_id: str) -> Any:
        """Add an extension to the parking lot.

        Args:
            extension_id: Extension ID

        Returns:
            API response

        """
        return self.parking_lot_extension.associate(self.parking_lot_id, extension_id)

    @extract_id
    async def add_extension_async(self, extension_id: str) -> Any:
        """Add an extension to the parking lot asynchronously.

        Args:
            extension_id: Extension ID

        Returns:
            API response

        """
        return await self.parking_lot_extension.associate_async(
            self.parking_lot_id, extension_id
        )

    @extract_id
    def remove_extension(self, extension_id: str) -> Any:
        """Remove an extension from the parking lot.

        Args:
            extension_id: Extension ID

        Returns:
            API response

        """
        return self.parking_lot_extension.dissociate(self.parking_lot_id, extension_id)

    @extract_id
    async def remove_extension_async(self, extension_id: str) -> Any:
        """Remove an extension from the parking lot asynchronously.

        Args:
            extension_id: Extension ID

        Returns:
            API response

        """
        return await self.parking_lot_extension.dissociate_async(
            self.parking_lot_id, extension_id
        )


class ParkingLotsCommand(MultiTenantCommand):
    """Command for managing parking lots."""

    resource = "parkinglots"
    relation_cmd = ParkingLotRelation
