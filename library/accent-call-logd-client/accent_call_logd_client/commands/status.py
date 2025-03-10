# Copyright 2025 Accent Communications

"""Status commands for the accent-call-logd-client library."""

from __future__ import annotations

import logging
from typing import Any

from .helpers.base import BaseCommand

logger = logging.getLogger(__name__)


class StatusCommand(BaseCommand):
    """Command for service status operations."""

    async def get_async(self) -> dict[str, Any]:
        """Get service status asynchronously.

        Returns:
            Status information

        """
        headers = self._get_headers()
        url = self._client.url("status")
        logger.debug("Fetching service status")

        r = await self.async_client.get(url, headers=headers)
        self.raise_from_response(r)
        return r.json()

    def get(self) -> dict[str, Any]:
        """Get service status.

        Returns:
            Status information

        """
        headers = self._get_headers()
        url = self._client.url("status")
        logger.debug("Fetching service status")

        r = self.sync_client.get(url, headers=headers)
        self.raise_from_response(r)
        return r.json()
