# Copyright 2025 Accent Communications

"""Personal source command implementation."""

from typing import Any

from accent_lib_rest_client.models import JSONResponse

from accent_dird_client.commands.helpers.base_source_command import SourceCommand


class Command(SourceCommand):
    """Command for personal source operations.

    This command provides methods to manage personal directory sources,
    which store user-specific contacts.
    """

    resource = "backends/personal/sources"

    async def import_contacts_async(
        self,
        source_uuid: str,
        contact_list: list[dict[str, Any]],
        tenant_uuid: str | None = None,
        token: str | None = None,
    ) -> JSONResponse:
        """Import contacts to a personal source asynchronously.

        Args:
            source_uuid: Personal source UUID
            contact_list: List of contact records to import
            tenant_uuid: Optional tenant UUID
            token: Optional authentication token

        Returns:
            Import results with status information

        """
        url = f"{self.base_url}/{source_uuid}/contacts"
        headers = self.build_headers(tenant_uuid, token)
        response = await self.async_client.post(url, json=contact_list, headers=headers)
        self.raise_from_response(response)
        return self.process_json_response(response)

    def import_contacts(
        self,
        source_uuid: str,
        contact_list: list[dict[str, Any]],
        tenant_uuid: str | None = None,
        token: str | None = None,
    ) -> dict[str, Any]:
        """Import contacts to a personal source.

        Args:
            source_uuid: Personal source UUID
            contact_list: List of contact records to import
            tenant_uuid: Optional tenant UUID
            token: Optional authentication token

        Returns:
            Import results with status information

        """
        url = f"{self.base_url}/{source_uuid}/contacts"
        headers = self.build_headers(tenant_uuid, token)
        response = self.sync_client.post(url, json=contact_list, headers=headers)
        self.raise_from_response(response)
        return response.json()

    async def list_contacts_async(
        self,
        source_uuid: str,
        tenant_uuid: str | None = None,
        token: str | None = None,
        **kwargs: Any,
    ) -> JSONResponse:
        """List contacts from a personal source asynchronously.

        Args:
            source_uuid: Personal source UUID
            tenant_uuid: Optional tenant UUID
            token: Optional authentication token
            **kwargs: Additional query parameters

        Returns:
            List of personal contacts

        """
        url = f"{self.base_url}/{source_uuid}/contacts"
        headers = self.build_headers(tenant_uuid, token)
        response = await self.async_client.get(url, params=kwargs, headers=headers)
        self.raise_from_response(response)
        return self.process_json_response(response)

    def list_contacts(
        self,
        source_uuid: str,
        tenant_uuid: str | None = None,
        token: str | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """List contacts from a personal source.

        Args:
            source_uuid: Personal source UUID
            tenant_uuid: Optional tenant UUID
            token: Optional authentication token
            **kwargs: Additional query parameters

        Returns:
            List of personal contacts

        """
        url = f"{self.base_url}/{source_uuid}/contacts"
        headers = self.build_headers(tenant_uuid, token)
        response = self.sync_client.get(url, params=kwargs, headers=headers)
        self.raise_from_response(response)
        return response.json()
