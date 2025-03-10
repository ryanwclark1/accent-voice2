# Copyright 2025 Accent Communications

"""Sounds command module for the Configuration Daemon API."""

import logging
from typing import Any
from urllib.parse import quote

from accent_confd_client.crud import MultiTenantCommand
from accent_confd_client.util import extract_id, url_join

# Configure standard logging
logger = logging.getLogger(__name__)


class SoundsCommand(MultiTenantCommand):
    """Command for managing sounds."""

    resource = "sounds"

    def get(self, category: str, tenant_uuid: str | None = None) -> dict[str, Any]:
        """Get sounds for a category.

        Args:
            category: Sound category
            tenant_uuid: Tenant UUID

        Returns:
            Sounds data

        """
        tenant_uuid = tenant_uuid or self._client.config.tenant_uuid
        headers = dict(self.session.READ_HEADERS)
        if tenant_uuid:
            headers["Accent-Tenant"] = tenant_uuid

        url = url_join(self.resource, category)
        response = self.session.get(url, headers=headers)
        return response.json()

    async def get_async(
        self, category: str, tenant_uuid: str | None = None
    ) -> dict[str, Any]:
        """Get sounds for a category asynchronously.

        Args:
            category: Sound category
            tenant_uuid: Tenant UUID

        Returns:
            Sounds data

        """
        tenant_uuid = tenant_uuid or self._client.config.tenant_uuid
        headers = dict(self.session.READ_HEADERS)
        if tenant_uuid:
            headers["Accent-Tenant"] = tenant_uuid

        url = url_join(self.resource, category)
        response = await self.session.get_async(url, headers=headers)
        return response.json()

    def delete(self, category: str, tenant_uuid: str | None = None) -> None:
        """Delete sounds for a category.

        Args:
            category: Sound category
            tenant_uuid: Tenant UUID

        """
        tenant_uuid = tenant_uuid or self._client.config.tenant_uuid
        headers = dict(self.session.READ_HEADERS)
        if tenant_uuid:
            headers["Accent-Tenant"] = tenant_uuid

        url = url_join(self.resource, category)
        self.session.delete(url, headers=headers)

    async def delete_async(
        self, category: str, tenant_uuid: str | None = None
    ) -> None:
        """Delete sounds for a category asynchronously.

        Args:
            category: Sound category
            tenant_uuid: Tenant UUID

        """
        tenant_uuid = tenant_uuid or self._client.config.tenant_uuid
        headers = dict(self.session.READ_HEADERS)
        if tenant_uuid:
            headers["Accent-Tenant"] = tenant_uuid

        url = url_join(self.resource, category)
        await self.session.delete_async(url, headers=headers)

    @extract_id
    def download_file(self, category: str, filename: str, **kwargs: Any) -> Any:
        """Download a sound file.

        Args:
            category: Sound category
            filename: Sound filename
            **kwargs: Additional parameters

        Returns:
            Sound file content

        """
        tenant_uuid = kwargs.pop("tenant_uuid", None) or self._client.config.tenant_uuid
        headers = {"Accept": "*/*"}
        if tenant_uuid:
            headers["Accent-Tenant"] = tenant_uuid
        url = url_join(self.resource, category, "files", quote(filename, safe=""))
        response = self.session.get(url, headers=headers, params=kwargs)
        return response

    @extract_id
    async def download_file_async(
        self, category: str, filename: str, **kwargs: Any
    ) -> Any:
        """Download a sound file asynchronously.

        Args:
            category: Sound category
            filename: Sound filename
            **kwargs: Additional parameters

        Returns:
            Sound file content

        """
        tenant_uuid = kwargs.pop("tenant_uuid", None) or self._client.config.tenant_uuid
        headers = {"Accept": "*/*"}
        if tenant_uuid:
            headers["Accent-Tenant"] = tenant_uuid
        url = url_join(self.resource, category, "files", quote(filename, safe=""))
        response = await self.session.get_async(url, headers=headers, params=kwargs)
        return response

    @extract_id
    def upload_file(
        self, category: str, filename: str, content: bytes, **kwargs: Any
    ) -> None:
        """Upload a sound file.

        Args:
            category: Sound category
            filename: Sound filename
            content: Sound file content
            **kwargs: Additional parameters

        """
        tenant_uuid = kwargs.pop("tenant_uuid", None) or self._client.config.tenant_uuid
        headers = {"Content-Type": "application/octet-stream"}
        if tenant_uuid:
            headers["Accent-Tenant"] = tenant_uuid
        url = url_join(self.resource, category, "files", filename)
        self.session.put(url, raw=content, headers=headers, params=kwargs)

    @extract_id
    async def upload_file_async(
        self, category: str, filename: str, content: bytes, **kwargs: Any
    ) -> None:
        """Upload a sound file asynchronously.

        Args:
            category: Sound category
            filename: Sound filename
            content: Sound file content
            **kwargs: Additional parameters

        """
        tenant_uuid = kwargs.pop("tenant_uuid", None) or self._client.config.tenant_uuid
        headers = {"Content-Type": "application/octet-stream"}
        if tenant_uuid:
            headers["Accent-Tenant"] = tenant_uuid
        url = url_join(self.resource, category, "files", filename)
        await self.session.put_async(url, raw=content, headers=headers, params=kwargs)

    @extract_id
    def delete_file(self, category: str, filename: str, **kwargs: Any) -> None:
        """Delete a sound file.

        Args:
            category: Sound category
            filename: Sound filename
            **kwargs: Additional parameters

        """
        tenant_uuid = kwargs.pop("tenant_uuid", None) or self._client.config.tenant_uuid
        headers = {}
        if tenant_uuid:
            headers["Accent-Tenant"] = tenant_uuid
        url = url_join(self.resource, category, "files", filename)
        self.session.delete(url, headers=headers, params=kwargs)

    @extract_id
    async def delete_file_async(
        self, category: str, filename: str, **kwargs: Any
    ) -> None:
        """Delete a sound file asynchronously.

        Args:
            category: Sound category
            filename: Sound filename
            **kwargs: Additional parameters

        """
        tenant_uuid = kwargs.pop("tenant_uuid", None) or self._client.config.tenant_uuid
        headers = {}
        if tenant_uuid:
            headers["Accent-Tenant"] = tenant_uuid
        url = url_join(self.resource, category, "files", filename)
        await self.session.delete_async(url, headers=headers, params=kwargs)
