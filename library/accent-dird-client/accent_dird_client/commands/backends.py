# Copyright 2025 Accent Communications

"""Backend command implementation."""

import builtins
import logging
from typing import Any

from accent_lib_rest_client.models import JSONResponse

from accent_dird_client.commands.helpers.base_command import DirdRESTCommand

logger = logging.getLogger(__name__)


class BackendsCommand(DirdRESTCommand):
    """Command for backend operations."""

    resource = "backends"

    async def create_source_async(
        self,
        backend: str,
        body: dict[str, Any],
        tenant_uuid: str | None = None,
        token: str | None = None,
    ) -> JSONResponse:
        """Create a source for a backend asynchronously.

        Args:
            backend: Backend identifier
            body: Source configuration
            tenant_uuid: Optional tenant UUID
            token: Optional authentication token

        Returns:
            Created source details

        """
        url = self._build_base_url(backend)
        headers = self.build_headers(tenant_uuid, token)
        response = await self.async_client.post(url, headers=headers, json=body)
        self.raise_from_response(response)
        return self.process_json_response(response)

    def create_source(
        self,
        backend: str,
        body: dict[str, Any],
        tenant_uuid: str | None = None,
        token: str | None = None,
    ) -> dict[str, Any]:
        """Create a source for a backend.

        Args:
            backend: Backend identifier
            body: Source configuration
            tenant_uuid: Optional tenant UUID
            token: Optional authentication token

        Returns:
            Created source details

        """
        url = self._build_base_url(backend)
        headers = self.build_headers(tenant_uuid, token)
        response = self.sync_client.post(url, headers=headers, json=body)
        self.raise_from_response(response)
        return response.json()

    async def delete_source_async(
        self,
        backend: str,
        source_uuid: str,
        tenant_uuid: str | None = None,
        token: str | None = None,
    ) -> None:
        """Delete a source from a backend asynchronously.

        Args:
            backend: Backend identifier
            source_uuid: Source UUID to delete
            tenant_uuid: Optional tenant UUID
            token: Optional authentication token

        """
        url = self._build_url(backend, source_uuid)
        headers = self.build_headers(tenant_uuid, token)
        response = await self.async_client.delete(url, headers=headers)
        self.raise_from_response(response)

    def delete_source(
        self,
        backend: str,
        source_uuid: str,
        tenant_uuid: str | None = None,
        token: str | None = None,
    ) -> None:
        """Delete a source from a backend.

        Args:
            backend: Backend identifier
            source_uuid: Source UUID to delete
            tenant_uuid: Optional tenant UUID
            token: Optional authentication token

        """
        url = self._build_url(backend, source_uuid)
        headers = self.build_headers(tenant_uuid, token)
        response = self.sync_client.delete(url, headers=headers)
        self.raise_from_response(response)

    async def edit_source_async(
        self,
        backend: str,
        source_uuid: str,
        body: dict[str, Any],
        tenant_uuid: str | None = None,
        token: str | None = None,
    ) -> None:
        """Edit a source in a backend asynchronously.

        Args:
            backend: Backend identifier
            source_uuid: Source UUID to edit
            body: Updated source configuration
            tenant_uuid: Optional tenant UUID
            token: Optional authentication token

        """
        url = self._build_url(backend, source_uuid)
        headers = self.build_headers(tenant_uuid, token)
        response = await self.async_client.put(url, headers=headers, json=body)
        self.raise_from_response(response)

    def edit_source(
        self,
        backend: str,
        source_uuid: str,
        body: dict[str, Any],
        tenant_uuid: str | None = None,
        token: str | None = None,
    ) -> None:
        """Edit a source in a backend.

        Args:
            backend: Backend identifier
            source_uuid: Source UUID to edit
            body: Updated source configuration
            tenant_uuid: Optional tenant UUID
            token: Optional authentication token

        """
        url = self._build_url(backend, source_uuid)
        headers = self.build_headers(tenant_uuid, token)
        response = self.sync_client.put(url, headers=headers, json=body)
        self.raise_from_response(response)

    async def get_source_async(
        self,
        backend: str,
        source_uuid: str,
        tenant_uuid: str | None = None,
        token: str | None = None,
    ) -> JSONResponse:
        """Get a source from a backend asynchronously.

        Args:
            backend: Backend identifier
            source_uuid: Source UUID to retrieve
            tenant_uuid: Optional tenant UUID
            token: Optional authentication token

        Returns:
            Source details

        """
        url = self._build_url(backend, source_uuid)
        headers = self.build_headers(tenant_uuid, token)
        response = await self.async_client.get(url, headers=headers)
        self.raise_from_response(response)
        return self.process_json_response(response)

    def get_source(
        self,
        backend: str,
        source_uuid: str,
        tenant_uuid: str | None = None,
        token: str | None = None,
    ) -> dict[str, Any]:
        """Get a source from a backend.

        Args:
            backend: Backend identifier
            source_uuid: Source UUID to retrieve
            tenant_uuid: Optional tenant UUID
            token: Optional authentication token

        Returns:
            Source details

        """
        url = self._build_url(backend, source_uuid)
        headers = self.build_headers(tenant_uuid, token)
        response = self.sync_client.get(url, headers=headers)
        self.raise_from_response(response)
        return response.json()

    async def list_async(
        self,
        token: str | None = None,
        tenant_uuid: str | None = None,
        **kwargs: Any,
    ) -> JSONResponse:
        """List backends asynchronously.

        Args:
            token: Optional authentication token
            tenant_uuid: Optional tenant UUID
            **kwargs: Additional query parameters

        Returns:
            List of backends

        """
        headers = self.build_headers(tenant_uuid, token)
        response = await self.async_client.get(
            self.base_url, params=kwargs, headers=headers
        )
        self.raise_from_response(response)
        return self.process_json_response(response)

    def list(
        self,
        token: str | None = None,
        tenant_uuid: str | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """List backends.

        Args:
            token: Optional authentication token
            tenant_uuid: Optional tenant UUID
            **kwargs: Additional query parameters

        Returns:
            List of backends

        """
        headers = self.build_headers(tenant_uuid, token)
        response = self.sync_client.get(self.base_url, params=kwargs, headers=headers)
        self.raise_from_response(response)
        return response.json()

    async def list_sources_async(
        self,
        backend: str,
        tenant_uuid: str | None = None,
        token: str | None = None,
        **kwargs: Any,
    ) -> JSONResponse:
        """List sources for a backend asynchronously.

        Args:
            backend: Backend identifier
            tenant_uuid: Optional tenant UUID
            token: Optional authentication token
            **kwargs: Additional query parameters

        Returns:
            List of sources

        """
        url = self._build_base_url(backend)
        headers = self.build_headers(tenant_uuid, token)
        response = await self.async_client.get(url, headers=headers, params=kwargs)
        self.raise_from_response(response)
        return self.process_json_response(response)

    def list_sources(
        self,
        backend: str,
        tenant_uuid: str | None = None,
        token: str | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """List sources for a backend.

        Args:
            backend: Backend identifier
            tenant_uuid: Optional tenant UUID
            token: Optional authentication token
            **kwargs: Additional query parameters

        Returns:
            List of sources

        """
        url = self._build_base_url(backend)
        headers = self.build_headers(tenant_uuid, token)
        response = self.sync_client.get(url, headers=headers, params=kwargs)
        self.raise_from_response(response)
        return response.json()

    async def list_contacts_from_source_async(
        self,
        backend: str,
        source_uuid: str,
        tenant_uuid: str | None = None,
        token: str | None = None,
        uuids: builtins.list[str] | None = None,
        **kwargs: Any,
    ) -> JSONResponse:
        """List contacts from a source asynchronously.

        Args:
            backend: Backend identifier
            source_uuid: Source UUID
            tenant_uuid: Optional tenant UUID
            token: Optional authentication token
            uuids: Optional list of contact UUIDs to filter
            **kwargs: Additional query parameters

        Returns:
            List of contacts

        """
        if backend == "accent" and uuids is not None:
            kwargs["uuid"] = ",".join(uuid for uuid in uuids)
        url = self._build_url(backend, source_uuid, "contacts")
        headers = self.build_headers(tenant_uuid, token)
        response = await self.async_client.get(url, headers=headers, params=kwargs)
        self.raise_from_response(response)
        return self.process_json_response(response)

    def list_contacts_from_source(
        self,
        backend: str,
        source_uuid: str,
        tenant_uuid: str | None = None,
        token: str | None = None,
        uuids: builtins.list[str] | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """List contacts from a source.

        Args:
            backend: Backend identifier
            source_uuid: Source UUID
            tenant_uuid: Optional tenant UUID
            token: Optional authentication token
            uuids: Optional list of contact UUIDs to filter
            **kwargs: Additional query parameters

        Returns:
            List of contacts

        """
        if backend == "accent" and uuids is not None:
            kwargs["uuid"] = ",".join(uuid for uuid in uuids)
        url = self._build_url(backend, source_uuid, "contacts")
        headers = self.build_headers(tenant_uuid, token)
        response = self.sync_client.get(url, headers=headers, params=kwargs)
        self.raise_from_response(response)
        return response.json()

    def _build_base_url(self, backend: str) -> str:
        """Build base URL for a backend.

        Args:
            backend: Backend identifier

        Returns:
            Base URL

        """
        return "/".join([self.base_url, backend, "sources"])

    def _build_url(self, backend: str, source_uuid: str, *args: str) -> str:
        """Build URL for a specific backend source.

        Args:
            backend: Backend identifier
            source_uuid: Source UUID
            *args: Additional path components

        Returns:
            Complete URL

        """
        return "/".join([self.base_url, backend, "sources", source_uuid] + list(args))
