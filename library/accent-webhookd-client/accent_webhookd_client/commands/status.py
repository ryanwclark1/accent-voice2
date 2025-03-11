# Copyright 2025 Accent Communications

"""Commands for checking Webhookd service status.

This module provides commands for retrieving the status and
health information of the Webhookd service.
"""

from __future__ import annotations

import logging
from functools import lru_cache

from accent_webhookd_client.command import WebhookdCommand
from accent_webhookd_client.models import StatusResponse

# Configure logging
logger = logging.getLogger(__name__)


class StatusCommand(WebhookdCommand):
    """Command for checking Webhookd service status.

    This command allows retrieving status and health information
    of the Webhookd service.
    """

    resource = "status"

    @lru_cache(maxsize=32)
    def get(self) -> StatusResponse:
        """Get the current service status.

        Returns:
            Current status information

        Raises:
            WebhookdError: If the request fails

        """
        logger.debug("Getting Webhookd status")
        headers = self._get_headers()
        r = self._sync_request("get", self.base_url, headers=headers)
        self.raise_from_response(r)
        return StatusResponse.model_validate(r.json())

    async def get_async(self) -> StatusResponse:
        """Get the current service status asynchronously.

        Returns:
            Current status information

        Raises:
            WebhookdError: If the request fails

        """
        logger.debug("Getting Webhookd status (async)")
        headers = self._get_headers()
        r = await self._async_request("get", self.base_url, headers=headers)
        self.raise_from_response(r)
        return StatusResponse.model_validate(r.json())
