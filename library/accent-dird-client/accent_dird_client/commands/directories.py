# Copyright 2025 Accent Communications

"""Directories command implementation."""

import logging
from typing import Any

from accent_lib_rest_client.models import JSONResponse

from accent_dird_client.commands.helpers.base_command import DirdRESTCommand

logger = logging.getLogger(__name__)


class DirectoriesCommand(DirdRESTCommand):
    """Command for directories operations."""

    resource = "directories"

    async def lookup_async(
        self,
        profile: str,
        token: str | None = None,
        tenant_uuid: str | None = None,
        **kwargs: Any,
    ) -> JSONResponse:
        """Look up contacts asynchronously.

        Args:
            profile: Profile name
            token: Optional authentication token
            tenant_uuid: Optional tenant UUID
            **kwargs: Additional query parameters

        Returns:
            Lookup results

        """
        url = f"{self.base_url}/lookup/{profile}"
        headers = self.build_headers(tenant_uuid, token)
        response = await self.async_client.get(url, params=kwargs, headers=headers)
        if response.status_code != 200:
            self.raise_from_response(response)
        return self.process_json_response(response)

    def lookup(
        self,
        profile: str,
        token: str | None = None,
        tenant_uuid: str | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Look up contacts.

        Args:
            profile: Profile name
            token: Optional authentication token
            tenant_uuid: Optional tenant UUID
            **kwargs: Additional query parameters

        Returns:
            Lookup results

        """
        url = f"{self.base_url}/lookup/{profile}"
        headers = self.build_headers(tenant_uuid, token)
        response = self.sync_client.get(url, params=kwargs, headers=headers)
        if response.status_code != 200:
            self.raise_from_response(response)
        return response.json()

    async def lookup_user_async(
        self,
        profile: str,
        user_uuid: str,
        token: str | None = None,
        tenant_uuid: str | None = None,
        **kwargs: Any,
    ) -> JSONResponse:
        """Look up user contacts asynchronously.

        Args:
            profile: Profile name
            user_uuid: User UUID
            token: Optional authentication token
            tenant_uuid: Optional tenant UUID
            **kwargs: Additional query parameters

        Returns:
            Lookup results

        """
        url = f"{self.base_url}/lookup/{profile}/{user_uuid}"
        headers = self.build_headers(tenant_uuid, token)
        response = await self.async_client.get(url, params=kwargs, headers=headers)
        if response.status_code != 200:
            self.raise_from_response(response)
        return self.process_json_response(response)

    def lookup_user(
        self,
        profile: str,
        user_uuid: str,
        token: str | None = None,
        tenant_uuid: str | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Look up user contacts.

        Args:
            profile: Profile name
            user_uuid: User UUID
            token: Optional authentication token
            tenant_uuid: Optional tenant UUID
            **kwargs: Additional query parameters

        Returns:
            Lookup results

        """
        url = f"{self.base_url}/lookup/{profile}/{user_uuid}"
        headers = self.build_headers(tenant_uuid, token)
        response = self.sync_client.get(url, params=kwargs, headers=headers)
        if response.status_code != 200:
            self.raise_from_response(response)
        return response.json()

    async def reverse_async(
        self,
        profile: str,
        user_uuid: str | None = None,
        token: str | None = None,
        tenant_uuid: str | None = None,
        **kwargs: Any,
    ) -> JSONResponse:
        """Reverse lookup contacts asynchronously.

        Args:
            profile: Profile name
            user_uuid: Optional user UUID
            token: Optional authentication token
            tenant_uuid: Optional tenant UUID
            **kwargs: Additional query parameters

        Returns:
            Reverse lookup results

        """
        if not user_uuid and "accent_user_uuid" in kwargs:
            logger.warning(
                'The "accent_user_uuid" argument has been renamed to "user_uuid"'
            )
            user_uuid = kwargs.pop("accent_user_uuid")

        url = f"{self.base_url}/reverse/{profile}/{user_uuid}"
        headers = self.build_headers(tenant_uuid, token)
        response = await self.async_client.get(url, params=kwargs, headers=headers)
        if response.status_code != 200:
            self.raise_from_response(response)
        return self.process_json_response(response)

    def reverse(
        self,
        profile: str,
        user_uuid: str | None = None,
        token: str | None = None,
        tenant_uuid: str | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Reverse lookup contacts.

        Args:
            profile: Profile name
            user_uuid: Optional user UUID
            token: Optional authentication token
            tenant_uuid: Optional tenant UUID
            **kwargs: Additional query parameters

        Returns:
            Reverse lookup results

        """
        if not user_uuid and "accent_user_uuid" in kwargs:
            logger.warning(
                'The "accent_user_uuid" argument has been renamed to "user_uuid"'
            )
            user_uuid = kwargs.pop("accent_user_uuid")

        url = f"{self.base_url}/reverse/{profile}/{user_uuid}"
        headers = self.build_headers(tenant_uuid, token)
        response = self.sync_client.get(url, params=kwargs, headers=headers)
        if response.status_code != 200:
            self.raise_from_response(response)
        return response.json()

    async def headers_async(
        self,
        profile: str,
        token: str | None = None,
        tenant_uuid: str | None = None,
        **kwargs: Any,
    ) -> JSONResponse:
        """Get directory headers asynchronously.

        Args:
            profile: Profile name
            token: Optional authentication token
            tenant_uuid: Optional tenant UUID
            **kwargs: Additional query parameters

        Returns:
            Headers information

        """
        url = f"{self.base_url}/lookup/{profile}/headers"
        headers = self.build_headers(tenant_uuid, token)
        response = await self.async_client.get(url, params=kwargs, headers=headers)
        if response.status_code != 200:
            self.raise_from_response(response)
        return self.process_json_response(response)

    def headers(
        self,
        profile: str,
        token: str | None = None,
        tenant_uuid: str | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Get directory headers.

        Args:
            profile: Profile name
            token: Optional authentication token
            tenant_uuid: Optional tenant UUID
            **kwargs: Additional query parameters

        Returns:
            Headers information

        """
        url = f"{self.base_url}/lookup/{profile}/headers"
        headers = self.build_headers(tenant_uuid, token)
        response = self.sync_client.get(url, params=kwargs, headers=headers)
        if response.status_code != 200:
            self.raise_from_response(response)
        return response.json()

    async def favorites_async(
        self,
        profile: str,
        token: str | None = None,
        tenant_uuid: str | None = None,
        **kwargs: Any,
    ) -> JSONResponse:
        """Get favorite contacts asynchronously.

        Args:
            profile: Profile name
            token: Optional authentication token
            tenant_uuid: Optional tenant UUID
            **kwargs: Additional query parameters

        Returns:
            List of favorite contacts

        """
        url = f"{self.base_url}/favorites/{profile}"
        headers = self.build_headers(tenant_uuid, token)
        response = await self.async_client.get(url, params=kwargs, headers=headers)
        if response.status_code != 200:
            self.raise_from_response(response)
        return self.process_json_response(response)

    def favorites(
        self,
        profile: str,
        token: str | None = None,
        tenant_uuid: str | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Get favorite contacts.

        Args:
            profile: Profile name
            token: Optional authentication token
            tenant_uuid: Optional tenant UUID
            **kwargs: Additional query parameters

        Returns:
            List of favorite contacts

        """
        url = f"{self.base_url}/favorites/{profile}"
        headers = self.build_headers(tenant_uuid, token)
        response = self.sync_client.get(url, params=kwargs, headers=headers)
        if response.status_code != 200:
            self.raise_from_response(response)
        return response.json()

    async def new_favorite_async(
        self,
        directory: str,
        contact: str,
        token: str | None = None,
        tenant_uuid: str | None = None,
        **kwargs: Any,
    ) -> None:
        """Add a new favorite contact asynchronously.

        Args:
            directory: Directory name
            contact: Contact identifier
            token: Optional authentication token
            tenant_uuid: Optional tenant UUID
            **kwargs: Additional query parameters

        """
        url = f"{self.base_url}/favorites/{directory}/{contact}"
        headers = self.build_headers(tenant_uuid, token)
        response = await self.async_client.put(url, params=kwargs, headers=headers)
        if response.status_code != 204:
            self.raise_from_response(response)

    def new_favorite(
        self,
        directory: str,
        contact: str,
        token: str | None = None,
        tenant_uuid: str | None = None,
        **kwargs: Any,
    ) -> None:
        """Add a new favorite contact.

        Args:
            directory: Directory name
            contact: Contact identifier
            token: Optional authentication token
            tenant_uuid: Optional tenant UUID
            **kwargs: Additional query parameters

        """
        url = f"{self.base_url}/favorites/{directory}/{contact}"
        headers = self.build_headers(tenant_uuid, token)
        response = self.sync_client.put(url, params=kwargs, headers=headers)
        if response.status_code != 204:
            self.raise_from_response(response)

    async def remove_favorite_async(
        self,
        directory: str,
        contact: str,
        token: str | None = None,
        tenant_uuid: str | None = None,
        **kwargs: Any,
    ) -> None:
        """Remove a favorite contact asynchronously.

        Args:
            directory: Directory name
            contact: Contact identifier
            token: Optional authentication token
            tenant_uuid: Optional tenant UUID
            **kwargs: Additional query parameters

        """
        url = f"{self.base_url}/favorites/{directory}/{contact}"
        headers = self.build_headers(tenant_uuid, token)
        response = await self.async_client.delete(url, params=kwargs, headers=headers)
        if response.status_code != 204:
            self.raise_from_response(response)

    def remove_favorite(
        self,
        directory: str,
        contact: str,
        token: str | None = None,
        tenant_uuid: str | None = None,
        **kwargs: Any,
    ) -> None:
        """Remove a favorite contact.

        Args:
            directory: Directory name
            contact: Contact identifier
            token: Optional authentication token
            tenant_uuid: Optional tenant UUID
            **kwargs: Additional query parameters

        """
        url = f"{self.base_url}/favorites/{directory}/{contact}"
        headers = self.build_headers(tenant_uuid, token)
        response = self.sync_client.delete(url, params=kwargs, headers=headers)
        if response.status_code != 204:
            self.raise_from_response(response)

    async def personal_async(
        self,
        profile: str,
        token: str | None = None,
        tenant_uuid: str | None = None,
        **kwargs: Any,
    ) -> JSONResponse:
        """Get personal contacts asynchronously.

        Args:
            profile: Profile name
            token: Optional authentication token
            tenant_uuid: Optional tenant UUID
            **kwargs: Additional query parameters

        Returns:
            List of personal contacts

        """
        url = f"{self.base_url}/personal/{profile}"
        headers = self.build_headers(tenant_uuid, token)
        response = await self.async_client.get(url, params=kwargs, headers=headers)
        if response.status_code != 200:
            self.raise_from_response(response)
        return self.process_json_response(response)

    def personal(
        self,
        profile: str,
        token: str | None = None,
        tenant_uuid: str | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Get personal contacts.

        Args:
            profile: Profile name
            token: Optional authentication token
            tenant_uuid: Optional tenant UUID
            **kwargs: Additional query parameters

        Returns:
            List of personal contacts

        """
        url = f"{self.base_url}/personal/{profile}"
        headers = self.build_headers(tenant_uuid, token)
        response = self.sync_client.get(url, params=kwargs, headers=headers)
        if response.status_code != 200:
            self.raise_from_response(response)
        return response.json()

    async def list_sources_async(
        self,
        profile: str,
        token: str | None = None,
        tenant_uuid: str | None = None,
        **list_params: Any,
    ) -> JSONResponse:
        """List directory sources asynchronously.

        Args:
            profile: Profile name
            token: Optional authentication token
            tenant_uuid: Optional tenant UUID
            **list_params: Additional query parameters

        Returns:
            List of sources

        """
        url = f"{self.base_url}/{profile}/sources"
        headers = self.build_headers(tenant_uuid, token)
        response = await self.async_client.get(url, params=list_params, headers=headers)
        if response.status_code != 200:
            self.raise_from_response(response)
        return self.process_json_response(response)

    def list_sources(
        self,
        profile: str,
        token: str | None = None,
        tenant_uuid: str | None = None,
        **list_params: Any,
    ) -> dict[str, Any]:
        """List directory sources.

        Args:
            profile: Profile name
            token: Optional authentication token
            tenant_uuid: Optional tenant UUID
            **list_params: Additional query parameters

        Returns:
            List of sources

        """
        url = f"{self.base_url}/{profile}/sources"
        headers = self.build_headers(tenant_uuid, token)
        response = self.sync_client.get(url, params=list_params, headers=headers)
        if response.status_code != 200:
            self.raise_from_response(response)
        return response.json()
