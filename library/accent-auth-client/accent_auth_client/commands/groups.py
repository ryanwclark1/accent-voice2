# Copyright 2025 Accent Communications

from __future__ import annotations

import logging
from typing import Any, cast

import httpx
from accent_lib_rest_client import RESTCommand

from accent_auth_client.type_definitions import JSON

logger = logging.getLogger(__name__)


class GroupsCommand(RESTCommand):
    """Command for group-related operations.

    Provides methods for managing user groups and their relationships.
    """

    resource = "groups"

    async def add_policy_async(
        self, group_uuid: str, policy_uuid: str, tenant_uuid: str | None = None
    ) -> None:
        """Add a policy to a group asynchronously.

        Args:
            group_uuid: Group identifier
            policy_uuid: Policy identifier
            tenant_uuid: Optional tenant identifier

        Raises:
            AccentAPIError: If the request fails

        """
        headers = self._get_headers(tenant_uuid=tenant_uuid)
        url = self._relation_url("policies", group_uuid, policy_uuid)

        r = await self.async_client.put(url, headers=headers)

        try:
            r.raise_for_status()
        except httpx.HTTPStatusError as e:
            if r.status_code != 204:
                logger.error(
                    "Failed to add policy to group: %s, status code: %s",
                    str(e),
                    r.status_code,
                )
                self.raise_from_response(r)

    def add_policy(
        self, group_uuid: str, policy_uuid: str, tenant_uuid: str | None = None
    ) -> None:
        """Add a policy to a group.

        Args:
            group_uuid: Group identifier
            policy_uuid: Policy identifier
            tenant_uuid: Optional tenant identifier

        Raises:
            AccentAPIError: If the request fails

        """
        headers = self._get_headers(tenant_uuid=tenant_uuid)
        url = self._relation_url("policies", group_uuid, policy_uuid)

        r = self.sync_client.put(url, headers=headers)

        if r.status_code != 204:
            logger.error("Failed to add policy to group: %s", group_uuid)
            self.raise_from_response(r)

    async def add_user_async(self, group_uuid: str, user_uuid: str) -> None:
        """Add a user to a group asynchronously.

        Args:
            group_uuid: Group identifier
            user_uuid: User identifier

        Raises:
            AccentAPIError: If the request fails

        """
        headers = self._get_headers()
        url = self._relation_url("users", group_uuid, user_uuid)

        r = await self.async_client.put(url, headers=headers)

        try:
            r.raise_for_status()
        except httpx.HTTPStatusError as e:
            if r.status_code != 204:
                logger.error(
                    "Failed to add user to group: %s, status code: %s",
                    str(e),
                    r.status_code,
                )
                self.raise_from_response(r)

    def add_user(self, group_uuid: str, user_uuid: str) -> None:
        """Add a user to a group.

        Args:
            group_uuid: Group identifier
            user_uuid: User identifier

        Raises:
            AccentAPIError: If the request fails

        """
        headers = self._get_headers()
        url = self._relation_url("users", group_uuid, user_uuid)

        r = self.sync_client.put(url, headers=headers)

        if r.status_code != 204:
            logger.error("Failed to add user to group: %s", group_uuid)
            self.raise_from_response(r)

    async def delete_async(self, group_uuid: str) -> None:
        """Delete a group asynchronously.

        Args:
            group_uuid: Group identifier

        Raises:
            AccentAPIError: If the request fails

        """
        headers = self._get_headers()
        url = f"{self.base_url}/{group_uuid}"

        r = await self.async_client.delete(url, headers=headers)

        try:
            r.raise_for_status()
        except httpx.HTTPStatusError as e:
            if r.status_code != 204:
                logger.error(
                    "Failed to delete group: %s, status code: %s", str(e), r.status_code
                )
                self.raise_from_response(r)

    def delete(self, group_uuid: str) -> None:
        """Delete a group.

        Args:
            group_uuid: Group identifier

        Raises:
            AccentAPIError: If the request fails

        """
        headers = self._get_headers()
        url = f"{self.base_url}/{group_uuid}"

        r = self.sync_client.delete(url, headers=headers)

        if r.status_code != 204:
            logger.error("Failed to delete group: %s", group_uuid)
            self.raise_from_response(r)

    async def edit_async(self, group_uuid: str, **params: Any) -> JSON:
        """Edit a group asynchronously.

        Args:
            group_uuid: Group identifier
            **params: Group properties to update

        Returns:
            JSON: Updated group information

        Raises:
            AccentAPIError: If the request fails

        """
        headers = self._get_headers()
        url = f"{self.base_url}/{group_uuid}"

        r = await self.async_client.put(url, headers=headers, json=params)

        try:
            r.raise_for_status()
        except httpx.HTTPStatusError:
            logger.error("Failed to edit group: %s", group_uuid)
            self.raise_from_response(r)

        return cast(JSON, r.json())

    def edit(self, group_uuid: str, **params: Any) -> JSON:
        """Edit a group.

        Args:
            group_uuid: Group identifier
            **params: Group properties to update

        Returns:
            JSON: Updated group information

        Raises:
            AccentAPIError: If the request fails

        """
        headers = self._get_headers()
        url = f"{self.base_url}/{group_uuid}"

        r = self.sync_client.put(url, headers=headers, json=params)

        if r.status_code != 200:
            logger.error("Failed to edit group: %s", group_uuid)
            self.raise_from_response(r)

        return cast(JSON, r.json())

    async def get_async(self, group_uuid: str) -> JSON:
        """Get group information asynchronously.

        Args:
            group_uuid: Group identifier

        Returns:
            JSON: Group information

        Raises:
            AccentAPIError: If the request fails

        """
        headers = self._get_headers()
        url = f"{self.base_url}/{group_uuid}"

        r = await self.async_client.get(url, headers=headers)

        try:
            r.raise_for_status()
        except httpx.HTTPStatusError:
            logger.error("Failed to get group: %s", group_uuid)
            self.raise_from_response(r)

        return cast(JSON, r.json())

    def get(self, group_uuid: str) -> JSON:
        """Get group information.

        Args:
            group_uuid: Group identifier

        Returns:
            JSON: Group information

        Raises:
            AccentAPIError: If the request fails

        """
        headers = self._get_headers()
        url = f"{self.base_url}/{group_uuid}"

        r = self.sync_client.get(url, headers=headers)

        if r.status_code != 200:
            logger.error("Failed to get group: %s", group_uuid)
            self.raise_from_response(r)

        return cast(JSON, r.json())

    async def get_policies_async(
        self, group_uuid: str, tenant_uuid: str | None = None, **kwargs: Any
    ) -> JSON:
        """Get group policies asynchronously.

        Args:
            group_uuid: Group identifier
            tenant_uuid: Optional tenant identifier
            **kwargs: Additional filter parameters

        Returns:
            JSON: Group policies

        Raises:
            AccentAPIError: If the request fails

        """
        headers = self._get_headers(tenant_uuid=tenant_uuid)
        url = f"{self.base_url}/{group_uuid}/policies"

        r = await self.async_client.get(url, headers=headers, params=kwargs)

        try:
            r.raise_for_status()
        except httpx.HTTPStatusError:
            logger.error("Failed to get policies for group: %s", group_uuid)
            self.raise_from_response(r)

        return cast(JSON, r.json())

    def get_policies(
        self, group_uuid: str, tenant_uuid: str | None = None, **kwargs: Any
    ) -> JSON:
        """Get group policies.

        Args:
            group_uuid: Group identifier
            tenant_uuid: Optional tenant identifier
            **kwargs: Additional filter parameters

        Returns:
            JSON: Group policies

        Raises:
            AccentAPIError: If the request fails

        """
        headers = self._get_headers(tenant_uuid=tenant_uuid)
        url = f"{self.base_url}/{group_uuid}/policies"

        r = self.sync_client.get(url, headers=headers, params=kwargs)

        if r.status_code != 200:
            logger.error("Failed to get policies for group: %s", group_uuid)
            self.raise_from_response(r)

        return cast(JSON, r.json())

    async def get_users_async(self, group_uuid: str, **kwargs: Any) -> JSON:
        """Get group users asynchronously.

        Args:
            group_uuid: Group identifier
            **kwargs: Additional filter parameters

        Returns:
            JSON: Group users

        Raises:
            AccentAPIError: If the request fails

        """
        headers = self._get_headers()
        url = f"{self.base_url}/{group_uuid}/users"

        r = await self.async_client.get(url, headers=headers, params=kwargs)

        try:
            r.raise_for_status()
        except httpx.HTTPStatusError:
            logger.error("Failed to get users for group: %s", group_uuid)
            self.raise_from_response(r)

        return cast(JSON, r.json())

    def get_users(self, group_uuid: str, **kwargs: Any) -> JSON:
        """Get group users.

        Args:
            group_uuid: Group identifier
            **kwargs: Additional filter parameters

        Returns:
            JSON: Group users

        Raises:
            AccentAPIError: If the request fails

        """
        headers = self._get_headers()
        url = f"{self.base_url}/{group_uuid}/users"

        r = self.sync_client.get(url, headers=headers, params=kwargs)

        if r.status_code != 200:
            logger.error("Failed to get users for group: %s", group_uuid)
            self.raise_from_response(r)

        return cast(JSON, r.json())

    async def list_async(self, **kwargs: Any) -> JSON:
        """List groups asynchronously.

        Args:
            **kwargs: Filter parameters

        Returns:
            JSON: List of groups

        Raises:
            AccentAPIError: If the request fails

        """
        headers = self._get_headers(**kwargs)

        r = await self.async_client.get(self.base_url, headers=headers, params=kwargs)

        try:
            r.raise_for_status()
        except httpx.HTTPStatusError:
            logger.error("Failed to list groups")
            self.raise_from_response(r)

        return cast(JSON, r.json())

    def list(self, **kwargs: Any) -> JSON:
        """List groups.

        Args:
            **kwargs: Filter parameters

        Returns:
            JSON: List of groups

        Raises:
            AccentAPIError: If the request fails

        """
        headers = self._get_headers(**kwargs)

        r = self.sync_client.get(self.base_url, headers=headers, params=kwargs)

        if r.status_code != 200:
            logger.error("Failed to list groups")
            self.raise_from_response(r)

        return cast(JSON, r.json())

    async def new_async(self, **kwargs: Any) -> JSON:
        """Create a new group asynchronously.

        Args:
            **kwargs: Group properties

        Returns:
            JSON: Created group information

        Raises:
            AccentAPIError: If the request fails

        """
        headers = self._get_headers(**kwargs)

        r = await self.async_client.post(self.base_url, headers=headers, json=kwargs)

        try:
            r.raise_for_status()
        except httpx.HTTPStatusError:
            logger.error("Failed to create new group")
            self.raise_from_response(r)

        return cast(JSON, r.json())

    def new(self, **kwargs: Any) -> JSON:
        """Create a new group.

        Args:
            **kwargs: Group properties

        Returns:
            JSON: Created group information

        Raises:
            AccentAPIError: If the request fails

        """
        headers = self._get_headers(**kwargs)

        r = self.sync_client.post(self.base_url, headers=headers, json=kwargs)

        if r.status_code != 200:
            logger.error("Failed to create new group")
            self.raise_from_response(r)

        return cast(JSON, r.json())

    async def remove_policy_async(
        self, group_uuid: str, policy_uuid: str, tenant_uuid: str | None = None
    ) -> None:
        """Remove a policy from a group asynchronously.

        Args:
            group_uuid: Group identifier
            policy_uuid: Policy identifier
            tenant_uuid: Optional tenant identifier

        Raises:
            AccentAPIError: If the request fails

        """
        headers = self._get_headers(tenant_uuid=tenant_uuid)
        url = self._relation_url("policies", group_uuid, policy_uuid)

        r = await self.async_client.delete(url, headers=headers)

        try:
            r.raise_for_status()
        except httpx.HTTPStatusError as e:
            if r.status_code != 204:
                logger.error(
                    "Failed to remove policy from group: %s, status code: %s",
                    str(e),
                    r.status_code,
                )
                self.raise_from_response(r)

    def remove_policy(
        self, group_uuid: str, policy_uuid: str, tenant_uuid: str | None = None
    ) -> None:
        """Remove a policy from a group.

        Args:
            group_uuid: Group identifier
            policy_uuid: Policy identifier
            tenant_uuid: Optional tenant identifier

        Raises:
            AccentAPIError: If the request fails

        """
        headers = self._get_headers(tenant_uuid=tenant_uuid)
        url = self._relation_url("policies", group_uuid, policy_uuid)

        r = self.sync_client.delete(url, headers=headers)

        if r.status_code != 204:
            logger.error("Failed to remove policy from group: %s", group_uuid)
            self.raise_from_response(r)

    async def remove_user_async(self, group_uuid: str, user_uuid: str) -> None:
        """Remove a user from a group asynchronously.

        Args:
            group_uuid: Group identifier
            user_uuid: User identifier

        Raises:
            AccentAPIError: If the request fails

        """
        headers = self._get_headers()
        url = self._relation_url("users", group_uuid, user_uuid)

        r = await self.async_client.delete(url, headers=headers)

        try:
            r.raise_for_status()
        except httpx.HTTPStatusError as e:
            if r.status_code != 204:
                logger.error(
                    "Failed to remove user from group: %s, status code: %s",
                    str(e),
                    r.status_code,
                )
                self.raise_from_response(r)

    def remove_user(self, group_uuid: str, user_uuid: str) -> None:
        """Remove a user from a group.

        Args:
            group_uuid: Group identifier
            user_uuid: User identifier

        Raises:
            AccentAPIError: If the request fails

        """
        headers = self._get_headers()
        url = self._relation_url("users", group_uuid, user_uuid)

        r = self.sync_client.delete(url, headers=headers)

        if r.status_code != 204:
            logger.error("Failed to remove user from group: %s", group_uuid)
            self.raise_from_response(r)

    def _relation_url(self, resource: str, group_uuid: str, resource_uuid: str) -> str:
        """Build a URL for group relation operations.

        Args:
            resource: Resource type (e.g., 'users', 'policies')
            group_uuid: Group identifier
            resource_uuid: Resource identifier

        Returns:
            str: Complete URL

        """
        return "/".join([self.base_url, group_uuid, resource, resource_uuid])
