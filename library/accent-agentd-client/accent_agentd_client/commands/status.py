# Copyright 2025 Accent Communications

"""Service status command for the Accent Agent Daemon client."""

from __future__ import annotations

import logging
from typing import Any

from accent_lib_rest_client.command import RESTCommand

from accent_agentd_client.helpers import ResponseProcessor

# Configure logging
logger = logging.getLogger(__name__)


class StatusCommand(RESTCommand):
    """Command for getting service status."""

    resource = "status"

    def __call__(self) -> dict[str, Any]:
        """Call the command as a function to get service status.

        Returns:
            Status information

        Raises:
            AgentdClientError: If the operation fails

        """
        logger.info("Getting service status")

        _resp_processor = ResponseProcessor()
        headers = self._get_headers()
        url = self.base_url

        resp = self.sync_client.get(url, headers=headers)

        if resp.status_code != 200:
            _resp_processor.generic(resp)

        return resp.json()

    async def __call_async__(self) -> dict[str, Any]:
        """Call the command as a function to get service status asynchronously.

        Returns:
            Status information

        Raises:
            AgentdClientError: If the operation fails

        """
        logger.info("Getting service status (async)")

        _resp_processor = ResponseProcessor()
        headers = self._get_headers()
        url = self.base_url

        resp = await self.async_client.get(url, headers=headers)

        if resp.status_code != 200:
            await _resp_processor.generic_async(resp)

        return resp.json()
