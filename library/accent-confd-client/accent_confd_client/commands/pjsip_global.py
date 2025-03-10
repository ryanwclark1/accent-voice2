# Copyright 2025 Accent Communications

"""PJSIP global command module for the Configuration Daemon API."""

import logging
from typing import Any

from accent_lib_rest_client import RESTCommand

# Configure standard logging
logger = logging.getLogger(__name__)


class PJSIPGlobalCommand(RESTCommand):
    """Command for managing PJSIP global settings."""

    resource = "asterisk/pjsip/global"

    def get(self) -> dict[str, Any]:
        """Get PJSIP global settings.

        Returns:
            PJSIP global settings

        """
        response = self.sync_client.get(self.base_url)
        response.raise_for_status()
        return response.json()

    async def get_async(self) -> dict[str, Any]:
        """Get PJSIP global settings asynchronously.

        Returns:
            PJSIP global settings

        """
        response = await self.async_client.get(self.base_url)
        response.raise_for_status()
        return response.json()

    def update(self, body: dict[str, Any]) -> None:
        """Update PJSIP global settings.

        Args:
            body: PJSIP global settings

        """
        response = self.sync_client.put(self.base_url, json=body)
        response.raise_for_status()

    async def update_async(self, body: dict[str, Any]) -> None:
        """Update PJSIP global settings asynchronously.

        Args:
            body: PJSIP global settings

        """
        response = await self.async_client.put(self.base_url, json=body)
        response.raise_for_status()
