# Copyright 2025 Accent Communications

"""Profiles command implementation."""

from typing import Any

from accent_lib_rest_client.models import JSONResponse

from accent_dird_client.commands.helpers.base_command import DirdRESTCommand


class ProfilesCommand(DirdRESTCommand):
    """Command for profile operations."""

    resource = "profiles"

    async def create_async(
        self,
        body: dict[str, Any],
        tenant_uuid: str | None = None,
        token: str | None = None,
    ) -> JSONResponse:
        """Create a profile asynchronously.

        Args:
            body: Profile configuration
            tenant_uuid: Optional tenant UUID
            token: Optional authentication token

        Returns:
            Created profile details

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
        """Create a profile.

        Args:
            body: Profile configuration
            tenant_uuid: Optional tenant UUID
            token: Optional authentication token

        Returns:
            Created profile details

        """
        headers = self.build_headers(tenant_uuid, token)
        response = self.sync_client.post(self.base_url, json=body, headers=headers)
        self.raise_from_response(response)
        return response.json()

    async def delete_async(
        self,
        profile_uuid: str,
        tenant_uuid: str | None = None,
        token: str | None = None,
    ) -> None:
        """Delete a profile asynchronously.

        Args:
            profile_uuid: Profile UUID to delete
            tenant_uuid: Optional tenant UUID
            token: Optional authentication token

        """
        headers = self.build_headers(tenant_uuid, token)
        url = "/".join([self.base_url, profile_uuid])
        response = await self.async_client.delete(url, headers=headers)
        self.raise_from_response(response)

    def delete(
        self,
        profile_uuid: str,
        tenant_uuid: str | None = None,
        token: str | None = None,
    ) -> None:
        """Delete a profile.

        Args:
            profile_uuid: Profile UUID to delete
            tenant_uuid: Optional tenant UUID
            token: Optional authentication token

        """
        headers = self.build_headers(tenant_uuid, token)
        url = "/".join([self.base_url, profile_uuid])
        response = self.sync_client.delete(url, headers=headers)
        self.raise_from_response(response)

    async def edit_async(
        self,
        profile_uuid: str,
        body: dict[str, Any],
        tenant_uuid: str | None = None,
        token: str | None = None,
    ) -> None:
        """Edit a profile asynchronously.

        Args:
            profile_uuid: Profile UUID to edit
            body: Updated profile configuration
            tenant_uuid: Optional tenant UUID
            token: Optional authentication token

        """
        headers = self.build_headers(tenant_uuid, token)
        url = "/".join([self.base_url, profile_uuid])
        response = await self.async_client.put(url, json=body, headers=headers)
        self.raise_from_response(response)

    def edit(
        self,
        profile_uuid: str,
        body: dict[str, Any],
        tenant_uuid: str | None = None,
        token: str | None = None,
    ) -> None:
        """Edit a profile.

        Args:
            profile_uuid: Profile UUID to edit
            body: Updated profile configuration
            tenant_uuid: Optional tenant UUID
            token: Optional authentication token

        """
        headers = self.build_headers(tenant_uuid, token)
        url = "/".join([self.base_url, profile_uuid])
        response = self.sync_client.put(url, json=body, headers=headers)
        self.raise_from_response(response)

    async def get_async(
        self,
        profile_uuid: str,
        tenant_uuid: str | None = None,
        token: str | None = None,
    ) -> JSONResponse:
        """Get a profile asynchronously.

        Args:
            profile_uuid: Profile UUID to retrieve
            tenant_uuid: Optional tenant UUID
            token: Optional authentication token

        Returns:
            Profile details

        """
        headers = self.build_headers(tenant_uuid, token)
        url = "/".join([self.base_url, profile_uuid])
        response = await self.async_client.get(url, headers=headers)
        self.raise_from_response(response)
        return self.process_json_response(response)

    def get(
        self,
        profile_uuid: str,
        tenant_uuid: str | None = None,
        token: str | None = None,
    ) -> dict[str, Any]:
        """Get a profile.

        Args:
            profile_uuid: Profile UUID to retrieve
            tenant_uuid: Optional tenant UUID
            token: Optional authentication token

        Returns:
            Profile details

        """
        headers = self.build_headers(tenant_uuid, token)
        url = "/".join([self.base_url, profile_uuid])
        response = self.sync_client.get(url, headers=headers)
        self.raise_from_response(response)
        return response.json()

    async def list_async(
        self,
        tenant_uuid: str | None = None,
        token: str | None = None,
        **kwargs: Any,
    ) -> JSONResponse:
        """List profiles asynchronously.

        Args:
            tenant_uuid: Optional tenant UUID
            token: Optional authentication token
            **kwargs: Additional query parameters

        Returns:
            List of profiles

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
        """List profiles.

        Args:
            tenant_uuid: Optional tenant UUID
            token: Optional authentication token
            **kwargs: Additional query parameters

        Returns:
            List of profiles

        """
        headers = self.build_headers(tenant_uuid, token)
        response = self.sync_client.get(self.base_url, params=kwargs, headers=headers)
        self.raise_from_response(response)
        return response.json()
