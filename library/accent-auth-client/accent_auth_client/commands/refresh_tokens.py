# Copyright 2025 Accent Communications

from __future__ import annotations

import logging
from typing import Any, cast

import httpx
from accent_lib_rest_client import RESTCommand

from ..types import JSON

logger = logging.getLogger(__name__)


class RefreshTokenCommand(RESTCommand):
    """Command for refresh token operations.

    Provides methods for managing authentication refresh tokens.
    """

    resource = "tokens"

    async def list_async(self, **kwargs: Any) -> JSON:
        """List refresh tokens asynchronously.

        Args:
            **kwargs: Filter parameters

        Returns:
            JSON: List of refresh tokens

        Raises:
            AccentAPIError: If the request fails

        """
        headers = self._get_headers(**kwargs)

        r = await self.async_client.get(self.base_url, headers=headers, params=kwargs)

        try:
            r.raise_for_status()
        except httpx.HTTPStatusError:
            logger.error("Failed to list refresh tokens")
            self.raise_from_response(r)

        return cast(JSON, r.json())

    def list(self, **kwargs: Any) -> JSON:
        """List refresh tokens.

        Args:
            **kwargs: Filter parameters

        Returns:
            JSON: List of refresh tokens

        Raises:
            AccentAPIError: If the request fails

        """
        headers = self._get_headers(**kwargs)

        r = self.sync_client.get(self.base_url, headers=headers, params=kwargs)

        if r.status_code != 200:
            logger.error("Failed to list refresh tokens")
            self.raise_from_response(r)

        return cast(JSON, r.json())
