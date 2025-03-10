# Copyright 2025 Accent Communications

"""IAX call number limits command module for the Configuration Daemon API."""

import logging
from typing import Any

from accent_lib_rest_client import RESTCommand

# Configure standard logging
logger = logging.getLogger(__name__)


class IAXCallNumberLimitsCommand(RESTCommand):
    """Command for managing IAX call number limits."""

    resource = "asterisk/iax/callnumberlimits"

    def get(self) -> dict[str, Any]:
        """Get IAX call number limits.

        Returns:
            IAX call number limits

        """
        response = self.sync_client.get(self.base_url)
        response.raise_for_status()
        return response.json()

    async def get_async(self) -> dict[str, Any]:
        """Get IAX call number limits asynchronously.

        Returns:
            IAX call number limits

        """
        response = await self.async_client.get(self.base_url)
        response.raise_for_status()
        return response.json()

    def update(self, body: dict[str, Any]) -> None:
        """Update IAX call number limits.

        Args:
            body: IAX call number limits

        """
        response = self.sync_client.put(self.base_url, json=body)
        response.raise_for_status()

    async def update_async(self, body: dict[str, Any]) -> None:
        """Update IAX call number limits asynchronously.

        Args:
            body: IAX call number limits

        """
        response = await self.async_client.put(self.base_url, json=body)
        response.raise_for_status()
