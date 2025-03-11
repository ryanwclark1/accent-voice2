# Copyright 2025 Accent Communications

"""Commands for checking Chat Daemon status."""

import logging
from typing import Any

from .helpers.base import BaseCommand

logger = logging.getLogger(__name__)


class StatusCommand(BaseCommand):
    """Command for checking the status of the Chat Daemon service."""

    resource = "status"

    async def get_async(self) -> dict[str, Any]:
        """Get the service status asynchronously.

        Returns:
            Status information

        Raises:
            ChatdError: If the API request fails

        """
        headers = self._get_headers()
        response = await self.async_client.get(self.base_url, headers=headers)
        self.raise_from_response(response)
        return response.json()

    def get(self) -> dict[str, Any]:
        """Get the service status.

        Returns:
            Status information

        Raises:
            ChatdError: If the API request fails

        """
        headers = self._get_headers()
        response = self.sync_client.get(self.base_url, headers=headers)
        self.raise_from_response(response)
        return response.json()
