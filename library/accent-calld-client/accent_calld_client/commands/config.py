# Copyright 2025 Accent Communications

"""Commands for configuration management in the Calld API.

This module provides commands for retrieving and updating Calld configuration.
"""

from __future__ import annotations

import logging
from typing import Any

from accent_calld_client.command import CalldCommand

logger = logging.getLogger(__name__)


class ConfigCommand(CalldCommand):
    """Command for managing Calld configuration.

    This command provides methods for retrieving and updating the
    global configuration.
    """

    resource = "config"

    async def get_async(self) -> dict[str, Any]:
        """Get the current configuration asynchronously.

        Returns:
            Configuration data as a dictionary

        Raises:
            CalldError: If the API returns an error

        """
        headers = self._get_headers()
        url = self.base_url
        r = await self.async_client.get(url, headers=headers)
        self.raise_from_response(r)
        return r.json()

    def get(self) -> dict[str, Any]:
        """Get the current configuration.

        Returns:
            Configuration data as a dictionary

        Raises:
            CalldError: If the API returns an error

        """
        headers = self._get_headers()
        url = self.base_url
        r = self.sync_client.get(url, headers=headers)
        self.raise_from_response(r)
        return r.json()

    async def patch_async(self, config_patch: dict[str, Any]) -> dict[str, Any]:
        """Update the configuration asynchronously.

        Args:
            config_patch: Configuration changes to apply

        Returns:
            Updated configuration data as a dictionary

        Raises:
            CalldError: If the API returns an error

        """
        headers = self._get_headers()
        url = self.base_url
        r = await self.async_client.patch(url, headers=headers, json=config_patch)
        self.raise_from_response(r)
        return r.json()

    def patch(self, config_patch: dict[str, Any]) -> dict[str, Any]:
        """Update the configuration.

        Args:
            config_patch: Configuration changes to apply

        Returns:
            Updated configuration data as a dictionary

        Raises:
            CalldError: If the API returns an error

        """
        headers = self._get_headers()
        url = self.base_url
        r = self.sync_client.patch(url, headers=headers, json=config_patch)
        self.raise_from_response(r)
        return r.json()
