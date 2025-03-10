# Copyright 2025 Accent Communications

"""Features application map command module for the Configuration Daemon API."""

import logging
from typing import Any

from accent_lib_rest_client import RESTCommand

# Configure standard logging
logger = logging.getLogger(__name__)


class FeaturesApplicationmapCommand(RESTCommand):
    """Command for managing features application map settings."""

    resource = "asterisk/features/applicationmap"

    def get(self) -> dict[str, Any]:
        """Get features application map settings.

        Returns:
            Features application map settings

        """
        response = self.sync_client.get(self.base_url)
        response.raise_for_status()
        return response.json()

    async def get_async(self) -> dict[str, Any]:
        """Get features application map settings asynchronously.

        Returns:
            Features application map settings

        """
        response = await self.async_client.get(self.base_url)
        response.raise_for_status()
        return response.json()

    def update(self, body: dict[str, Any]) -> None:
        """Update features application map settings.

        Args:
            body: Features application map settings

        """
        response = self.sync_client.put(self.base_url, json=body)
        response.raise_for_status()

    async def update_async(self, body: dict[str, Any]) -> None:
        """Update features application map settings asynchronously.

        Args:
            body: Features application map settings

        """
        response = await self.async_client.put(self.base_url, json=body)
        response.raise_for_status()
