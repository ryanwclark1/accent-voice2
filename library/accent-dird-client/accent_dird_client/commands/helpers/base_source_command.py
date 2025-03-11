# Copyright 2025 Accent Communications

"""Base source command implementation."""

from typing import Any

from accent_lib_rest_client.models import JSONResponse

from accent_dird_client.commands.helpers.base_command import DirdRESTCommand


class SourceCommand(DirdRESTCommand):
    """Base command for source operations."""

    async def create_async(
        self,
        body: dict[str, Any],
        tenant_uuid: str | None = None,
        token: str | None = None,
    ) -> JSONResponse:
        """Create a source asynchronously.

        Args:
            body: Source configuration
            tenant_uuid: Optional tenant UUID
            token: Optional authentication token

        Returns:
            Created source details

        """
        headers = self.build_headers(tenant_uuid, token)
        response = await self.async_client.post(
            self.base_url, json=body, headers=headers
        )
        self.raise_from_response(response)
        return self.process_json_response(response)

    def create(
        self,
        body: dict[str, Any],
        tenant_uuid: str | None = None,
        token: str | None = None,
    ) -> dict[str, Any]:
        """Create a source.

        Args:
            body: Source configuration
            tenant_uuid: Optional tenant UUID
            token: Optional authentication token

        Returns:
            Created source details

        """
        headers = self.build_headers(tenant_uuid, token)
        response = self.sync_client.post(self.base_url, json=body, headers=headers)
        self.raise_from_response(response)
        return response.json()

    async def delete_async(
        self,
        source_uuid: str,
        tenant_uuid: str | None = None,
        token: str | None = None,
    ) -> None:
        """Delete a source asynchronously.

        Args:
            source_uuid: Source UUID to delete
            tenant_uuid: Optional tenant UUID
            token: Optional authentication token

        """
        headers = self.build_headers(tenant_uuid, token)
        url = "/".join([self.base_url, source_uuid])
        response = await self.async_client.delete(url, headers=headers)
        self.raise_from_response(response)

    def delete(
        self,
        source_uuid: str,
        tenant_uuid: str | None = None,
        token: str | None = None,
    ) -> None:
        """Delete a source.

        Args:
            source_uuid: Source UUID to delete
            tenant_uuid: Optional tenant UUID
            token: Optional authentication token

        """
        headers = self.build_headers(tenant_uuid, token)
        url = "/".join([self.base_url, source_uuid])
        response = self.sync_client.delete(url, headers=headers)
        self.raise_from_response(response)

    async def get_async(
        self,
        source_uuid: str,
        tenant_uuid: str | None = None,
        token: str | None = None,
    ) -> JSONResponse:
        """Get a source asynchronously.

        Args:
            source_uuid: Source UUID to retrieve
            tenant_uuid: Optional tenant UUID
            token: Optional authentication token

        Returns:
            Source details

        """
        headers = self.build_headers(tenant_uuid, token)
        url = "/".join([self.base_url, source_uuid])
        response = await self.async_client.get(url, headers=headers)
        self.raise_from_response(response)
        return self.process_json_response(response)

    def get(
        self,
        source_uuid: str,
        tenant_uuid: str | None = None,
        token: str | None = None,
    ) -> dict[str, Any]:
        """Get a source.

        Args:
            source_uuid: Source UUID to retrieve
            tenant_uuid: Optional tenant UUID
            token: Optional authentication token

        Returns:
            Source details

        """
        headers = self.build_headers(tenant_uuid, token)
        url = "/".join([self.base_url, source_uuid])
        response = self.sync_client.get(url, headers=headers)
        self.raise_from_response(response)
        return response.json()

    async def edit_async(
        self,
        source_uuid: str,
        body: dict[str, Any],
        tenant_uuid: str | None = None,
        token: str | None = None,
    ) -> None:
        """Edit a source asynchronously.

        Args:
            source_uuid: Source UUID to edit
            body: Updated source configuration
            tenant_uuid: Optional tenant UUID
            token: Optional authentication token

        """
        headers = self.build_headers(tenant_uuid, token)
        url = "/".join([self.base_url, source_uuid])
        response = await self.async_client.put(url, json=body, headers=headers)
        self.raise_from_response(response)

    def edit(
        self,
        source_uuid: str,
        body: dict[str, Any],
        tenant_uuid: str | None = None,
        token: str | None = None,
    ) -> None:
        """Edit a source.

        Args:
            source_uuid: Source UUID to edit
            body: Updated source configuration
            tenant_uuid: Optional tenant UUID
            token: Optional authentication token

        """
        headers = self.build_headers(tenant_uuid, token)
        url = "/".join([self.base_url, source_uuid])
        response = self.sync_client.put(url, json=body, headers=headers)
        self.raise_from_response(response)

    async def list_async(
        self,
        tenant_uuid: str | None = None,
        token: str | None = None,
        **kwargs: Any,
    ) -> JSONResponse:
        """List sources asynchronously.

        Args:
            tenant_uuid: Optional tenant UUID
            token: Optional authentication token
            **kwargs: Additional query parameters

        Returns:
            List of sources

        """
        headers = self.build_headers(tenant_uuid, token)
        response = await self.async_client.get(
            self.base_url, params=kwargs, headers=headers
        )
        self.raise_from_response(response)
        return self.process_json_response(response)

    def list(
        self,
        tenant_uuid: str | None = None,
        token: str | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """List sources.

        Args:
            tenant_uuid: Optional tenant UUID
            token: Optional authentication token
            **kwargs: Additional query parameters

        Returns:
            List of sources

        """
        headers = self.build_headers(tenant_uuid, token)
        response = self.sync_client.get(self.base_url, params=kwargs, headers=headers)
        self.raise_from_response(response)
        return response.json()
