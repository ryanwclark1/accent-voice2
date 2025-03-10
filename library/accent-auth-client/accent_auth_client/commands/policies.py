# Copyright 2025 Accent Communications

from __future__ import annotations

import logging
from typing import Any, cast
from urllib.parse import quote

import httpx
from accent_lib_rest_client import RESTCommand

from ..types import JSON

logger = logging.getLogger(__name__)


class PoliciesCommand(RESTCommand):
    """Command for policy-related operations.

    Provides methods for managing authorization policies.
    """

    resource = "policies"

    async def add_access_async(self, policy_uuid: str, access: str) -> None:
        """Add an access control entry to a policy asynchronously.

        Args:
            policy_uuid: Policy identifier
            access: Access control entry

        Raises:
            AccentAPIError: If the request fails

        """
        headers = self._get_headers()
        access = quote(access)
        url = f"{self.base_url}/{policy_uuid}/acl/{access}"

        r = await self.async_client.put(url, headers=headers)

        try:
            r.raise_for_status()
        except httpx.HTTPStatusError as e:
            if r.status_code != 204:
                logger.error(
                    "Failed to add access: %s, status code: %s", str(e), r.status_code
                )
                self.raise_from_response(r)

    def add_access(self, policy_uuid: str, access: str) -> None:
        """Add an access control entry to a policy.

        Args:
            policy_uuid: Policy identifier
            access: Access control entry

        Raises:
            AccentAPIError: If the request fails

        """
        headers = self._get_headers()
        access = quote(access)
        url = f"{self.base_url}/{policy_uuid}/acl/{access}"

        r = self.sync_client.put(url, headers=headers)

        if r.status_code != 204:
            logger.error("Failed to add access to policy: %s", policy_uuid)
            self.raise_from_response(r)

    async def delete_async(self, policy_uuid: str) -> None:
        """Delete a policy asynchronously.

        Args:
            policy_uuid: Policy identifier

        Raises:
            AccentAPIError: If the request fails

        """
        headers = self._get_headers()
        url = f"{self.base_url}/{policy_uuid}"

        r = await self.async_client.delete(url, headers=headers)

        try:
            r.raise_for_status()
        except httpx.HTTPStatusError as e:
            if r.status_code != 204:
                logger.error(
                    "Failed to delete policy: %s, status code: %s",
                    str(e),
                    r.status_code,
                )
                self.raise_from_response(r)

    def delete(self, policy_uuid: str) -> None:
        """Delete a policy.

        Args:
            policy_uuid: Policy identifier

        Raises:
            AccentAPIError: If the request fails

        """
        headers = self._get_headers()
        url = f"{self.base_url}/{policy_uuid}"

        r = self.sync_client.delete(url, headers=headers)

        if r.status_code != 204:
            logger.error("Failed to delete policy: %s", policy_uuid)
            self.raise_from_response(r)

    async def edit_async(self, policy_uuid: str, name: str, **kwargs: Any) -> JSON:
        """Edit a policy asynchronously.

        Args:
            policy_uuid: Policy identifier
            name: Policy name
            **kwargs: Additional policy properties

        Returns:
            JSON: Updated policy information

        Raises:
            AccentAPIError: If the request fails

        """
        headers = self._get_headers()
        url = f"{self.base_url}/{policy_uuid}"
        kwargs["name"] = name

        r = await self.async_client.put(url, headers=headers, json=kwargs)

        try:
            r.raise_for_status()
        except httpx.HTTPStatusError:
            logger.error("Failed to edit policy: %s", policy_uuid)
            self.raise_from_response(r)

        return cast(JSON, r.json())

    def edit(self, policy_uuid: str, name: str, **kwargs: Any) -> JSON:
        """Edit a policy.

        Args:
            policy_uuid: Policy identifier
            name: Policy name
            **kwargs: Additional policy properties

        Returns:
            JSON: Updated policy information

        Raises:
            AccentAPIError: If the request fails

        """
        headers = self._get_headers()
        url = f"{self.base_url}/{policy_uuid}"
        kwargs["name"] = name

        r = self.sync_client.put(url, headers=headers, json=kwargs)

        if r.status_code != 200:
            logger.error("Failed to edit policy: %s", policy_uuid)
            self.raise_from_response(r)

        return cast(JSON, r.json())

    async def get_async(self, policy_uuid: str) -> JSON:
        """Get policy information asynchronously.

        Args:
            policy_uuid: Policy identifier

        Returns:
            JSON: Policy information

        Raises:
            AccentAPIError: If the request fails

        """
        headers = self._get_headers()
        url = f"{self.base_url}/{policy_uuid}"

        r = await self.async_client.get(url, headers=headers)

        try:
            r.raise_for_status()
        except httpx.HTTPStatusError:
            logger.error("Failed to get policy: %s", policy_uuid)
            self.raise_from_response(r)

        return cast(JSON, r.json())

    def get(self, policy_uuid: str) -> JSON:
        """Get policy information.

        Args:
            policy_uuid: Policy identifier

        Returns:
            JSON: Policy information

        Raises:
            AccentAPIError: If the request fails

        """
        headers = self._get_headers()
        url = f"{self.base_url}/{policy_uuid}"

        r = self.sync_client.get(url, headers=headers)

        if r.status_code != 200:
            logger.error("Failed to get policy: %s", policy_uuid)
            self.raise_from_response(r)

        return cast(JSON, r.json())

    async def list_async(self, tenant_uuid: str | None = None, **kwargs: Any) -> JSON:
        """List policies asynchronously.

        Args:
            tenant_uuid: Optional tenant identifier
            **kwargs: Additional filter parameters

        Returns:
            JSON: List of policies

        Raises:
            AccentAPIError: If the request fails

        """
        headers = self._get_headers(tenant_uuid=tenant_uuid)

        r = await self.async_client.get(self.base_url, headers=headers, params=kwargs)

        try:
            r.raise_for_status()
        except httpx.HTTPStatusError:
            logger.error("Failed to list policies")
            self.raise_from_response(r)

        return cast(JSON, r.json())

    def list(self, tenant_uuid: str | None = None, **kwargs: Any) -> JSON:
        """List policies.

        Args:
            tenant_uuid: Optional tenant identifier
            **kwargs: Additional filter parameters

        Returns:
            JSON: List of policies

        Raises:
            AccentAPIError: If the request fails

        """
        headers = self._get_headers(tenant_uuid=tenant_uuid)

        r = self.sync_client.get(self.base_url, headers=headers, params=kwargs)

        if r.status_code != 200:
            logger.error("Failed to list policies")
            self.raise_from_response(r)

        return cast(JSON, r.json())

    async def new_async(
        self, name: str, tenant_uuid: str | None = None, **kwargs: Any
    ) -> JSON:
        """Create a new policy asynchronously.

        Args:
            name: Policy name
            tenant_uuid: Optional tenant identifier
            **kwargs: Additional policy properties

        Returns:
            JSON: Created policy information

        Raises:
            AccentAPIError: If the request fails

        """
        headers = self._get_headers(tenant_uuid=tenant_uuid)
        kwargs["name"] = name

        r = await self.async_client.post(self.base_url, headers=headers, json=kwargs)

        try:
            r.raise_for_status()
        except httpx.HTTPStatusError:
            logger.error("Failed to create new policy: %s", name)
            self.raise_from_response(r)

        return cast(JSON, r.json())

    def new(self, name: str, tenant_uuid: str | None = None, **kwargs: Any) -> JSON:
        """Create a new policy.

        Args:
            name: Policy name
            tenant_uuid: Optional tenant identifier
            **kwargs: Additional policy properties

        Returns:
            JSON: Created policy information

        Raises:
            AccentAPIError: If the request fails

        """
        headers = self._get_headers(tenant_uuid=tenant_uuid)
        kwargs["name"] = name

        r = self.sync_client.post(self.base_url, headers=headers, json=kwargs)

        if r.status_code != 200:
            logger.error("Failed to create new policy: %s", name)
            self.raise_from_response(r)

        return cast(JSON, r.json())

    async def remove_access_async(self, policy_uuid: str, access: str) -> None:
        """Remove an access control entry from a policy asynchronously.

        Args:
            policy_uuid: Policy identifier
            access: Access control entry

        Raises:
            AccentAPIError: If the request fails

        """
        headers = self._get_headers()
        access = quote(access)
        url = f"{self.base_url}/{policy_uuid}/acl/{access}"

        r = await self.async_client.delete(url, headers=headers)

        try:
            r.raise_for_status()
        except httpx.HTTPStatusError as e:
            if r.status_code != 204:
                logger.error(
                    "Failed to remove access: %s, status code: %s",
                    str(e),
                    r.status_code,
                )
                self.raise_from_response(r)

    def remove_access(self, policy_uuid: str, access: str) -> None:
        """Remove an access control entry from a policy.

        Args:
            policy_uuid: Policy identifier
            access: Access control entry

        Raises:
            AccentAPIError: If the request fails

        """
        headers = self._get_headers()
        access = quote(access)
        url = f"{self.base_url}/{policy_uuid}/acl/{access}"

        r = self.sync_client.delete(url, headers=headers)

        if r.status_code != 204:
            logger.error("Failed to remove access from policy: %s", policy_uuid)
            self.raise_from_response(r)
