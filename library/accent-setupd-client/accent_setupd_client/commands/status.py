# Copyright 2025 Accent Communications

"""Status commands for Setupd client."""

from __future__ import annotations

import logging
import time
from typing import Any

from accent_setupd_client.command import SetupdCommand

logger = logging.getLogger(__name__)


class StatusCommand(SetupdCommand):
    """Command for checking setup status."""

    resource = "status"

    async def get_async(self, tenant_uuid: str | None = None) -> dict[str, Any]:
        """Get the current setup status asynchronously.

        Args:
            tenant_uuid: Optional tenant identifier

        Returns:
            Status data as a dictionary

        """
        headers = self._get_headers(tenant_uuid=tenant_uuid)
        logger.debug("Fetching status for tenant: %s", tenant_uuid or "default")

        start_time = logger.isEnabledFor(logging.DEBUG) and time.time()

        response = await self.async_client.get(self.base_url, headers=headers)
        self.raise_from_response(response)

        if start_time:
            logger.debug("Status retrieved in %.2fs", time.time() - start_time)

        return response.json()

    def get(self, tenant_uuid: str | None = None) -> dict[str, Any]:
        """Get the current setup status.

        Args:
            tenant_uuid: Optional tenant identifier

        Returns:
            Status data as a dictionary

        """
        headers = self._get_headers(tenant_uuid=tenant_uuid)
        logger.debug("Fetching status for tenant: %s", tenant_uuid or "default")

        start_time = logger.isEnabledFor(logging.DEBUG) and time.time()

        response = self.sync_client.get(self.base_url, headers=headers)
        self.raise_from_response(response)

        if start_time:
            logger.debug("Status retrieved in %.2fs", time.time() - start_time)

        return response.json()
