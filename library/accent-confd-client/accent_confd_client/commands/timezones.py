# Copyright 2025 Accent Communications

"""Timezones command module for the Configuration Daemon API."""

import logging
from typing import Any

from accent_lib_rest_client import RESTCommand

from accent_confd_client.util import url_join

# Configure standard logging
logger = logging.getLogger(__name__)


class TimezonesCommand(RESTCommand):
    """Command for managing timezones."""

    resource = "timezones"

    def list(self) -> dict[str, Any]:
        """List available timezones.

        Returns:
            Available timezones

        """
        url = url_join(self.resource)
        response = self.sync_client.get(url)
        response.raise_for_status()
        return response.json()

    async def list_async(self) -> dict[str, Any]:
        """List available timezones asynchronously.

        Returns:
            Available timezones

        """
        url = url_join(self.resource)
        response = await self.async_client.get(url)
        response.raise_for_status()
        return response.json()
