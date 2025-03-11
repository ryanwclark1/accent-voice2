# Copyright 2025 Accent Communications

from __future__ import annotations

import logging
from typing import Any, cast

import httpx
from accent_lib_rest_client import RESTCommand

from accent_auth_client.type_definitions import JSON

logger = logging.getLogger(__name__)


class TenantsCommand(RESTCommand):
    """Command for tenant-related operations.

    Provides methods for managing multi-tenant environments.
    """

    resource = "tenants"
    _ro_headers = {"Accept": "application/json"}
    _rw_headers = {"Accept": "application/json", "Content-Type": "application/json"}

    async def add_policy_async(self, tenant_uuid: str, policy_uuid: str) -> None:
        """Add a policy to a tenant asynchronously.

        Args:
            tenant_uuid: Tenant identifier
            policy_uuid: Policy identifier

        Raises:
            AccentAPIError: If the request fails

        """
        headers = self._get_headers()
        url = "/".join([self.base_url, tenant_uuid, "policies", policy_uuid])

        r = await self.async_client.put(url, headers=headers)

        try:
            r.raise_for_status()
        except httpx.HTTPStatusError as e:
            if r.status_code != 204:
                logger.error(
                    "Failed to add policy to tenant: %s, status code: %s",
                    str(e),
                    r.status_code,
                )
                self.raise_from_response(r)

    def add_policy(self, tenant_uuid: str, policy_uuid: str) -> None:
        """Add a policy to a tenant.

        Args:
            tenant_uuid: Tenant identifier
            policy_uuid: Policy identifier

        Raises:
            AccentAPIError: If the request fails

        """
        headers = self._get_headers()
        url = "/".join([self.base_url, tenant_uuid, "policies", policy_uuid])

        r = self.sync_client.put(url, headers=headers)

        if r.status_code != 204:
            logger.error("Failed to add policy to tenant: %s", tenant_uuid)
            self.raise_from_response(r)

    async def delete_async(self, uuid: str, tenant_uuid: str | None = None) -> None:
        """Delete a tenant asynchronously.

        Args:
            uuid: Tenant identifier to delete
            tenant_uuid: Optional parent tenant identifier

        Raises:
            AccentAPIError: If the request fails

        """
        headers = self._get_headers(tenant_uuid=tenant_uuid)
        url = f"{self.base_url}/{uuid}"

        r = await self.async_client.delete(url, headers=headers)

        try:
            r.raise_for_status()
        except httpx.HTTPStatusError as e:
            if r.status_code != 204:
                logger.error(
                    "Failed to delete tenant: %s, status code: %s",
                    str(e),
                    r.status_code,
                )
                self.raise_from_response(r)

    def delete(self, uuid: str, tenant_uuid: str | None = None) -> None:
        """Delete a tenant.

        Args:
            uuid: Tenant identifier to delete
            tenant_uuid: Optional parent tenant identifier

        Raises:
            AccentAPIError: If the request fails

        """
        headers = self._get_headers(tenant_uuid=tenant_uuid)
        url = f"{self.base_url}/{uuid}"

        r = self.sync_client.delete(url, headers=headers)

        if r.status_code != 204:
            logger.error("Failed to delete tenant: %s", uuid)
            self.raise_from_response(r)

    async def edit_async(self, tenant_uuid: str, **kwargs: Any) -> JSON:
        """Edit a tenant asynchronously.

        Args:
            tenant_uuid: Tenant identifier
            **kwargs: Tenant properties to update

        Returns:
            JSON: Updated tenant information

        Raises:
            AccentAPIError: If the request fails

        """
        headers = self._get_headers()
        url = f"{self.base_url}/{tenant_uuid}"

        r = await self.async_client.put(url, headers=headers, json=kwargs)

        try:
            r.raise_for_status()
        except httpx.HTTPStatusError:
            logger.error("Failed to edit tenant: %s", tenant_uuid)
            self.raise_from_response(r)

        return cast(JSON, r.json())

    def edit(self, tenant_uuid: str, **kwargs: Any) -> JSON:
        """Edit a tenant.

        Args:
            tenant_uuid: Tenant identifier
            **kwargs: Tenant properties to update

        Returns:
            JSON: Updated tenant information

        Raises:
            AccentAPIError: If the request fails

        """
        headers = self._get_headers()
        url = f"{self.base_url}/{tenant_uuid}"

        r = self.sync_client.put(url, headers=headers, json=kwargs)

        if r.status_code != 200:
            logger.error("Failed to edit tenant: %s", tenant_uuid)
            self.raise_from_response(r)

        return cast(JSON, r.json())

    async def get_async(self, tenant_uuid: str) -> JSON:
        """Get tenant information asynchronously.

        Args:
            tenant_uuid: Tenant identifier

        Returns:
            JSON: Tenant information

        Raises:
            AccentAPIError: If the request fails

        """
        headers = self._get_headers()
        url = f"{self.base_url}/{tenant_uuid}"

        r = await self.async_client.get(url, headers=headers)

        try:
            r.raise_for_status()
        except httpx.HTTPStatusError:
            logger.error("Failed to get tenant: %s", tenant_uuid)
            self.raise_from_response(r)

        return cast(JSON, r.json())

    def get(self, tenant_uuid: str) -> JSON:
        """Get tenant information.

        Args:
            tenant_uuid: Tenant identifier

        Returns:
            JSON: Tenant information

        Raises:
            AccentAPIError: If the request fails

        """
        headers = self._get_headers()
        url = f"{self.base_url}/{tenant_uuid}"

        r = self.sync_client.get(url, headers=headers)

        if r.status_code != 200:
            logger.error("Failed to get tenant: %s", tenant_uuid)
            self.raise_from_response(r)

        return cast(JSON, r.json())

    async def list_async(self, tenant_uuid: str | None = None, **kwargs: Any) -> JSON:
        """List tenants asynchronously.

        Args:
            tenant_uuid: Optional parent tenant identifier
            **kwargs: Filter parameters

        Returns:
            JSON: List of tenants

        Raises:
            AccentAPIError: If the request fails

        """
        headers = self._get_headers(tenant_uuid=tenant_uuid)

        r = await self.async_client.get(self.base_url, headers=headers, params=kwargs)

        try:
            r.raise_for_status()
        except httpx.HTTPStatusError:
            logger.error("Failed to list tenants")
            self.raise_from_response(r)

        return cast(JSON, r.json())

    def list(self, tenant_uuid: str | None = None, **kwargs: Any) -> JSON:
        """List tenants.

        Args:
            tenant_uuid: Optional parent tenant identifier
            **kwargs: Filter parameters

        Returns:
            JSON: List of tenants

        Raises:
            AccentAPIError: If the request fails

        """
        headers = self._get_headers(tenant_uuid=tenant_uuid)

        r = self.sync_client.get(self.base_url, headers=headers, params=kwargs)

        if r.status_code != 200:
            logger.error("Failed to list tenants")
            self.raise_from_response(r)

        return cast(JSON, r.json())

    async def new_async(self, **kwargs: Any) -> JSON:
        """Create a new tenant asynchronously.

        Args:
            **kwargs: Tenant properties

        Returns:
            JSON: Created tenant information

        Raises:
            AccentAPIError: If the request fails

        """
        parent_uuid = kwargs.pop("parent_uuid", None)
        headers = self._get_headers(tenant_uuid=parent_uuid)

        r = await self.async_client.post(self.base_url, headers=headers, json=kwargs)

        try:
            r.raise_for_status()
        except httpx.HTTPStatusError:
            logger.error("Failed to create new tenant")
            self.raise_from_response(r)

        return cast(JSON, r.json())

    def new(self, **kwargs: Any) -> JSON:
        """Create a new tenant.

        Args:
            **kwargs: Tenant properties

        Returns:
            JSON: Created tenant information

        Raises:
            AccentAPIError: If the request fails

        """
        parent_uuid = kwargs.pop("parent_uuid", None)
        headers = self._get_headers(tenant_uuid=parent_uuid)

        r = self.sync_client.post(self.base_url, headers=headers, json=kwargs)

        if r.status_code != 200:
            logger.error("Failed to create new tenant")
            self.raise_from_response(r)

        return cast(JSON, r.json())

    async def remove_policy_async(self, tenant_uuid: str, policy_uuid: str) -> None:
        """Remove a policy from a tenant asynchronously.

        Args:
            tenant_uuid: Tenant identifier
            policy_uuid: Policy identifier

        Raises:
            AccentAPIError: If the request fails

        """
        headers = self._get_headers()
        url = "/".join([self.base_url, tenant_uuid, "policies", policy_uuid])

        r = await self.async_client.delete(url, headers=headers)

        try:
            r.raise_for_status()
        except httpx.HTTPStatusError as e:
            if r.status_code != 204:
                logger.error(
                    "Failed to remove policy from tenant: %s, status code: %s",
                    str(e),
                    r.status_code,
                )
                self.raise_from_response(r)

    def remove_policy(self, tenant_uuid: str, policy_uuid: str) -> None:
        """Remove a policy from a tenant.

        Args:
            tenant_uuid: Tenant identifier
            policy_uuid: Policy identifier

        Raises:
            AccentAPIError: If the request fails

        """
        headers = self._get_headers()
        url = "/".join([self.base_url, tenant_uuid, "policies", policy_uuid])

        r = self.sync_client.delete(url, headers=headers)

        if r.status_code != 204:
            logger.error("Failed to remove policy from tenant: %s", tenant_uuid)
            self.raise_from_response(r)

    async def get_domains_async(self, tenant_uuid: str) -> JSON:
        """Get tenant domains asynchronously.

        Args:
            tenant_uuid: Tenant identifier

        Returns:
            JSON: List of tenant domains

        Raises:
            AccentAPIError: If the request fails

        """
        url = f"{self.base_url}/{tenant_uuid}/domains"

        r = await self.async_client.get(url)

        try:
            r.raise_for_status()
        except httpx.HTTPStatusError:
            logger.error("Failed to get domains for tenant: %s", tenant_uuid)
            self.raise_from_response(r)

        return cast(JSON, r.json())

    def get_domains(self, tenant_uuid: str) -> JSON:
        """Get tenant domains.

        Args:
            tenant_uuid: Tenant identifier

        Returns:
            JSON: List of tenant domains

        Raises:
            AccentAPIError: If the request fails

        """
        url = f"{self.base_url}/{tenant_uuid}/domains"

        r = self.sync_client.get(url)

        if r.status_code != 200:
            logger.error("Failed to get domains for tenant: %s", tenant_uuid)
            self.raise_from_response(r)

        return cast(JSON, r.json())
