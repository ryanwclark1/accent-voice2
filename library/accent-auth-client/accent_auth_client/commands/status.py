# Copyright 2025 Accent Communications

from __future__ import annotations

import logging

import httpx
from accent_lib_rest_client import RESTCommand

logger = logging.getLogger(__name__)


class StatusCommand(RESTCommand):
    """Command for status-related operations.

    Provides methods for checking the API status.
    """

    resource = "status"

    async def check_async(self) -> None:
        """Check API status asynchronously.

        Raises:
            AccentAPIError: If the API is not available

        """
        headers = self._get_headers()

        r = await self.async_client.head(self.base_url, headers=headers)

        try:
            r.raise_for_status()
        except httpx.HTTPStatusError as e:
            if r.status_code != 200:
                logger.error(
                    "API status check failed: %s, status code: %s",
                    str(e),
                    r.status_code,
                )
                self.raise_from_response(r)

    def check(self) -> None:
        """Check API status.

        Raises:
            AccentAPIError: If the API is not available

        """
        headers = self._get_headers()

        r = self.sync_client.head(self.base_url, headers=headers)

        if r.status_code != 200:
            logger.error("API status check failed: status code %s", r.status_code)
            self.raise_from_response(r)
