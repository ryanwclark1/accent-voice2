# Copyright 2025 Accent Communications

"""Commands for status management in the Calld API.

This module provides commands for retrieving the Calld service status.
"""

from __future__ import annotations

import logging
from typing import Any

from accent_calld_client.command import CalldCommand

logger = logging.getLogger(__name__)


class StatusCommand(CalldCommand):
    """Command for retrieving Calld service status.

    This command provides methods for checking the current status of the service.
    """

    resource = "status"

    async def get_async(self) -> dict[str, Any]:
        """Get the current service status asynchronously.

        Returns:
            Status data as a dictionary

        Raises:
            CalldError: If the API returns an error

        """
        headers = self._get_headers()
        url = self.base_url
        r = await self.async_client.get(url, headers=headers)
        self.raise_from_response(r)
        return r.json()

    def get(self) -> dict[str, Any]:
        """Get the current service status.

        Returns:
            Status data as a dictionary

        Raises:
            CalldError: If the API returns an error

        """
        headers = self._get_headers()
        url = self.base_url
        r = self.sync_client.get(url, headers=headers)
        self.raise_from_response(r)
        return r.json()
