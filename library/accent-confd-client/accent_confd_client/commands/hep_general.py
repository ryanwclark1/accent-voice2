# Copyright 2025 Accent Communications

"""HEP general command module for the Configuration Daemon API."""

import logging
from typing import Any

from accent_lib_rest_client import RESTCommand

# Configure standard logging
logger = logging.getLogger(__name__)


class HEPGeneralCommand(RESTCommand):
    """Command for managing HEP general settings."""

    resource = "asterisk/hep/general"

    def get(self) -> dict[str, Any]:
        """Get HEP general settings.

        Returns:
            HEP general settings

        """
        response = self.sync_client.get(self.base_url)
        response.raise_for_status()
        return response.json()

    async def get_async(self) -> dict[str, Any]:
        """Get HEP general settings asynchronously.

        Returns:
            HEP general settings

        """
        response = await self.async_client.get(self.base_url)
        response.raise_for_status()
        return response.json()

    def update(self, body: dict[str, Any]) -> None:
        """Update HEP general settings.

        Args:
            body: HEP general settings

        """
        response = self.sync_client.put(self.base_url, json=body)
        response.raise_for_status()

    async def update_async(self, body: dict[str, Any]) -> None:
        """Update HEP general settings asynchronously.

        Args:
            body: HEP general settings

        """
        response = await self.async_client.put(self.base_url, json=body)
        response.raise_for_status()
