# Copyright 2025 Accent Communications

"""Retention commands for the accent-call-logd-client library."""

from __future__ import annotations

import logging
from typing import Any

from .helpers.base import BaseCommand

logger = logging.getLogger(__name__)


class RetentionCommand(BaseCommand):
    """Command for retention policy operations."""

    async def get_async(self, tenant_uuid: str | None = None) -> dict[str, Any]:
        """Get retention policy asynchronously.

        Args:
            tenant_uuid: Optional tenant identifier

        Returns:
            Retention policy data

        """
        headers = self._get_headers(tenant_uuid=tenant_uuid)
        url = self._client.url("retention")
        logger.debug("Fetching retention policy")

        r = await self.async_client.get(url, headers=headers)
        self.raise_from_response(r)
        return r.json()

    def get(self, tenant_uuid: str | None = None) -> dict[str, Any]:
        """Get retention policy.

        Args:
            tenant_uuid: Optional tenant identifier

        Returns:
            Retention policy data

        """
        headers = self._get_headers(tenant_uuid=tenant_uuid)
        url = self._client.url("retention")
        logger.debug("Fetching retention policy")

        r = self.sync_client.get(url, headers=headers)
        self.raise_from_response(r)
        return r.json()

    async def update_async(
        self, tenant_uuid: str | None = None, **body: Any
    ) -> None:
        """Update retention policy asynchronously.

        Args:
            tenant_uuid: Optional tenant identifier
            **body: Policy update parameters

        """
        headers = self._get_headers(tenant_uuid=tenant_uuid)
        url = self._client.url("retention")
        logger.debug("Updating retention policy")

        r = await self.async_client.put(url, json=body, headers=headers)
        self.raise_from_response(r)

    def update(self, tenant_uuid: str | None = None, **body: Any) -> None:
        """Update retention policy.

        Args:
            tenant_uuid: Optional tenant identifier
            **body: Policy update parameters

        """
        headers = self._get_headers(tenant_uuid=tenant_uuid)
        url = self._client.url("retention")
        logger.debug("Updating retention policy")

        r = self.sync_client.put(url, json=body, headers=headers)
        self.raise_from_response(r)
