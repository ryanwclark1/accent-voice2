# Copyright 2025 Accent Communications

"""Deployd configuration commands.

This module provides commands for interacting with the Deployd configuration API.
"""

from __future__ import annotations

import logging
from typing import Any

from accent_deployd_client.command import DeploydCommand

logger = logging.getLogger(__name__)


class ConfigCommand(DeploydCommand):
    """Command for interacting with Deployd configuration.

    This command provides methods for retrieving and managing Deployd configuration.
    """

    resource = "config"

    async def get(self) -> dict[str, Any]:
        """Get the current Deployd configuration.

        Returns:
            Configuration data

        Raises:
            DeploydError: If the configuration cannot be retrieved

        """
        logger.debug("Getting Deployd configuration")
        headers = self._get_headers()
        response = await self.async_client.get(self.base_url, headers=headers)
        self.raise_from_response(response)
        return response.json()

    # For backward compatibility
    def get_sync(self) -> dict[str, Any]:
        """Get the current Deployd configuration (synchronous version).

        Returns:
            Configuration data

        Raises:
            DeploydError: If the configuration cannot be retrieved

        """
        logger.debug("Getting Deployd configuration (sync)")
        headers = self._get_headers()
        response = self.sync_client.get(self.base_url, headers=headers)
        self.raise_from_response(response)
        return response.json()
