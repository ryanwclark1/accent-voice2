# Copyright 2025 Accent Communications

"""Sound languages command module for the Configuration Daemon API."""

import logging
from typing import Any

from accent_lib_rest_client import RESTCommand

from accent_confd_client.util import url_join

# Configure standard logging
logger = logging.getLogger(__name__)


class SoundsLanguagesCommand(RESTCommand):
    """Command for managing sound languages."""

    resource = "sounds/languages"

    def list(self) -> dict[str, Any]:
        """List available sound languages.

        Returns:
            Available sound languages

        """
        url = url_join(self.resource)
        response = self.sync_client.get(url)
        response.raise_for_status()
        return response.json()

    async def list_async(self) -> dict[str, Any]:
        """List available sound languages asynchronously.

        Returns:
            Available sound languages

        """
        url = url_join(self.resource)
        response = await self.async_client.get(url)
        response.raise_for_status()
        return response.json()
