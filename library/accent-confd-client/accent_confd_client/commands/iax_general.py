# Copyright 2025 Accent Communications

"""IAX general command module for the Configuration Daemon API."""

import logging
from typing import Any

from accent_lib_rest_client import RESTCommand

# Configure standard logging
logger = logging.getLogger(__name__)


class IAXGeneralCommand(RESTCommand):
    """Command for managing IAX general settings."""

    resource = "asterisk/iax/general"

    def get(self) -> dict[str, Any]:
        """Get IAX general settings.

        Returns:
            IAX general settings

        """
        response = self.sync_client.get(self.base_url)
        response.raise_for_status()
        return response.json()

    async def get_async(self) -> dict[str, Any]:
        """Get IAX general settings asynchronously.

        Returns:
            IAX general settings

        """
        response = await self.async_client.get(self.base_url)
        response.raise_for_status()
        return response.json()

    def update(self, body: dict[str, Any]) -> None:
        """Update IAX general settings.

        Args:
            body: IAX general settings

        """
        response = self.sync_client.put(self.base_url, json=body)
        response.raise_for_status()

    async def update_async(self, body: dict[str, Any]) -> None:
        """Update IAX general settings asynchronously.

        Args:
            body: IAX general settings

        """
        response = await self.async_client.put(self.base_url, json=body)
        response.raise_for_status()
