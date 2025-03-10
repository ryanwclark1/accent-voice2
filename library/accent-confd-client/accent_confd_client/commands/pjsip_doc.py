# Copyright 2025 Accent Communications

"""PJSIP documentation command module for the Configuration Daemon API."""

import logging
from typing import Any

from accent_lib_rest_client import RESTCommand

# Configure standard logging
logger = logging.getLogger(__name__)


class PJSIPDocCommand(RESTCommand):
    """Command for retrieving PJSIP documentation."""

    resource = "asterisk/pjsip/doc"

    def get(self) -> dict[str, Any]:
        """Get PJSIP documentation.

        Returns:
            PJSIP documentation data

        """
        response = self.sync_client.get(self.base_url)
        response.raise_for_status()
        return response.json()

    async def get_async(self) -> dict[str, Any]:
        """Get PJSIP documentation asynchronously.

        Args:

        Returns:
            PJSIP documentation data

        """
        response = await self.async_client.get(self.base_url)
        response.raise_for_status()
        return response.json()
