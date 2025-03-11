# Copyright 2025 Accent Communications

"""Commands for phone line management in the Calld API.

This module provides commands for listing and managing phone lines.
"""

from __future__ import annotations

import logging
from typing import Any

from accent_calld_client.command import CalldCommand

logger = logging.getLogger(__name__)


class LinesCommand(CalldCommand):
    """Command for managing phone lines.

    This command provides methods for listing and retrieving phone line information.
    """

    resource = "lines"

    async def list_lines_async(
        self, tenant_uuid: str | None = None
    ) -> dict[str, Any]:
        """List all phone lines asynchronously.

        Args:
            tenant_uuid: Optional tenant UUID

        Returns:
            Dictionary containing line information

        Raises:
            CalldError: If the API returns an error

        """
        headers = self._get_headers(tenant_uuid=tenant_uuid)
        url = self._client.url(self.resource)

        r = await self.async_client.get(url, headers=headers)
        if r.status_code != 200:
            self.raise_from_response(r)

        return r.json()

    def list_lines(self, tenant_uuid: str | None = None) -> dict[str, Any]:
        """List all phone lines.

        Args:
            tenant_uuid: Optional tenant UUID

        Returns:
            Dictionary containing line information

        Raises:
            CalldError: If the API returns an error

        """
        headers = self._get_headers(tenant_uuid=tenant_uuid)
        url = self._client.url(self.resource)

        r = self.sync_client.get(url, headers=headers)
        if r.status_code != 200:
            self.raise_from_response(r)

        return r.json()
