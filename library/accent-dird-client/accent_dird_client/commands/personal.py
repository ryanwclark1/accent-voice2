# Copyright 2025 Accent Communications

"""Personal command implementation."""

import logging
from typing import Any

from accent_lib_rest_client.models import JSONResponse

from accent_dird_client.commands.helpers.base_command import DirdRESTCommand

logger = logging.getLogger(__name__)


class PersonalCommand(DirdRESTCommand):
    """Command for personal contact operations."""

    resource = "personal"

    async def list_async(
        self,
        token: str | None = None,
        tenant_uuid: str | None = None,
        **kwargs: Any,
    ) -> JSONResponse:
        """List personal contacts asynchronously.

        Args:
            token: Optional authentication token
            tenant_uuid: Optional tenant UUID
            **kwargs: Additional query parameters

        Returns:
            List of personal contacts

        """
        headers = self.build_headers(tenant_uuid, token)
        response = await self.async_client.get(
            self.base_url, params=kwargs, headers=headers
        )
        if response.status_code != 200:
            self.raise_from_response(response)
        return self.process_json_response(response)

    def list(
        self,
        token: str | None = None,
        tenant_uuid: str | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """List personal contacts.

        Args:
            token: Optional authentication token
            tenant_uuid: Optional tenant UUID
            **kwargs: Additional query parameters

        Returns:
            List of personal contacts

        """
        headers = self.build_headers(tenant_uuid, token)
        response = self.sync_client.get(self.base_url, params=kwargs, headers=headers)
        if response.status_code != 200:
            self.raise_from_response(response)
        return response.json()

    async def purge_async(
        self,
        token: str | None = None,
        tenant_uuid: str | None = None,
        **kwargs: Any,
    ) -> None:
        """Purge personal contacts asynchronously.

        Args:
            token: Optional authentication token
            tenant_uuid: Optional tenant UUID
            **kwargs: Additional query parameters

        """
        headers = self.build_headers(tenant_uuid, token)
        response = await self.async_client.delete(
            self.base_url, params=kwargs, headers=headers
        )
        if response.status_code != 204:
            self.raise_from_response(response)

    def purge(
        self,
        token: str | None = None,
        tenant_uuid: str | None = None,
        **kwargs: Any,
    ) -> None:
        """Purge personal contacts.

        Args:
            token: Optional authentication token
            tenant_uuid: Optional tenant UUID
            **kwargs: Additional query parameters

        """
        headers = self.build_headers(tenant_uuid, token)
        response = self.sync_client.delete(
            self.base_url, params=kwargs, headers=headers
        )
        if response.status_code != 204:
            self.raise_from_response(response)

    async def export_csv_async(
        self,
        token: str | None = None,
        tenant_uuid: str | None = None,
        **kwargs: Any,
    ) -> str | None:
        """Export personal contacts to CSV asynchronously.

        Args:
            token: Optional authentication token
            tenant_uuid: Optional tenant UUID
            **kwargs: Additional query parameters

        Returns:
            CSV content or None if no contacts

        """
        headers = self.build_headers(tenant_uuid, token)
        # Remove Accept header for CSV response
        headers_copy = headers.copy()
        if "Accept" in headers_copy:
            del headers_copy["Accept"]
        kwargs["format"] = "text/csv"

        response = await self.async_client.get(
            self.base_url, params=kwargs, headers=headers_copy
        )

        if response.status_code == 200:
            return response.text
        if response.status_code == 204:
            return None
        self.raise_from_response(response)

    def export_csv(
        self,
        token: str | None = None,
        tenant_uuid: str | None = None,
        **kwargs: Any,
    ) -> str | None:
        """Export personal contacts to CSV.

        Args:
            token: Optional authentication token
            tenant_uuid: Optional tenant UUID
            **kwargs: Additional query parameters

        Returns:
            CSV content or None if no contacts

        """
        headers = self.build_headers(tenant_uuid, token)
        # Remove Accept header for CSV response
        if "Accept" in headers:
            del headers["Accept"]
        kwargs["format"] = "text/csv"

        response = self.sync_client.get(self.base_url, params=kwargs, headers=headers)

        if response.status_code == 200:
            return response.text
        if response.status_code == 204:
            return None
        self.raise_from_response(response)

    async def get_async(
        self,
        contact_id: str,
        token: str | None = None,
        tenant_uuid: str | None = None,
        **kwargs: Any,
    ) -> JSONResponse:
        """Get a personal contact asynchronously.

        Args:
            contact_id: Contact identifier
            token: Optional authentication token
            tenant_uuid: Optional tenant UUID
            **kwargs: Additional query parameters

        Returns:
            Contact details

        """
        headers = self.build_headers(tenant_uuid, token)
        url = f"{self.base_url}/{contact_id}"
        response = await self.async_client.get(url, params=kwargs, headers=headers)
        if response.status_code != 200:
            self.raise_from_response(response)
        return self.process_json_response(response)

    def get(
        self,
        contact_id: str,
        token: str | None = None,
        tenant_uuid: str | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Get a personal contact.

        Args:
            contact_id: Contact identifier
            token: Optional authentication token
            tenant_uuid: Optional tenant UUID
            **kwargs: Additional query parameters

        Returns:
            Contact details

        """
        headers = self.build_headers(tenant_uuid, token)
        url = f"{self.base_url}/{contact_id}"
        response = self.sync_client.get(url, params=kwargs, headers=headers)
        if response.status_code != 200:
            self.raise_from_response(response)
        return response.json()

    async def import_csv_async(
        self,
        csv_text: str,
        encoding: str | None = None,
        token: str | None = None,
        tenant_uuid: str | None = None,
        **kwargs: Any,
    ) -> JSONResponse:
        """Import contacts from CSV asynchronously.

        Args:
            csv_text: CSV content
            encoding: Optional character encoding
            token: Optional authentication token
            tenant_uuid: Optional tenant UUID
            **kwargs: Additional query parameters

        Returns:
            Import results

        """
        url = f"{self.base_url}/import"
        headers = self.build_headers(tenant_uuid, token)
        content_type = f"text/csv; charset={encoding}" if encoding else "text/csv"
        headers["Content-Type"] = content_type

        response = await self.async_client.post(
            url, content=csv_text, params=kwargs, headers=headers
        )
        if response.status_code != 201:
            self.raise_from_response(response)
        return self.process_json_response(response)

    def import_csv(
        self,
        csv_text: str,
        encoding: str | None = None,
        token: str | None = None,
        tenant_uuid: str | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Import contacts from CSV.

        Args:
            csv_text: CSV content
            encoding: Optional character encoding
            token: Optional authentication token
            tenant_uuid: Optional tenant UUID
            **kwargs: Additional query parameters

        Returns:
            Import results

        """
        url = f"{self.base_url}/import"
        headers = self.build_headers(tenant_uuid, token)
        content_type = f"text/csv; charset={encoding}" if encoding else "text/csv"
        headers["Content-Type"] = content_type

        response = self.sync_client.post(
            url, data=csv_text, params=kwargs, headers=headers
        )
        if response.status_code != 201:
            self.raise_from_response(response)
        return response.json()

    async def create_async(
        self,
        contact_infos: dict[str, Any],
        token: str | None = None,
        tenant_uuid: str | None = None,
        **kwargs: Any,
    ) -> JSONResponse:
        """Create a personal contact asynchronously.

        Args:
            contact_infos: Contact information
            token: Optional authentication token
            tenant_uuid: Optional tenant UUID
            **kwargs: Additional query parameters

        Returns:
            Created contact details

        """
        headers = self.build_headers(tenant_uuid, token)
        response = await self.async_client.post(
            self.base_url, json=contact_infos, params=kwargs, headers=headers
        )
        if response.status_code != 201:
            self.raise_from_response(response)
        return self.process_json_response(response)

    def create(
        self,
        contact_infos: dict[str, Any],
        token: str | None = None,
        tenant_uuid: str | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Create a personal contact.

        Args:
            contact_infos: Contact information
            token: Optional authentication token
            tenant_uuid: Optional tenant UUID
            **kwargs: Additional query parameters

        Returns:
            Created contact details

        """
        headers = self.build_headers(tenant_uuid, token)
        response = self.sync_client.post(
            self.base_url, json=contact_infos, params=kwargs, headers=headers
        )
