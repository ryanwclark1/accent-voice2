# Copyright 2025 Accent Communications

"""Status command module for the Configuration Daemon API."""

import logging
from typing import Any

from accent_lib_rest_client import HTTPCommand

# Configure standard logging
logger = logging.getLogger(__name__)


class StatusCommand(HTTPCommand):
    """Command for checking API status."""

    def __call__(self) -> dict[str, Any]:
        """Call the command as a function.

        Returns:
            API status

        """
        return self.get()

    async def __call_async__(self) -> dict[str, Any]:
        """Call the command as a function asynchronously.

        Returns:
            API status

        """
        return await self.get_async()

    def get(self) -> dict[str, Any]:
        """Get API status.

        Returns:
            API status

        """
        response = self.sync_client.get(self._client.url("/status"))
        response.raise_for_status()
        return response.json()

    async def get_async(self) -> dict[str, Any]:
        """Get API status asynchronously.

        Returns:
            API status

        """
        response = await self.async_client.get(self._client.url("/status"))
        response.raise_for_status()
        return response.json()
