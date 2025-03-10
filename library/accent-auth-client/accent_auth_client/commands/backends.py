# Copyright 2025 Accent Communications

from __future__ import annotations

import logging
from typing import cast

import httpx
from accent_lib_rest_client import RESTCommand

from ..types import JSON

logger = logging.getLogger(__name__)


class BackendsCommand(RESTCommand):
    """Command for authentication backends operations.

    Provides methods for managing authentication backends.
    """

    resource = "backends"

    async def list_async(self) -> JSON:
        """List authentication backends asynchronously.

        Returns:
            JSON: List of authentication backends

        Raises:
            AccentAPIError: If the request fails

        """
        headers = self._get_headers()

        r = await self.async_client.get(self.base_url, headers=headers)

        try:
            r.raise_for_status()
        except httpx.HTTPStatusError:
            logger.error("Failed to list backends")
            self.raise_from_response(r)

        return cast(JSON, r.json()["data"])

    def list(self) -> JSON:
        """List authentication backends.

        Returns:
            JSON: List of authentication backends

        Raises:
            AccentAPIError: If the request fails

        """
        headers = self._get_headers()

        r = self.sync_client.get(self.base_url, headers=headers)

        if r.status_code != 200:
            logger.error("Failed to list backends")
            self.raise_from_response(r)

        return cast(JSON, r.json()["data"])
