# Copyright 2025 Accent Communications

"""Emails command module for the Configuration Daemon API."""

import logging
from typing import Any

from accent_lib_rest_client import RESTCommand

# Configure standard logging
logger = logging.getLogger(__name__)


class EmailsCommand(RESTCommand):
    """Command for managing email settings."""

    resource = "emails"

    def get(self) -> dict[str, Any]:
        """Get email settings.

        Returns:
            Email settings

        """
        response = self.sync_client.get(self.base_url)
        response.raise_for_status()
        return response.json()

    async def get_async(self) -> dict[str, Any]:
        """Get email settings asynchronously.

        Returns:
            Email settings

        """
        response = await self.async_client.get(self.base_url)
        response.raise_for_status()
        return response.json()

    def update(self, body: dict[str, Any]) -> None:
        """Update email settings.

        Args:
            body: Email settings

        """
        response = self.sync_client.put(self.base_url, json=body)
        response.raise_for_status()

    async def update_async(self, body: dict[str, Any]) -> None:
        """Update email settings asynchronously.

        Args:
            body: Email settings

        """
        response = await self.async_client.put(self.base_url, json=body)
        response.raise_for_status()
