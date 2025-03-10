# Copyright 2025 Accent Communications

"""Conference bridge default bridge command module for the Configuration Daemon API."""

import logging
from typing import Any

from accent_lib_rest_client import RESTCommand

# Configure standard logging
logger = logging.getLogger(__name__)


class ConfBridgeAccentDefaultBridgeCommand(RESTCommand):
    """Command for managing conference bridge default bridge settings."""

    resource = "asterisk/confbridge/accent_default_bridge"

    def get(self) -> dict[str, Any]:
        """Get conference bridge default bridge settings.

        Returns:
            Conference bridge default bridge settings

        """
        response = self.sync_client.get(self.base_url)
        response.raise_for_status()
        return response.json()

    async def get_async(self) -> dict[str, Any]:
        """Get conference bridge default bridge settings asynchronously.

        Returns:
            Conference bridge default bridge settings

        """
        response = await self.async_client.get(self.base_url)
        response.raise_for_status()
        return response.json()

    def update(self, body: dict[str, Any]) -> None:
        """Update conference bridge default bridge settings.

        Args:
            body: Conference bridge default bridge settings

        """
        response = self.sync_client.put(self.base_url, json=body)
        response.raise_for_status()

    async def update_async(self, body: dict[str, Any]) -> None:
        """Update conference bridge default bridge settings asynchronously.

        Args:
            body: Conference bridge default bridge settings

        """
        response = await self.async_client.put(self.base_url, json=body)
        response.raise_for_status()
