# Copyright 2025 Accent Communications

"""Commands for status checking."""

from __future__ import annotations

import logging
from typing import Any

from accent_provd_client.command import ProvdCommand

logger = logging.getLogger(__name__)


class StatusCommand(ProvdCommand):
    """Commands for checking service status.

    Provides methods for checking the status of the provisioning service.
    """

    resource = "status"
    _headers = {"Content-Type": "application/vnd.accent.provd+json"}

    async def get_async(self) -> dict[str, Any]:
        """Get service status asynchronously.

        Returns:
            Status information

        Raises:
            ProvdError: If the request fails

        """
        r = await self.async_client.get(self.base_url, headers=self._headers)
        self.raise_from_response(r)
        return r.json()

    def get(self) -> dict[str, Any]:
        """Get service status.

        Returns:
            Status information

        Raises:
            ProvdError: If the request fails

        """
        r = self.sync_client.get(self.base_url, headers=self._headers)
        self.raise_from_response(r)
        return r.json()
