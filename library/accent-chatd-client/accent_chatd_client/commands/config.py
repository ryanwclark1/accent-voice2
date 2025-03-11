# Copyright 2025 Accent Communications

"""Commands for managing Chat Daemon configuration."""

import logging
from typing import Any

from .helpers.base import BaseCommand

logger = logging.getLogger(__name__)


class ConfigCommand(BaseCommand):
    """Command for managing Chat Daemon configuration settings."""

    resource = "config"

    async def get_async(self) -> dict[str, Any]:
        """Get the current configuration asynchronously.

        Returns:
            Current configuration settings

        Raises:
            ChatdError: If the API request fails

        """
        headers = self._get_headers()
        response = await self.async_client.get(self.base_url, headers=headers)
        self.raise_from_response(response)
        return response.json()

    def get(self) -> dict[str, Any]:
        """Get the current configuration.

        Returns:
            Current configuration settings

        Raises:
            ChatdError: If the API request fails

        """
        headers = self._get_headers()
        response = self.sync_client.get(self.base_url, headers=headers)
        self.raise_from_response(response)
        return response.json()

    async def patch_async(self, config_patch: dict[str, Any]) -> dict[str, Any]:
        """Update configuration settings asynchronously.

        Args:
            config_patch: Dictionary of settings to update

        Returns:
            Updated configuration settings

        Raises:
            ChatdError: If the API request fails

        """
        headers = self._get_headers()
        response = await self.async_client.patch(
            self.base_url, headers=headers, json=config_patch
        )
        if response.status_code != 200:
            self.raise_from_response(response)
        return response.json()

    def patch(self, config_patch: dict[str, Any]) -> dict[str, Any]:
        """Update configuration settings.

        Args:
            config_patch: Dictionary of settings to update

        Returns:
            Updated configuration settings

        Raises:
            ChatdError: If the API request fails

        """
        headers = self._get_headers()
        response = self.sync_client.patch(
            self.base_url, headers=headers, json=config_patch
        )
        if response.status_code != 200:
            self.raise_from_response(response)
        return response.json()
