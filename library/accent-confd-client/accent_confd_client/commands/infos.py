# Copyright 2025 Accent Communications

"""Info command module for the Configuration Daemon API."""

import logging
from typing import Any

from accent_lib_rest_client import HTTPCommand

# Configure standard logging
logger = logging.getLogger(__name__)


class InfosCommand(HTTPCommand):
    """Command for retrieving system information."""

    def __call__(self) -> dict[str, Any]:
        """Call the command as a function.

        Returns:
            System information

        """
        return self.get()

    async def __call_async__(self) -> dict[str, Any]:
        """Call the command as a function asynchronously.

        Returns:
            System information

        """
        return await self.get_async()

    def get(self) -> dict[str, Any]:
        """Get system information.

        Returns:
            System information

        """
        response = self.sync_client.get(self._client.url("infos"))
        response.raise_for_status()
        return response.json()

    async def get_async(self) -> dict[str, Any]:
        """Get system information asynchronously.

        Returns:
            System information

        """
        response = await self.async_client.get(self._client.url("infos"))
        response.raise_for_status()
        return response.json()
