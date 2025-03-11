# Copyright 2025 Accent Communications

"""Commands for trunk management in the Calld API.

This module provides commands for listing and retrieving trunk information.
"""

from __future__ import annotations

import logging
from typing import Any

from accent_calld_client.command import CalldCommand

logger = logging.getLogger(__name__)


class TrunksCommand(CalldCommand):
    """Command for managing trunks.

    This command provides methods for listing and retrieving trunk information.
    """

    resource = "trunks"

    async def list_trunks_async(
        self, tenant_uuid: str | None = None
    ) -> dict[str, Any]:
        """List all trunks asynchronously.

        Args:
            tenant_uuid: Optional tenant UUID

        Returns:
            Dictionary containing trunk information

        Raises:
            CalldError: If the API returns an error

        """
        headers = self._get_headers(tenant_uuid=tenant_uuid)
        url = self._client.url(self.resource)
        r = await self.async_client.get(url, headers=headers)
        if r.status_code != 200:
            self.raise_from_response(r)

        return r.json()

    def list_trunks(self, tenant_uuid: str | None = None) -> dict[str, Any]:
        """List all trunks.

        Args:
            tenant_uuid: Optional tenant UUID

        Returns:
            Dictionary containing trunk information

        Raises:
            CalldError: If the API returns an error

        """
        headers = self._get_headers(tenant_uuid=tenant_uuid)
        url = self._client.url(self.resource)
        r = self.sync_client.get(url, headers=headers)
        if r.status_code != 200:
            self.raise_from_response(r)

        return r.json()
