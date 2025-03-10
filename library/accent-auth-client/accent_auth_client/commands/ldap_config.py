# Copyright 2025 Accent Communications

from __future__ import annotations

import logging
from typing import cast

import httpx
from accent_lib_rest_client import RESTCommand

from ..types import JSON

logger = logging.getLogger(__name__)


class LDAPBackendConfigCommand(RESTCommand):
    """Command for LDAP backend configuration operations.

    Provides methods for managing LDAP authentication backends.
    """

    resource = "backends"

    async def get_async(self, tenant_uuid: str | None = None) -> JSON:
        """Get LDAP configuration asynchronously.

        Args:
            tenant_uuid: Optional tenant identifier

        Returns:
            JSON: LDAP configuration

        Raises:
            AccentAPIError: If the request fails

        """
        headers = self._get_headers(tenant_uuid=tenant_uuid)
        url = f"{self.base_url}/ldap"

        r = await self.async_client.get(url, headers=headers)

        try:
            r.raise_for_status()
        except httpx.HTTPStatusError:
            logger.error("Failed to get LDAP configuration")
            self.raise_from_response(r)

        return cast(JSON, r.json())

    def get(self, tenant_uuid: str | None = None) -> JSON:
        """Get LDAP configuration.

        Args:
            tenant_uuid: Optional tenant identifier

        Returns:
            JSON: LDAP configuration

        Raises:
            AccentAPIError: If the request fails

        """
        headers = self._get_headers(tenant_uuid=tenant_uuid)
        url = f"{self.base_url}/ldap"

        r = self.sync_client.get(url, headers=headers)

        if r.status_code != 200:
            logger.error("Failed to get LDAP configuration")
            self.raise_from_response(r)

        return cast(JSON, r.json())

    async def update_async(
        self, ldap_config: dict[str, JSON], tenant_uuid: str | None = None
    ) -> JSON:
        """Update LDAP configuration asynchronously.

        Args:
            ldap_config: Updated LDAP configuration
            tenant_uuid: Optional tenant identifier

        Returns:
            JSON: Updated LDAP configuration

        Raises:
            AccentAPIError: If the request fails

        """
        headers = self._get_headers(tenant_uuid=tenant_uuid)
        url = f"{self.base_url}/ldap"

        r = await self.async_client.put(url, headers=headers, json=ldap_config)

        try:
            r.raise_for_status()
        except httpx.HTTPStatusError:
            logger.error("Failed to update LDAP configuration")
            self.raise_from_response(r)

        return cast(JSON, r.json())

    def update(
        self, ldap_config: dict[str, JSON], tenant_uuid: str | None = None
    ) -> JSON:
        """Update LDAP configuration.

        Args:
            ldap_config: Updated LDAP configuration
            tenant_uuid: Optional tenant identifier

        Returns:
            JSON: Updated LDAP configuration

        Raises:
            AccentAPIError: If the request fails

        """
        headers = self._get_headers(tenant_uuid=tenant_uuid)
        url = f"{self.base_url}/ldap"

        r = self.sync_client.put(url, headers=headers, json=ldap_config)

        if r.status_code != 200:
            logger.error("Failed to update LDAP configuration")
            self.raise_from_response(r)

        return cast(JSON, r.json())

    async def delete_async(self, tenant_uuid: str | None = None) -> None:
        """Delete LDAP configuration asynchronously.

        Args:
            tenant_uuid: Optional tenant identifier

        Raises:
            AccentAPIError: If the request fails

        """
        headers = self._get_headers(tenant_uuid=tenant_uuid)
        url = f"{self.base_url}/ldap"

        r = await self.async_client.delete(url, headers=headers)

        try:
            r.raise_for_status()
        except httpx.HTTPStatusError as e:
            if r.status_code != 204:
                logger.error(
                    "Failed to delete LDAP configuration: %s, status code: %s",
                    str(e),
                    r.status_code,
                )
                self.raise_from_response(r)

    def delete(self, tenant_uuid: str | None = None) -> None:
        """Delete LDAP configuration.

        Args:
            tenant_uuid: Optional tenant identifier

        Raises:
            AccentAPIError: If the request fails

        """
        headers = self._get_headers(tenant_uuid=tenant_uuid)
        url = f"{self.base_url}/ldap"

        r = self.sync_client.delete(url, headers=headers)

        if r.status_code != 204:
            logger.error("Failed to delete LDAP configuration")
            self.raise_from_response(r)
