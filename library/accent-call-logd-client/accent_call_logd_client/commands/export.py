# Copyright 2025 Accent Communications

"""Export commands for the accent-call-logd-client library."""

from __future__ import annotations

import logging
from typing import Any

import httpx

from .helpers.base import BaseCommand

logger = logging.getLogger(__name__)


class ExportCommand(BaseCommand):
    """Command for export operations."""

    async def get_async(
        self, export_uuid: str, tenant_uuid: str | None = None
    ) -> dict[str, Any]:
        """Get export information asynchronously.

        Args:
            export_uuid: The export identifier
            tenant_uuid: Optional tenant identifier

        Returns:
            Export information

        """
        headers = self._get_headers(tenant_uuid=tenant_uuid)
        url = self._client.url("exports", export_uuid)
        logger.debug("Fetching export: %s", export_uuid)

        r = await self.async_client.get(url, headers=headers)
        self.raise_from_response(r)
        return r.json()

    def get(
        self, export_uuid: str, tenant_uuid: str | None = None
    ) -> dict[str, Any]:
        """Get export information.

        Args:
            export_uuid: The export identifier
            tenant_uuid: Optional tenant identifier

        Returns:
            Export information

        """
        headers = self._get_headers(tenant_uuid=tenant_uuid)
        url = self._client.url("exports", export_uuid)
        logger.debug("Fetching export: %s", export_uuid)

        r = self.sync_client.get(url, headers=headers)
        self.raise_from_response(r)
        return r.json()

    async def download_async(
        self, export_uuid: str, tenant_uuid: str | None = None
    ) -> httpx.Response:
        """Download export data asynchronously.

        Args:
            export_uuid: The export identifier
            tenant_uuid: Optional tenant identifier

        Returns:
            HTTP response with export data

        """
        headers = self._get_headers(write=True, tenant_uuid=tenant_uuid)
        url = self._client.url("exports", export_uuid, "download")
        logger.debug("Downloading export: %s", export_uuid)

        r = await self.async_client.get(url, headers=headers)
        self.raise_from_response(r)
        return r

    def download(
        self, export_uuid: str, tenant_uuid: str | None = None
    ) -> httpx.Response:
        """Download export data.

        Args:
            export_uuid: The export identifier
            tenant_uuid: Optional tenant identifier

        Returns:
            HTTP response with export data

        """
        headers = self._get_headers(write=True, tenant_uuid=tenant_uuid)
        url = self._client.url("exports", export_uuid, "download")
        logger.debug("Downloading export: %s", export_uuid)

        r = self.sync_client.get(url, headers=headers)
        self.raise_from_response(r)
        return r
