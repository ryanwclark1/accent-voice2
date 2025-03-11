# Copyright 2025 Accent Communications

"""Phonebook command implementation."""

import logging
from typing import Any

from accent_lib_rest_client.models import JSONResponse

from accent_dird_client.commands.helpers.base_command import DirdRESTCommand

logger = logging.getLogger(__name__)


class PhonebookCommand(DirdRESTCommand):
    """Command for phonebook operations."""

    resource = "phonebooks"

    async def create_async(
        self,
        phonebook_body: dict[str, Any],
        token: str | None = None,
        tenant_uuid: str | None = None,
        **kwargs: Any
    ) -> JSONResponse:
        """Create a phonebook asynchronously.
        
        Args:
            phonebook_body: Phonebook configuration
            token: Optional authentication token
            tenant_uuid: Optional tenant UUID
            **kwargs: Additional query parameters
            
        Returns:
            Created phonebook details

        """
        url = self._phonebook_all_url()
        headers = self.build_headers(tenant_uuid, token)
        response = await self.async_client.post(
            url,
            json=phonebook_body,
            params=kwargs,
            headers=headers
        )
        if response.status_code != 201:
            self.raise_from_response(response)
        return self.process_json_response(response)

    def create(
        self,
        phonebook_body: dict[str, Any] | None = None,
        token: str | None = None,
        tenant_uuid: str | None = None,
        **kwargs: Any
    ) -> dict[str, Any]:
        """Create a phonebook.
        
        Args:
            phonebook_body: Phonebook configuration
            token: Optional authentication token
            tenant_uuid: Optional tenant UUID
            **kwargs: Additional query parameters
            
        Returns:
            Created phonebook details

        """
        url = self._phonebook_all_url()
        headers = self.build_headers(tenant_uuid, token)
        response = self.sync_client.post(
            url,
            json=phonebook_body,
            params=kwargs,
            headers=headers
        )
        if response.status_code != 201:
            self.raise_from_response(response)
        return response.json()

    async def create_contact_async(
        self,
        phonebook_uuid: str,
        contact_body: dict[str, Any],
        token: str | None = None,
        tenant_uuid: str | None = None,
        **kwargs: Any
    ) -> JSONResponse:
        """Create a contact in a phonebook asynchronously.
        
        Args:
            phonebook_uuid: Phonebook UUID
            contact_body: Contact configuration
            token: Optional authentication token
            tenant_uuid: Optional tenant UUID
            **kwargs: Additional query parameters
            
        Returns:
            Created contact details

        """
        url = self._contact_all_url(phonebook_uuid)
        headers = self.build_headers(tenant_uuid, token)
        response = await self.async_client.post(
            url,
            json=contact_body,
            params=kwargs,
            headers=headers
        )
        if response.status_code != 201:
            self.raise_from_response(response)
        return self.process_json_response(response)

    def create_contact(
        self,
        phonebook_uuid: str | None = None,
        contact_body: dict[str, Any] | None = None,
        token: str | None = None,
        tenant_uuid: str | None = None,
        **kwargs: Any
    ) -> dict[str, Any]:
        """Create a contact in a phonebook.
        
        Args:
            phonebook_uuid: Phonebook UUID
            contact_body: Contact configuration
            token: Optional authentication token
            tenant_uuid: Optional tenant UUID
            **kwargs: Additional query parameters
            
        Returns:
            Created contact details

        """
        url = self._contact_all_url(phonebook_uuid)
        headers = self.build_headers(tenant_uuid, token)
        response = self.sync_client.post(
            url,
            json=contact_body,
            params=kwargs,
            headers=headers
        )
        if response.status_code != 201:
            self.raise_from_response(response)
        return response.json()

    async def list_async(
        self,
        token: str | None = None,
        tenant_uuid: str | None = None,
        **kwargs: Any
    ) -> JSONResponse:
        """List phonebooks asynchronously.
        
        Args:
            token: Optional authentication token
            tenant_uuid: Optional tenant UUID
            **kwargs: Additional query parameters
            
        Returns:
            List of phonebooks

        """
        url = self._phonebook_all_url()
        headers = self.build_headers(tenant_uuid, token)
        response = await self.async_client.get(
            url,
            params=kwargs,
            headers=headers
        )
        if response.status_code != 200:
            self.raise_from_response(response)
        return self.process_json_response(response)

    def list(
        self,
        token: str | None = None,
        tenant_uuid: str | None = None,
        **kwargs: Any
    ) -> dict[str, Any]:
        """List phonebooks.
        
        Args:
            token: Optional authentication token
            tenant_uuid: Optional tenant UUID
            **kwargs: Additional query parameters
            
        Returns:
            List of phonebooks

        """
        url = self._phonebook_all_url()
        headers = self.build_headers(tenant_uuid, token)
        response = self.sync_client.get(
            url,
            params=kwargs,
            headers=headers
        )
        if response.status_code != 200:
            self.raise_from_response(response)
        return response.json()

    async def list_contacts_async(
        self,
        phonebook_uuid: str,
        token: str | None = None,
        tenant_uuid: str | None = None,
        **kwargs: Any
    ) -> JSONResponse:
        """List contacts in a phonebook asynchronously.
        
        Args:
            phonebook_uuid: Phonebook UUID
            token: Optional authentication token
            tenant_uuid: Optional tenant UUID
            **kwargs: Additional query parameters
            
        Returns:
            List of contacts

        """
        url = self._contact_all_url(phonebook_uuid)
        headers = self.build_headers(tenant_uuid, token)
        response = await self.async_client.get(
            url,
            params=kwargs,
            headers=headers
        )
        if response.status_code != 200:
            self.raise_from_response(response)
        return self.process_json_response(response)

    def list_contacts(
        self,
        phonebook_uuid: str | None = None,
        token: str | None = None,
        tenant_uuid: str | None = None,
        **kwargs: Any
    ) -> dict[str, Any]:
        """List contacts in a phonebook.
        
        Args:
            phonebook_uuid: Phonebook UUID
            token: Optional authentication token
            tenant_uuid: Optional tenant UUID
            **kwargs: Additional query parameters
            
        Returns:
            List of contacts

        """
        url = self._contact_all_url(phonebook_uuid)
        headers = self.build_headers(tenant_uuid, token)
        response = self.sync_client.get(
            url,
            params=kwargs,
            headers=headers
        )
        if response.status_code != 200:
            self.raise_from_response(response)
        return response.json()

    async def delete_async(
        self,
        phonebook_uuid: str,
        token: str | None = None,
        tenant_uuid: str | None = None,
        **kwargs: Any
    ) -> None:
        """Delete a phonebook asynchronously.
        
        Args:
            phonebook_uuid: Phonebook UUID
            token: Optional authentication token
            tenant_uuid: Optional tenant UUID
            **kwargs: Additional query parameters

        """
        url = self._phonebook_one_url(phonebook_uuid)
        headers = self.build_headers(tenant_uuid, token)
        response = await self.async_client.delete(
            url,
            params=kwargs,
            headers=headers
        )
        if response.status_code != 204:
            self.raise_from_response(response)

    def delete(
        self,
        phonebook_uuid: str | None = None,
        token: str | None = None,
        tenant_uuid: str | None = None,
        **kwargs: Any
    ) -> None:
        """Delete a phonebook.
        
        Args:
            phonebook_uuid: Phonebook UUID
            token: Optional authentication token
            tenant_uuid: Optional tenant UUID
            **kwargs: Additional query parameters

        """
        url = self._phonebook_one_url(phonebook_uuid)
        headers = self.build_headers(tenant_uuid, token)
        response = self.sync_client.delete(
            url,
            params=kwargs,
            headers=headers
        )
        if response.status_code != 204:
            self.raise_from_response(response)

    async def edit_async(
        self,
        phonebook_uuid: str,
        phonebook_body: dict[str, Any],
        token: str | None = None,
        tenant_uuid: str | None = None,
        **kwargs: Any
    ) -> JSONResponse:
        """Edit a phonebook asynchronously.
        
        Args:
            phonebook_uuid: Phonebook UUID
            phonebook_body: Updated phonebook configuration
            token: Optional authentication token
            tenant_uuid: Optional tenant UUID
            **kwargs: Additional query parameters
            
        Returns:
            Updated phonebook details

        """
        url = self._phonebook_one_url(phonebook_uuid)
        headers = self.build_headers(tenant_uuid, token)
        response = await self.async_client.put(
            url,
            json=phonebook_body,
            params=kwargs,
            headers=headers
        )
        if response.status_code != 200:
            self.raise_from_response(response)
        return self.process_json_response(response)

    def edit(
        self,
        phonebook_uuid: str | None = None,
        phonebook_body: dict[str, Any] | None = None,
        token: str | None = None,
        tenant_uuid: str | None = None,
        **kwargs: Any
    ) -> dict[str, Any]:
        """Edit a phonebook.
        
        Args:
            phonebook_uuid: Phonebook UUID
            phonebook_body: Updated phonebook configuration
            token: Optional authentication token
            tenant_uuid: Optional tenant UUID
            **kwargs: Additional query parameters
            
        Returns:
            Updated phonebook details

        """
        url = self._phonebook_one_url(phonebook_uuid)
        headers = self.build_headers(tenant_uuid, token)
        response = self.sync_client.put(
            url,
            json=phonebook_body,
            params=kwargs,
            headers=headers
        )
        if response.status_code != 200:
            self.raise_from_response(response)
        return response.json()

    async def get_async(
        self,
        phonebook_uuid: str,
        token: str | None = None,
        tenant_uuid: str | None = None,
        **kwargs: Any
    ) -> JSONResponse:
        """Get a phonebook asynchronously.
        
        Args:
            phonebook_uuid: Phonebook UUID
            token: Optional authentication token
            tenant_uuid: Optional tenant UUID
            **kwargs: Additional query parameters
            
        Returns:
            Phonebook details

        """
        url = self._phonebook_one_url(phonebook_uuid)
        headers = self.build_headers(tenant_uuid, token)
        response = await self.async_client.get(
            url,
            params=kwargs,
            headers=headers
        )
        if response.status_code != 200:
            self.raise_from_response(response)
        return self.process_json_response(response)

    def get(
        self,
        phonebook_uuid: str | None = None,
        token: str | None = None,
        tenant_uuid: str | None = None,
        **kwargs: Any
    ) -> dict[str, Any]:
        """Get a phonebook.
        
        Args:
            phonebook_uuid: Phonebook UUID
            token: Optional authentication token
            tenant_uuid: Optional tenant UUID
            **kwargs: Additional query parameters
            
        Returns:
            Phonebook details

        """
        url = self._phonebook_one_url(phonebook_uuid)
        headers = self.build_headers(tenant_uuid, token)
        response = self.sync_client.get(
            url,
            params=kwargs,
            headers=headers
        )
        if response.status_code != 200:
            self.raise_from_response(response)
        return response.json()

    async def get_contact_async(
        self,
        phonebook_uuid: str,
        contact_uuid: str,
        token: str | None = None,
        tenant_uuid: str | None = None,
        **kwargs: Any
    ) -> JSONResponse:
        """Get a contact from a phonebook asynchronously.
        
        Args:
            phonebook_uuid: Phonebook UUID
            contact_uuid: Contact UUID
            token: Optional authentication token
            tenant_uuid: Optional tenant UUID
            **kwargs: Additional query parameters
            
        Returns:
            Contact details

        """
        url = self._contact_one_url(phonebook_uuid, contact_uuid)
        headers = self.build_headers(tenant_uuid, token)
        response = await self.async_client.get(
            url,
            params=kwargs,
            headers=headers
        )
        if response.status_code != 200:
            self.raise_from_response(response)
        return self.process_json_response(response)

    def get_contact(
        self,
        phonebook_uuid: str | None = None,
        contact_uuid: str | None = None,
        token: str | None = None,
        tenant_uuid: str | None = None,
        **kwargs: Any
    ) -> dict[str, Any]:
        """Get a contact from a phonebook.
        
        Args:
            phonebook_uuid: Phonebook UUID
            contact_uuid: Contact UUID
            token: Optional authentication token
            tenant_uuid: Optional tenant UUID
            **kwargs: Additional query parameters
            
        Returns:
            Contact details

        """
        url = self._contact_one_url(phonebook_uuid, contact_uuid)
        headers = self.build_headers(tenant_uuid, token)
        response = self.sync_client.get(
            url,
            params=kwargs,
            headers=headers
        )
        if response.status_code != 200:
            self.raise_from_response(response)
        return response.json()

    async def edit_contact_async(
        self,
        phonebook_uuid: str,
        contact_uuid: str,
        contact_body: dict[str, Any],
        token: str | None = None,
        tenant_uuid: str | None = None,
        **kwargs: Any
    ) -> JSONResponse:
        """Edit a contact in a phonebook asynchronously.
        
        Args:
            phonebook_uuid: Phonebook UUID
            contact_uuid: Contact UUID
            contact_body: Updated contact configuration
            token: Optional authentication token
            tenant_uuid: Optional tenant UUID
            **kwargs: Additional query parameters
            
        Returns:
            Updated contact details

        """
        url = self._contact_one_url(phonebook_uuid, contact_uuid)
        headers = self.build_headers(tenant_uuid, token)
        response = await self.async_client.put(
            url,
            json=contact_body,
            params=kwargs,
            headers=headers
        )
        if response.status_code != 200:
            self.raise_from_response(response)
        return self.process_json_response(response)

    def edit_contact(
        self,
        phonebook_uuid: str | None = None,
        contact_uuid: str | None = None,
        contact_body: dict[str, Any] | None = None,
        token: str | None = None,
        tenant_uuid: str | None = None,
        **kwargs: Any
    ) -> dict[str, Any]:
        """Edit a contact in a phonebook.

        Args:
            phonebook_uuid: Phonebook UUID
            contact_uuid: Contact UUID
            contact_body: Updated contact configuration
            token: Optional authentication token
            tenant_uuid: Optional tenant UUID
            **kwargs: Additional query parameters

        Returns:
            Updated contact details

        """
        url = self._contact_one_url(phonebook_uuid, contact_uuid)
        headers = self.build_headers(tenant_uuid, token)
        response = self.sync_client.put(
            url, json=contact_body, params=kwargs, headers=headers
        )
        if response.status_code != 200:
            self.raise_from_response(response)
        return response.json()

    async def delete_contact_async(
        self,
        phonebook_uuid: str,
        contact_uuid: str,
        token: str | None = None,
        tenant_uuid: str | None = None,
        **kwargs: Any,
    ) -> None:
        """Delete a contact from a phonebook asynchronously.

        Args:
            phonebook_uuid: Phonebook UUID
            contact_uuid: Contact UUID
            token: Optional authentication token
            tenant_uuid: Optional tenant UUID
            **kwargs: Additional query parameters

        """
        url = self._contact_one_url(phonebook_uuid, contact_uuid)
        headers = self.build_headers(tenant_uuid, token)
        response = await self.async_client.delete(url, params=kwargs, headers=headers)
        if response.status_code != 204:
            self.raise_from_response(response)

    def delete_contact(
        self,
        phonebook_uuid: str | None = None,
        contact_uuid: str | None = None,
        token: str | None = None,
        tenant_uuid: str | None = None,
        **kwargs: Any,
    ) -> None:
        """Delete a contact from a phonebook.

        Args:
            phonebook_uuid: Phonebook UUID
            contact_uuid: Contact UUID
            token: Optional authentication token
            tenant_uuid: Optional tenant UUID
            **kwargs: Additional query parameters

        """
        url = self._contact_one_url(phonebook_uuid, contact_uuid)
        headers = self.build_headers(tenant_uuid, token)
        response = self.sync_client.delete(url, params=kwargs, headers=headers)
        if response.status_code != 204:
            self.raise_from_response(response)

    async def import_csv_async(
        self,
        phonebook_uuid: str,
        csv_text: str,
        encoding: str | None = None,
        token: str | None = None,
        tenant_uuid: str | None = None,
        **kwargs: Any,
    ) -> JSONResponse:
        """Import contacts from CSV to a phonebook asynchronously.

        Args:
            phonebook_uuid: Phonebook UUID
            csv_text: CSV content
            encoding: Optional character encoding
            token: Optional authentication token
            tenant_uuid: Optional tenant UUID
            **kwargs: Additional query parameters

        Returns:
            Import results

        """
        url = self._contact_import_url(phonebook_uuid)
        headers = self.build_headers(tenant_uuid, token)
        content_type = f"text/csv; charset={encoding}" if encoding else "text/csv"
        headers["Content-Type"] = content_type

        response = await self.async_client.post(
            url, content=csv_text, params=kwargs, headers=headers
        )
        if response.status_code != 200:
            self.raise_from_response(response)
        return self.process_json_response(response)

    def import_csv(
        self,
        phonebook_uuid: str | None = None,
        csv_text: str | None = None,
        encoding: str | None = None,
        token: str | None = None,
        tenant_uuid: str | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Import contacts from CSV to a phonebook.

        Args:
            phonebook_uuid: Phonebook UUID
            csv_text: CSV content
            encoding: Optional character encoding
            token: Optional authentication token
            tenant_uuid: Optional tenant UUID
            **kwargs: Additional query parameters

        Returns:
            Import results

        """
        url = self._contact_import_url(phonebook_uuid)
        headers = self.build_headers(tenant_uuid, token)
        content_type = f"text/csv; charset={encoding}" if encoding else "text/csv"
        headers["Content-Type"] = content_type

        response = self.sync_client.post(
            url, data=csv_text, params=kwargs, headers=headers
        )
        if response.status_code != 200:
            self.raise_from_response(response)
        return response.json()

    def _contact_all_url(self, phonebook_uuid: str | None) -> str:
        """Build URL for all contacts in a phonebook.

        Args:
            phonebook_uuid: Phonebook UUID

        Returns:
            URL string

        """
        return f"{self._phonebook_one_url(phonebook_uuid)}/contacts"

    def _contact_one_url(
        self, phonebook_uuid: str | None, contact_uuid: str | None
    ) -> str:
        """Build URL for a specific contact in a phonebook.

        Args:
            phonebook_uuid: Phonebook UUID
            contact_uuid: Contact UUID

        Returns:
            URL string

        """
        return f"{self._contact_all_url(phonebook_uuid)}/{contact_uuid}"

    def _contact_import_url(self, phonebook_uuid: str | None) -> str:
        """Build URL for importing contacts to a phonebook.

        Args:
            phonebook_uuid: Phonebook UUID

        Returns:
            URL string

        """
        return f"{self._contact_all_url(phonebook_uuid)}/import"

    def _phonebook_all_url(self) -> str:
        """Build URL for all phonebooks.

        Returns:
            URL string

        """
        return f"{self.base_url}"

    def _phonebook_one_url(self, phonebook_uuid: str | None) -> str:
        """Build URL for a specific phonebook.

        Args:
            phonebook_uuid: Phonebook UUID

        Returns:
            URL string

        """
        return f"{self._phonebook_all_url()}/{phonebook_uuid}"
