# Copyright 2025 Accent Communications

"""Status commands for AMID API.

This module defines the commands for checking AMID status.
"""

from __future__ import annotations

import logging

from accent_amid_client.command import AmidCommand
from accent_amid_client.models import JSON

logger = logging.getLogger(__name__)


class StatusCommand(AmidCommand):
    """Command for checking AMID status."""

    resource = "status"

    def __call__(self) -> JSON:
        """Get the current AMID status synchronously.

        Returns:
            Current status

        Raises:
            AmidError: If the server returns an error response

        """
        logger.info("Getting AMID status")
        headers = self._get_headers()
        url = self.base_url

        r = self.sync_client.get(url, headers=headers)

        if r.status_code != 200:
            self.raise_from_response(r)

        return r.json()

    async def async_call(self) -> JSON:
        """Get the current AMID status asynchronously.

        Returns:
            Current status

        Raises:
            AmidError: If the server returns an error response

        """
        logger.info("Async getting AMID status")
        headers = self._get_headers()
        url = self.base_url

        r = await self.async_client.get(url, headers=headers)

        if r.status_code != 200:
            self.raise_from_response(r)

        return r.json()
