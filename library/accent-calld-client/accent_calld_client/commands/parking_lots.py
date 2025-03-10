# Copyright 2025 Accent Communications

"""Commands for parking lot management in the Calld API.

This module provides commands for listing and retrieving parking lot information.
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

from accent_calld_client.command import CalldCommand

if TYPE_CHECKING:
    from collections.abc import Mapping

logger = logging.getLogger(__name__)


class ParkingLotsCommand(CalldCommand):
    """Command for managing parking lots.

    This command provides methods for listing and retrieving parking lot information.
    """

    resource = "parkinglots"

    async def get_async(self, parking_id: int) -> Mapping[str, Any]:
        """Get information about a specific parking lot asynchronously.

        Args:
            parking_id: ID of the parking lot

        Returns:
            Parking lot data as a dictionary

        Raises:
            CalldError: If the API returns an error

        """
        headers = self._get_headers()
        url = self._client.url(self.resource, parking_id)
        r = await self.async_client.get(url, headers=headers)

        if r.status_code != 200:
            self.raise_from_response(r)

        return r.json()

    def get(self, parking_id: int) -> Mapping[str, Any]:
        """Get information about a specific parking lot.

        Args:
            parking_id: ID of the parking lot

        Returns:
            Parking lot data as a dictionary

        Raises:
            CalldError: If the API returns an error

        """
        headers = self._get_headers()
        url = self._client.url(self.resource, parking_id)
        r = self.sync_client.get(url, headers=headers)

        if r.status_code != 200:
            self.raise_from_response(r)

        return r.json()

    async def list_async(self) -> Mapping[str, Any]:
        """List all parking lots asynchronously.

        Returns:
            Dictionary containing parking lot information

        Raises:
            CalldError: If the API returns an error

        """
        headers = self._get_headers()
        url = self._client.url(self.resource)
        r = await self.async_client.get(url, headers=headers)

        if r.status_code != 200:
            self.raise_from_response(r)

        return r.json()

    def list_(self) -> Mapping[str, Any]:
        """List all parking lots.

        Returns:
            Dictionary containing parking lot information

        Raises:
            CalldError: If the API returns an error

        """
        headers = self._get_headers()
        url = self._client.url(self.resource)
        r = self.sync_client.get(url, headers=headers)

        if r.status_code != 200:
            self.raise_from_response(r)

        return r.json()
