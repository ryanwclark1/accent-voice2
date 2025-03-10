# Copyright 2025 Accent Communications

"""Voicemail zone messages command module for the Configuration Daemon API."""

import logging
from typing import Any

from accent_lib_rest_client import RESTCommand

# Configure standard logging
logger = logging.getLogger(__name__)


class VoicemailZoneMessagesCommand(RESTCommand):
    """Command for managing voicemail zone messages settings."""

    resource = "asterisk/voicemail/zonemessages"

    def get(self) -> dict[str, Any]:
        """Get voicemail zone messages settings.

        Returns:
            Voicemail zone messages settings

        """
        response = self.sync_client.get(self.base_url)
        response.raise_for_status()
        return response.json()

    async def get_async(self) -> dict[str, Any]:
        """Get voicemail zone messages settings asynchronously.

        Returns:
            Voicemail zone messages settings

        """
        response = await self.async_client.get(self.base_url)
        response.raise_for_status()
        return response.json()

    def update(self, body: dict[str, Any]) -> None:
        """Update voicemail zone messages settings.

        Args:
            body: Voicemail zone messages settings

        """
        response = self.sync_client.put(self.base_url, json=body)
        response.raise_for_status()

    async def update_async(self, body: dict[str, Any]) -> None:
        """Update voicemail zone messages settings asynchronously.

        Args:
            body: Voicemail zone messages settings

        """
        response = await self.async_client.put(self.base_url, json=body)
        response.raise_for_status()
