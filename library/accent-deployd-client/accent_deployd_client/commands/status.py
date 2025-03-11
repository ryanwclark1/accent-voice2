# Copyright 2025 Accent Communications

"""Deployd status command.

This module provides a command for checking the Deployd service status.
"""

from __future__ import annotations

import logging

from accent_deployd_client.command import DeploydCommand

logger = logging.getLogger(__name__)


class StatusCommand(DeploydCommand):
    """Command for checking Deployd service status.

    This command provides methods for verifying that the Deployd service
    is available and responding to requests.
    """

    resource = "status"

    async def check(self) -> None:
        """Check if the Deployd service is available.

        Raises:
            DeploydError: If the service is unavailable

        """
        logger.debug("Checking Deployd service status")
        headers = self._get_headers()
        response = await self.async_client.head(self.base_url, headers=headers)
        if response.status_code != 200:
            self.raise_from_response(response)

    # For backward compatibility
    def check_sync(self) -> None:
        """Check if the Deployd service is available (synchronous version).

        Raises:
            DeploydError: If the service is unavailable

        """
        logger.debug("Checking Deployd service status (sync)")
        headers = self._get_headers()
        response = self.sync_client.head(self.base_url, headers=headers)
        if response.status_code != 200:
            self.raise_from_response(response)
