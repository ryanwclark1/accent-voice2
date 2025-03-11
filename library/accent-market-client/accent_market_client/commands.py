# Copyright 2025 Accent Communications

"""Command implementations for the Accent Market API.

This module provides command classes for interacting with specific
endpoints of the Accent Market API.
"""

from __future__ import annotations

import builtins
import functools
import logging
import time
from typing import ClassVar

from accent_lib_rest_client import RESTCommand

from .models import PluginResponse

# Configure logging
logger = logging.getLogger(__name__)

# Default request headers
DEFAULT_HEADERS = {"Accept": "application/json", "Content-Type": "application/json"}


class PluginCommand(RESTCommand):
    """Command for interacting with plugin endpoints.

    This command provides methods for managing plugins in the Accent Market.
    """

    resource: ClassVar[str] = "plugins"
    _headers: ClassVar[dict[str, str]] = DEFAULT_HEADERS

    @functools.lru_cache(maxsize=32)
    def list(self) -> builtins.list[PluginResponse]:
        """List all available plugins.

        Returns:
            List of plugin data objects

        Raises:
            AccentAPIError: If the API request fails

        """
        logger.debug("Fetching plugin list")
        start_time = time.time()

        response = self.sync_client.get(self.base_url, headers=self._headers)

        json_response = self.process_json_response(response, start_time)
        logger.info(
            "Retrieved %d plugins in %.2fs",
            len(json_response.data),
            json_response.response_time or 0,
        )

        # Parse the response data into proper models
        plugins_data = json_response.data
        return [PluginResponse.model_validate(item) for item in plugins_data]

    async def list_async(self) -> builtins.list[PluginResponse]:
        """List all available plugins asynchronously.

        Returns:
            List of plugin data objects

        Raises:
            AccentAPIError: If the API request fails

        """
        logger.debug("Fetching plugin list asynchronously")
        start_time = time.time()

        response = await self.async_client.get(self.base_url, headers=self._headers)

        json_response = self.process_json_response(response, start_time)
        logger.info(
            "Retrieved %d plugins in %.2fs",
            len(json_response.data),
            json_response.response_time or 0,
        )

        # Parse the response data into proper models
        plugins_data = json_response.data
        return [PluginResponse.model_validate(item) for item in plugins_data]

    def get(self, plugin_id: str) -> PluginResponse:
        """Get details of a specific plugin.

        Args:
            plugin_id: Unique identifier of the plugin

        Returns:
            Plugin data object

        Raises:
            AccentAPIError: If the API request fails

        """
        logger.debug("Fetching plugin with ID: %s", plugin_id)
        url = f"{self.base_url}/{plugin_id}"

        response = self.sync_client.get(url, headers=self._headers)

        json_response = self.process_json_response(response)
        return PluginResponse.model_validate(json_response.data)

    async def get_async(self, plugin_id: str) -> PluginResponse:
        """Get details of a specific plugin asynchronously.

        Args:
            plugin_id: Unique identifier of the plugin

        Returns:
            Plugin data object

        Raises:
            AccentAPIError: If the API request fails

        """
        logger.debug("Fetching plugin with ID: %s asynchronously", plugin_id)
        url = f"{self.base_url}/{plugin_id}"

        response = await self.async_client.get(url, headers=self._headers)

        json_response = self.process_json_response(response)
        return PluginResponse.model_validate(json_response.data)
