# Copyright 2025 Accent Communications

"""Provisioning networking command module for the Configuration Daemon API."""

import logging
from typing import Any

from accent_lib_rest_client import HTTPCommand

from accent_confd_client.util import url_join

# Configure standard logging
logger = logging.getLogger(__name__)


class ProvisioningNetworkingCommand(HTTPCommand):
    """Command for managing provisioning networking settings."""

    headers = {"Accept": "application/json"}

    def get(self) -> dict[str, Any]:
        """Get provisioning networking settings.

        Returns:
            Provisioning networking settings

        """
        url = url_join("provisioning", "networking")
        response = self.sync_client.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    async def get_async(self) -> dict[str, Any]:
        """Get provisioning networking settings asynchronously.

        Returns:
            Provisioning networking settings

        """
        url = url_join("provisioning", "networking")
        response = await self.async_client.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def update(self, body: dict[str, Any]) -> None:
        """Update provisioning networking settings.

        Args:
            body: Provisioning networking settings

        """
        url = url_join("provisioning", "networking")
        response = self.sync_client.put(url, json=body, headers=self.headers)
        response.raise_for_status()

    async def update_async(self, body: dict[str, Any]) -> None:
        """Update provisioning networking settings asynchronously.

        Args:
            body: Provisioning networking settings

        """
        url = url_join("provisioning", "networking")
        response = await self.async_client.put(url, json=body, headers=self.headers)
        response.raise_for_status()
