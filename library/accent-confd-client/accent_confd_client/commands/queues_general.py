# Copyright 2025 Accent Communications

"""Queues general command module for the Configuration Daemon API."""

import logging
from typing import Any

from accent_lib_rest_client import RESTCommand

# Configure standard logging
logger = logging.getLogger(__name__)


class QueuesGeneralCommand(RESTCommand):
    """Command for managing queues general settings."""

    resource = "asterisk/queues/general"

    def get(self) -> dict[str, Any]:
        """Get queues general settings.

        Returns:
            Queues general settings

        """
        response = self.sync_client.get(self.base_url)
        response.raise_for_status()
        return response.json()

    async def get_async(self) -> dict[str, Any]:
        """Get queues general settings asynchronously.

        Returns:
            Queues general settings

        """
        response = await self.async_client.get(self.base_url)
        response.raise_for_status()
        return response.json()

    def update(self, body: dict[str, Any]) -> None:
        """Update queues general settings.

        Args:
            body: Queues general settings

        """
        response = self.sync_client.put(self.base_url, json=body)
        response.raise_for_status()

    async def update_async(self, body: dict[str, Any]) -> None:
        """Update queues general settings asynchronously.

        Args:
            body: Queues general settings

        """
        response = await self.async_client.put(self.base_url, json=body)
        response.raise_for_status()
