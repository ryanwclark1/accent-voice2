# Copyright 2025 Accent Communications

from __future__ import annotations

import logging
from functools import lru_cache
from typing import cast

import httpx
from accent_lib_rest_client import RESTCommand

from accent_auth_client.type_definitions import JSON

logger = logging.getLogger(__name__)


class ConfigCommand(RESTCommand):
    """Command for configuration-related operations.

    Provides methods for getting and updating configuration settings.
    """

    resource = "config"

    @lru_cache(maxsize=16)
    async def get_async(self) -> JSON:
        """Get configuration asynchronously.

        Returns:
            JSON: Configuration data

        Raises:
            AccentAPIError: If the request fails
        """
        headers = self._get_headers()

        r = await self.async_client.get(self.base_url, headers=headers)

        try:
            r.raise_for_status()
        except httpx.HTTPStatusError:
            logger.error("Failed to get configuration")
            self.raise_from_response(r)

        return cast(JSON, r.json())

    @lru_cache(maxsize=16)
    def get(self) -> JSON:
        """Get configuration.

        Returns:
            JSON: Configuration data

        Raises:
            AccentAPIError: If the request fails
        """
        headers = self._get_headers()

        r = self.sync_client.get(self.base_url, headers=headers)

        if r.status_code != 200:
            logger.error("Failed to get configuration")
            self.raise_from_response(r)

        return cast(JSON, r.json())

    async def patch_async(self, config_patch: dict[str, JSON]) -> JSON:
        """Patch configuration asynchronously.

        Args:
            config_patch: Configuration patch

        Returns:
            JSON: Updated configuration

        Raises:
            AccentAPIError: If the request fails
        """
        headers = self._get_headers()

        r = await self.async_client.patch(
            self.base_url, headers=headers, json=config_patch
        )

        try:
            r.raise_for_status()
        except httpx.HTTPStatusError:
            logger.error("Failed to patch configuration")
            self.raise_from_response(r)

        # Invalidate cache when config changes
        self.get_async.cache_clear()
        self.get.cache_clear()

        return cast(JSON, r.json())

    def patch(self, config_patch: dict[str, JSON]) -> JSON:
        """Patch configuration.

        Args:
            config_patch: Configuration patch

        Returns:
            JSON: Updated configuration

        Raises:
            AccentAPIError: If the request fails
        """
        headers = self._get_headers()

        r = self.sync_client.patch(self.base_url, headers=headers, json=config_patch)

        if r.status_code != 200:
            logger.error("Failed to patch configuration")
            self.raise_from_response(r)

        # Invalidate cache when config changes
        self.get_async.cache_clear()
        self.get.cache_clear()

        return cast(JSON, r.json())
