# Copyright 2025 Accent Communications

"""High Availability command module for the Configuration Daemon API."""

import logging
from typing import Any

from accent_lib_rest_client import HTTPCommand

from accent_confd_client.util import url_join

# Configure standard logging
logger = logging.getLogger(__name__)


class HACommand(HTTPCommand):
    """Command for managing High Availability settings."""

    headers = {"Accept": "application/json"}

    def get(self) -> dict[str, Any]:
        """Get High Availability settings.

        Returns:
            High Availability settings

        """
        url = url_join("ha")
        response = self.sync_client.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    async def get_async(self) -> dict[str, Any]:
        """Get High Availability settings asynchronously.

        Returns:
            High Availability settings

        """
        url = url_join("ha")
        response = await self.async_client.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def update(self, body: dict[str, Any]) -> None:
        """Update High Availability settings.

        Args:
            body: High Availability settings

        """
        url = url_join("ha")
        response = self.sync_client.put(url, json=body, headers=self.headers)
        response.raise_for_status()

    async def update_async(self, body: dict[str, Any]) -> None:
        """Update High Availability settings asynchronously.

        Args:
            body: High Availability settings

        """
        url = url_join("ha")
        response = await self.async_client.put(url, json=body, headers=self.headers)
        response.raise_for_status()
