# Copyright 2025 Accent Communications

from __future__ import annotations

import logging
from typing import Any, cast

import httpx
from accent_lib_rest_client import RESTCommand

from ..types import JSON

logger = logging.getLogger(__name__)


class SAMLConfigCommand(RESTCommand):
    """Command for SAML configuration operations.

    Provides methods for managing SAML authentication providers.
    """

    resource = "backends"

    async def get_async(self, tenant_uuid: str | None = None) -> JSON:
        """Get SAML configuration asynchronously.

        Args:
            tenant_uuid: Optional tenant identifier

        Returns:
            JSON: SAML configuration

        Raises:
            AccentAPIError: If the request fails

        """
        headers = self._get_headers(tenant_uuid=tenant_uuid)
        url = f"{self.base_url}/saml"

        r = await self.async_client.get(url, headers=headers)

        try:
            r.raise_for_status()
        except httpx.HTTPStatusError:
            logger.error("Failed to get SAML configuration")
            self.raise_from_response(r)

        return cast(JSON, r.json())

    def get(self, tenant_uuid: str | None = None) -> JSON:
        """Get SAML configuration.

        Args:
            tenant_uuid: Optional tenant identifier

        Returns:
            JSON: SAML configuration

        Raises:
            AccentAPIError: If the request fails

        """
        headers = self._get_headers(tenant_uuid=tenant_uuid)
        url = f"{self.base_url}/saml"

        r = self.sync_client.get(url, headers=headers)

        if r.status_code != 200:
            logger.error("Failed to get SAML configuration")
            self.raise_from_response(r)

        return cast(JSON, r.json())

    async def create_async(
        self, tenant_uuid: str | None = None, **saml_config: Any
    ) -> JSON:
        """Create SAML configuration asynchronously.

        Args:
            tenant_uuid: Optional tenant identifier
            **saml_config: SAML configuration data

        Returns:
            JSON: Created SAML configuration

        Raises:
            AccentAPIError: If the request fails

        """
        headers = self._get_headers(tenant_uuid=tenant_uuid)
        url = f"{self.base_url}/saml"

        r = await self.async_client.post(url, headers=headers, json=saml_config)

        try:
            r.raise_for_status()
        except httpx.HTTPStatusError:
            logger.error("Failed to create SAML configuration")
            self.raise_from_response(r)

        return cast(JSON, r.json())

    def create(self, tenant_uuid: str | None = None, **saml_config: Any) -> JSON:
        """Create SAML configuration.

        Args:
            tenant_uuid: Optional tenant identifier
            **saml_config: SAML configuration data

        Returns:
            JSON: Created SAML configuration

        Raises:
            AccentAPIError: If the request fails

        """
        headers = self._get_headers(tenant_uuid=tenant_uuid)
        url = f"{self.base_url}/saml"

        r = self.sync_client.post(url, headers=headers, json=saml_config)

        if r.status_code != 200:
            logger.error("Failed to create SAML configuration")
            self.raise_from_response(r)

        return cast(JSON, r.json())

    async def update_async(
        self, tenant_uuid: str | None = None, **saml_config: Any
    ) -> None:
        """Update SAML configuration asynchronously.

        Args:
            tenant_uuid: Optional tenant identifier
            **saml_config: Updated SAML configuration data

        Raises:
            AccentAPIError: If the request fails

        """
        headers = self._get_headers(tenant_uuid=tenant_uuid)
        url = f"{self.base_url}/saml"

        r = await self.async_client.put(url, headers=headers, json=saml_config)

        try:
            r.raise_for_status()
        except httpx.HTTPStatusError as e:
            if r.status_code != 200:
                logger.error(
                    "Failed to update SAML configuration: %s, status code: %s",
                    str(e),
                    r.status_code,
                )
                self.raise_from_response(r)

    def update(self, tenant_uuid: str | None = None, **saml_config: Any) -> None:
        """Update SAML configuration.

        Args:
            tenant_uuid: Optional tenant identifier
            **saml_config: Updated SAML configuration data

        Raises:
            AccentAPIError: If the request fails

        """
        headers = self._get_headers(tenant_uuid=tenant_uuid)
        url = f"{self.base_url}/saml"

        r = self.sync_client.put(url, headers=headers, json=saml_config)

        if r.status_code != 200:
            logger.error("Failed to update SAML configuration")
            self.raise_from_response(r)

    async def delete_async(self, tenant_uuid: str | None = None) -> None:
        """Delete SAML configuration asynchronously.

        Args:
            tenant_uuid: Optional tenant identifier

        Raises:
            AccentAPIError: If the request fails

        """
        headers = self._get_headers(tenant_uuid=tenant_uuid)
        url = f"{self.base_url}/saml"

        r = await self.async_client.delete(url, headers=headers)

        try:
            r.raise_for_status()
        except httpx.HTTPStatusError as e:
            if r.status_code != 204:
                logger.error(
                    "Failed to delete SAML configuration: %s, status code: %s",
                    str(e),
                    r.status_code,
                )
                self.raise_from_response(r)

    def delete(self, tenant_uuid: str | None = None) -> None:
        """Delete SAML configuration.

        Args:
            tenant_uuid: Optional tenant identifier

        Raises:
            AccentAPIError: If the request fails

        """
        headers = self._get_headers(tenant_uuid=tenant_uuid)
        url = f"{self.base_url}/saml"

        r = self.sync_client.delete(url, headers=headers)

        if r.status_code != 204:
            logger.error("Failed to delete SAML configuration")
            self.raise_from_response(r)

    async def get_acs_template_async(self) -> JSON:
        """Get ACS URL template asynchronously.

        Returns:
            JSON: ACS URL template

        Raises:
            AccentAPIError: If the request fails

        """
        url = f"{self.base_url}/saml/acs_url_template"

        r = await self.async_client.get(url)

        try:
            r.raise_for_status()
        except httpx.HTTPStatusError:
            logger.error("Failed to get ACS URL template")
            self.raise_from_response(r)

        return cast(JSON, r.json())

    def get_acs_template(self) -> JSON:
        """Get ACS URL template.

        Returns:
            JSON: ACS URL template

        Raises:
            AccentAPIError: If the request fails

        """
        url = f"{self.base_url}/saml/acs_url_template"

        r = self.sync_client.get(url)

        if r.status_code != 200:
            logger.error("Failed to get ACS URL template")
            self.raise_from_response(r)

        return cast(JSON, r.json())

    async def get_metadata_async(self, tenant_uuid: str) -> bytes:
        """Get SAML metadata asynchronously.

        Args:
            tenant_uuid: Tenant identifier

        Returns:
            bytes: SAML metadata content

        Raises:
            AccentAPIError: If the request fails

        """
        headers = self._get_headers(tenant_uuid=tenant_uuid)
        url = f"{self.base_url}/saml/metadata"

        r = await self.async_client.get(url, headers=headers)

        try:
            r.raise_for_status()
        except httpx.HTTPStatusError:
            logger.error("Failed to get SAML metadata")
            self.raise_from_response(r)

        return r.content

    def get_metadata(self, tenant_uuid: str) -> bytes:
        """Get SAML metadata.

        Args:
            tenant_uuid: Tenant identifier

        Returns:
            bytes: SAML metadata content

        Raises:
            AccentAPIError: If the request fails

        """
        headers = self._get_headers(tenant_uuid=tenant_uuid)
        url = f"{self.base_url}/saml/metadata"

        r = self.sync_client.get(url, headers=headers)

        if r.status_code != 200:
            logger.error("Failed to get SAML metadata")
            self.raise_from_response(r)

        return r.content
