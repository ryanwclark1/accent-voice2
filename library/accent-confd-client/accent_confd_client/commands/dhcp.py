# Copyright 2025 Accent Communications

"""DHCP command module for the Configuration Daemon API."""

import logging
from typing import Any

from accent_lib_rest_client import HTTPCommand

from accent_confd_client.util import url_join

# Configure standard logging
logger = logging.getLogger(__name__)


class DHCPCommand(HTTPCommand):
    """Command for managing DHCP settings."""

    headers = {"Accept": "application/json"}

    def get(self) -> dict[str, Any]:
        """Get DHCP settings.

        Returns:
            DHCP settings

        """
        url = url_join("dhcp")
        response = self.sync_client.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    async def get_async(self) -> dict[str, Any]:
        """Get DHCP settings asynchronously.

        Returns:
            DHCP settings

        """
        url = url_join("dhcp")
        response = await self.async_client.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def update(self, body: dict[str, Any]) -> None:
        """Update DHCP settings.

        Args:
            body: DHCP settings

        """
        url = url_join("dhcp")
        response = self.sync_client.put(url, json=body, headers=self.headers)
        response.raise_for_status()

    async def update_async(self, body: dict[str, Any]) -> None:
        """Update DHCP settings asynchronously.

        Args:
            body: DHCP settings

        """
        url = url_join("dhcp")
        response = await self.async_client.put(url, json=body, headers=self.headers)
        response.raise_for_status()
