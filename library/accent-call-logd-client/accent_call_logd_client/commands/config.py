# Copyright 2025 Accent Communications

"""Configuration commands for the accent-call-logd-client library."""

from __future__ import annotations

import logging
from typing import Any

from .helpers.base import BaseCommand

logger = logging.getLogger(__name__)


class ConfigCommand(BaseCommand):
    """Command for configuration operations."""

    async def get_async(self) -> dict[str, Any]:
        """Get configuration asynchronously.

        Returns:
            Configuration data

        """
        headers = self._get_headers()
        url = self._client.url("config")
        logger.debug("Fetching configuration")

        r = await self.async_client.get(url, headers=headers)
        self.raise_from_response(r)
        return r.json()

    def get(self) -> dict[str, Any]:
        """Get configuration.

        Returns:
            Configuration data

        """
        headers = self._get_headers()
        url = self._client.url("config")
        logger.debug("Fetching configuration")

        r = self.sync_client.get(url, headers=headers)
        self.raise_from_response(r)
        return r.json()

    async def patch_async(self, config_patch: dict[str, Any]) -> dict[str, Any]:
        """Update configuration partially asynchronously.

        Args:
            config_patch: Configuration changes

        Returns:
            Updated configuration

        """
        headers = self._get_headers()
        url = self._client.url("config")
        logger.debug("Patching configuration")

        r = await self.async_client.patch(url, headers=headers, json=config_patch)
        self.raise_from_response(r)
        return r.json()

    def patch(self, config_patch: dict[str, Any]) -> dict[str, Any]:
        """Update configuration partially.

        Args:
            config_patch: Configuration changes

        Returns:
            Updated configuration

        """
        headers = self._get_headers()
        url = self._client.url("config")
        logger.debug("Patching configuration")

        r = self.sync_client.patch(url, headers=headers, json=config_patch)
        self.raise_from_response(r)
        return r.json()
