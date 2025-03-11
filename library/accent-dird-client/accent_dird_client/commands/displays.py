# Copyright 2025 Accent Communications

"""Displays command implementation."""

from typing import Any

from accent_lib_rest_client.models import JSONResponse

from accent_dird_client.commands.helpers.base_command import DirdRESTCommand


class DisplaysCommand(DirdRESTCommand):
    """Command for display operations."""

    resource = "displays"

    async def create_async(
        self,
        body: dict[str, Any],
        tenant_uuid: str | None = None,
        token: str | None = None,
    ) -> JSONResponse:
        """Create a display asynchronously.

        Args:
            body: Display configuration
            tenant_uuid: Optional tenant UUID
            token: Optional authentication token

        Returns:
            Created display details

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
        """Create a display.

        Args:
            body: Display configuration
            tenant_uuid: Optional tenant UUID
            token: Optional authentication token

        Returns:
            Created display details

        """
        headers = self.build_headers(tenant_uuid, token)
        response = self.sync_client.post(self.base_url, json=body, headers=headers)
        self.raise_from_response(response)
        return response.json()

    async def delete_async(
        self,
        display_uuid: str,
        tenant_uuid: str | None = None,
        token: str | None = None,
    ) -> None:
        """Delete a display asynchronously.

        Args:
            display_uuid: Display UUID to delete
            tenant_uuid: Optional tenant UUID
            token: Optional authentication token

        """
        headers = self.build_headers(tenant_uuid, token)
        url = "/".join([self.base_url, display_uuid])
        response = await self.async_client.delete(url, headers=headers)
        self.raise_from_response(response)

    def delete(
        self,
        display_uuid: str,
        tenant_uuid: str | None = None,
        token: str | None = None,
    ) -> None:
        """Delete a display.

        Args:
            display_uuid: Display UUID to delete
            tenant_uuid: Optional tenant UUID
            token: Optional authentication token

        """
        headers = self.build_headers(tenant_uuid, token)
        url = "/".join([self.base_url, display_uuid])
        response = self.sync_client.delete(url, headers=headers)
        self.raise_from_response(response)

    async def edit_async(
        self,
        display_uuid: str,
        body: dict[str, Any],
        tenant_uuid: str | None = None,
        token: str | None = None,
    ) -> None:
        """Edit a display asynchronously.

        Args:
            display_uuid: Display UUID to edit
            body: Updated display configuration
            tenant_uuid: Optional tenant UUID
            token: Optional authentication token

        """
        headers = self.build_headers(tenant_uuid, token)
        url = "/".join([self.base_url, display_uuid])
        response = await self.async_client.put(url, json=body, headers=headers)
        self.raise_from_response(response)

    def edit(
        self,
        display_uuid: str,
        body: dict[str, Any],
        tenant_uuid: str | None = None,
        token: str | None = None,
    ) -> None:
        """Edit a display.

        Args:
            display_uuid: Display UUID to edit
            body: Updated display configuration
            tenant_uuid: Optional tenant UUID
            token: Optional authentication token

        """
        headers = self.build_headers(tenant_uuid, token)
        url = "/".join([self.base_url, display_uuid])
        response = self.sync_client.put(url, json=body, headers=headers)
        self.raise_from_response(response)

    async def get_async(
        self,
        display_uuid: str,
        tenant_uuid: str | None = None,
        token: str | None = None,
    ) -> JSONResponse:
        """Get a display asynchronously.

        Args:
            display_uuid: Display UUID to retrieve
            tenant_uuid: Optional tenant UUID
            token: Optional authentication token

        Returns:
            Display details

        """
        headers = self.build_headers(tenant_uuid, token)
        url = "/".join([self.base_url, display_uuid])
        response = await self.async_client.get(url, headers=headers)
        self.raise_from_response(response)
        return self.process_json_response(response)

    def get(
        self,
        display_uuid: str,
        tenant_uuid: str | None = None,
        token: str | None = None,
    ) -> dict[str, Any]:
        """Get a display.

        Args:
            display_uuid: Display UUID to retrieve
            tenant_uuid: Optional tenant UUID
            token: Optional authentication token

        Returns:
            Display details

        """
        headers = self.build_headers(tenant_uuid, token)
        url = "/".join([self.base_url, display_uuid])
        response = self.sync_client.get(url, headers=headers)
        self.raise_from_response(response)
        return response.json()

    async def list_async(
        self,
        tenant_uuid: str | None = None,
        token: str | None = None,
        **kwargs: Any,
    ) -> JSONResponse:
        """List displays asynchronously.

        Args:
            tenant_uuid: Optional tenant UUID
            token: Optional authentication token
            **kwargs: Additional query parameters

        Returns:
            List of displays

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
        """List displays.

        Args:
            tenant_uuid: Optional tenant UUID
            token: Optional authentication token
            **kwargs: Additional query parameters

        Returns:
            List of displays

        """
        headers = self.build_headers(tenant_uuid, token)
        response = self.sync_client.get(self.base_url, params=kwargs, headers=headers)
        self.raise_from_response(response)
        return response.json()
