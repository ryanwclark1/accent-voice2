# Copyright 2025 Accent Communications

"""Configuration commands for Setupd client."""

from __future__ import annotations

import logging
from typing import Any

from accent_setupd_client.command import SetupdCommand

logger = logging.getLogger(__name__)


class ConfigCommand(SetupdCommand):
    """Command for interacting with configuration endpoints."""

    resource = "config"

    async def get_async(self, tenant_uuid: str | None = None) -> dict[str, Any]:
        """Get the current configuration asynchronously.

        Args:
            tenant_uuid: Optional tenant identifier

        Returns:
            Configuration data as a dictionary

        """
        headers = self._get_headers(tenant_uuid=tenant_uuid)
        logger.debug("Fetching config for tenant: %s", tenant_uuid or "default")

        start_time = logger.isEnabledFor(logging.DEBUG) and time.time()

        response = await self.async_client.get(self.base_url, headers=headers)
        self.raise_from_response(response)

        if start_time:
            logger.debug("Config retrieved in %.2fs", time.time() - start_time)

        return response.json()

    def get(self, tenant_uuid: str | None = None) -> dict[str, Any]:
        """Get the current configuration.

        Args:
            tenant_uuid: Optional tenant identifier

        Returns:
            Configuration data as a dictionary

        """
        headers = self._get_headers(tenant_uuid=tenant_uuid)
        logger.debug("Fetching config for tenant: %s", tenant_uuid or "default")

        start_time = logger.isEnabledFor(logging.DEBUG) and time.time()

        response = self.sync_client.get(self.base_url, headers=headers)
        self.raise_from_response(response)

        if start_time:
            logger.debug("Config retrieved in %.2fs", time.time() - start_time)

        return response.json()
