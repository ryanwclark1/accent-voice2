# Copyright 2025 Accent Communications

"""Configuration command module for the Configuration Daemon API."""

import logging
from typing import Any

from accent_lib_rest_client import HTTPCommand

from accent_confd_client.util import url_join

# Configure standard logging
logger = logging.getLogger(__name__)


class LiveReloadCommand(HTTPCommand):
    """Command for managing live reload settings."""

    def get(self) -> dict[str, Any]:
        """Get live reload settings.

        Returns:
            Live reload settings

        """
        url = url_join("configuration", "live_reload")
        response = self.sync_client.get(url)
        response.raise_for_status()
        return response.json()

    async def get_async(self) -> dict[str, Any]:
        """Get live reload settings asynchronously.

        Returns:
            Live reload settings

        """
        url = url_join("configuration", "live_reload")
        response = await self.async_client.get(url)
        response.raise_for_status()
        return response.json()

    def update(self, body: dict[str, Any]) -> None:
        """Update live reload settings.

        Args:
            body: Live reload settings

        """
        url = url_join("configuration", "live_reload")
        response = self.sync_client.put(url, json=body)
        response.raise_for_status()

    async def update_async(self, body: dict[str, Any]) -> None:
        """Update live reload settings asynchronously.

        Args:
            body: Live reload settings

        """
        url = url_join("configuration", "live_reload")
        response = await self.async_client.put(url, json=body)
        response.raise_for_status()


class ConfigurationCommand:
    """Command for managing configuration settings."""

    def __init__(self, client: Any) -> None:
        """Initialize the configuration command.

        Args:
            client: API client

        """
        self.live_reload = LiveReloadCommand(client)
