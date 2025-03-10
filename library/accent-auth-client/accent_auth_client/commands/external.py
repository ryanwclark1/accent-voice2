# Copyright 2025 Accent Communications

from __future__ import annotations

import logging
from typing import Any, cast

import httpx
from accent_lib_rest_client import RESTCommand

from ..types import JSON

logger = logging.getLogger(__name__)


class ExternalAuthCommand(RESTCommand):
    """Command for external authentication operations.

    Provides methods for managing external authentication providers.
    """

    resource = "users"

    async def create_async(
        self, auth_type: str, user_uuid: str, data: dict[str, JSON]
    ) -> JSON:
        """Create an external authentication entry asynchronously.

        Args:
            auth_type: Authentication type
            user_uuid: User identifier
            data: Authentication data

        Returns:
            JSON: Created authentication entry

        Raises:
            AccentAPIError: If the request fails

        """
        headers = self._get_headers()
        url = self._build_url(auth_type, user_uuid)

        r = await self.async_client.post(url, headers=headers, json=data)

        try:
            r.raise_for_status()
        except httpx.HTTPStatusError:
            logger.error(
                "Failed to create external auth for user: %s, auth type: %s",
                user_uuid,
                auth_type,
            )
            self.raise_from_response(r)

        return cast(JSON, r.json())

    def create(self, auth_type: str, user_uuid: str, data: dict[str, JSON]) -> JSON:
        """Create an external authentication entry.

        Args:
            auth_type: Authentication type
            user_uuid: User identifier
            data: Authentication data

        Returns:
            JSON: Created authentication entry

        Raises:
            AccentAPIError: If the request fails

        """
        headers = self._get_headers()
        url = self._build_url(auth_type, user_uuid)

        r = self.sync_client.post(url, headers=headers, json=data)

        if r.status_code != 200:
            logger.error(
                "Failed to create external auth for user: %s, auth type: %s",
                user_uuid,
                auth_type,
            )
            self.raise_from_response(r)

        return cast(JSON, r.json())

    async def create_config_async(
        self, auth_type: str, data: dict[str, JSON], tenant_uuid: str | None = None
    ) -> JSON:
        """Create an external authentication configuration asynchronously.

        Args:
            auth_type: Authentication type
            data: Configuration data
            tenant_uuid: Optional tenant identifier

        Returns:
            JSON: Created configuration

        Raises:
            AccentAPIError: If the request fails

        """
        headers = self._get_headers(tenant_uuid=tenant_uuid)
        url = self._build_config_url(auth_type)

        r = await self.async_client.post(url, headers=headers, json=data)

        try:
            r.raise_for_status()
        except httpx.HTTPStatusError:
            logger.error(
                "Failed to create external auth config for auth type: %s", auth_type
            )
            self.raise_from_response(r)

        return cast(JSON, r.json())

    def create_config(
        self, auth_type: str, data: dict[str, JSON], tenant_uuid: str | None = None
    ) -> JSON:
        """Create an external authentication configuration.

        Args:
            auth_type: Authentication type
            data: Configuration data
            tenant_uuid: Optional tenant identifier

        Returns:
            JSON: Created configuration

        Raises:
            AccentAPIError: If the request fails

        """
        headers = self._get_headers(tenant_uuid=tenant_uuid)
        url = self._build_config_url(auth_type)

        r = self.sync_client.post(url, headers=headers, json=data)

        if r.status_code != 201:
            logger.error(
                "Failed to create external auth config for auth type: %s", auth_type
            )
            self.raise_from_response(r)

        return cast(JSON, r.json())

    async def delete_async(self, auth_type: str, user_uuid: str) -> None:
        """Delete an external authentication entry asynchronously.

        Args:
            auth_type: Authentication type
            user_uuid: User identifier

        Raises:
            AccentAPIError: If the request fails

        """
        headers = self._get_headers()
        url = self._build_url(auth_type, user_uuid)

        r = await self.async_client.delete(url, headers=headers)

        try:
            r.raise_for_status()
        except httpx.HTTPStatusError as e:
            if r.status_code != 204:
                logger.error(
                    "Failed to delete external auth: %s, status code: %s",
                    str(e),
                    r.status_code,
                )
                self.raise_from_response(r)

    def delete(self, auth_type: str, user_uuid: str) -> None:
        """Delete an external authentication entry.

        Args:
            auth_type: Authentication type
            user_uuid: User identifier

        Raises:
            AccentAPIError: If the request fails

        """
        headers = self._get_headers()
        url = self._build_url(auth_type, user_uuid)

        r = self.sync_client.delete(url, headers=headers)

        if r.status_code != 204:
            logger.error(
                "Failed to delete external auth for user: %s, auth type: %s",
                user_uuid,
                auth_type,
            )
            self.raise_from_response(r)

    async def delete_config_async(
        self, auth_type: str, tenant_uuid: str | None = None
    ) -> None:
        """Delete an external authentication configuration asynchronously.

        Args:
            auth_type: Authentication type
            tenant_uuid: Optional tenant identifier

        Raises:
            AccentAPIError: If the request fails

        """
        headers = self._get_headers(tenant_uuid=tenant_uuid)
        url = self._build_config_url(auth_type)

        r = await self.async_client.delete(url, headers=headers)

        try:
            r.raise_for_status()
        except httpx.HTTPStatusError as e:
            if r.status_code != 204:
                logger.error(
                    "Failed to delete external auth config: %s, status code: %s",
                    str(e),
                    r.status_code,
                )
                self.raise_from_response(r)

    def delete_config(self, auth_type: str, tenant_uuid: str | None = None) -> None:
        """Delete an external authentication configuration.

        Args:
            auth_type: Authentication type
            tenant_uuid: Optional tenant identifier

        Raises:
            AccentAPIError: If the request fails

        """
        headers = self._get_headers(tenant_uuid=tenant_uuid)
        url = self._build_config_url(auth_type)

        r = self.sync_client.delete(url, headers=headers)

        if r.status_code != 204:
            logger.error(
                "Failed to delete external auth config for auth type: %s", auth_type
            )
            self.raise_from_response(r)

    async def get_async(
        self, auth_type: str, user_uuid: str, tenant_uuid: str | None = None
    ) -> JSON:
        """Get an external authentication entry asynchronously.

        Args:
            auth_type: Authentication type
            user_uuid: User identifier
            tenant_uuid: Optional tenant identifier

        Returns:
            JSON: Authentication entry

        Raises:
            AccentAPIError: If the request fails

        """
        headers = self._get_headers(tenant_uuid=tenant_uuid)
        url = self._build_url(auth_type, user_uuid)

        r = await self.async_client.get(url, headers=headers)

        try:
            r.raise_for_status()
        except httpx.HTTPStatusError:
            logger.error(
                "Failed to get external auth for user: %s, auth type: %s",
                user_uuid,
                auth_type,
            )
            self.raise_from_response(r)

        return cast(JSON, r.json())

    def get(
        self, auth_type: str, user_uuid: str, tenant_uuid: str | None = None
    ) -> JSON:
        """Get an external authentication entry.

        Args:
            auth_type: Authentication type
            user_uuid: User identifier
            tenant_uuid: Optional tenant identifier

        Returns:
            JSON: Authentication entry

        Raises:
            AccentAPIError: If the request fails

        """
        headers = self._get_headers(tenant_uuid=tenant_uuid)
        url = self._build_url(auth_type, user_uuid)

        r = self.sync_client.get(url, headers=headers)

        if r.status_code != 200:
            logger.error(
                "Failed to get external auth for user: %s, auth type: %s",
                user_uuid,
                auth_type,
            )
            self.raise_from_response(r)

        return cast(JSON, r.json())

    async def get_config_async(
        self, auth_type: str, tenant_uuid: str | None = None
    ) -> JSON:
        """Get an external authentication configuration asynchronously.

        Args:
            auth_type: Authentication type
            tenant_uuid: Optional tenant identifier

        Returns:
            JSON: Authentication configuration

        Raises:
            AccentAPIError: If the request fails

        """
        headers = self._get_headers(tenant_uuid=tenant_uuid)
        url = self._build_config_url(auth_type)

        r = await self.async_client.get(url, headers=headers)

        try:
            r.raise_for_status()
        except httpx.HTTPStatusError:
            logger.error(
                "Failed to get external auth config for auth type: %s", auth_type
            )
            self.raise_from_response(r)

        return cast(JSON, r.json())

    def get_config(self, auth_type: str, tenant_uuid: str | None = None) -> JSON:
        """Get an external authentication configuration.

        Args:
            auth_type: Authentication type
            tenant_uuid: Optional tenant identifier

        Returns:
            JSON: Authentication configuration

        Raises:
            AccentAPIError: If the request fails

        """
        headers = self._get_headers(tenant_uuid=tenant_uuid)
        url = self._build_config_url(auth_type)

        r = self.sync_client.get(url, headers=headers)

        if r.status_code != 200:
            logger.error(
                "Failed to get external auth config for auth type: %s", auth_type
            )
            self.raise_from_response(r)

        return cast(JSON, r.json())

    async def list_async(self, user_uuid: str, **kwargs: Any) -> JSON:
        """List external authentication entries for a user asynchronously.

        Args:
            user_uuid: User identifier
            **kwargs: Additional parameters

        Returns:
            JSON: List of authentication entries

        Raises:
            AccentAPIError: If the request fails

        """
        headers = self._get_headers()
        url = "/".join([self.base_url, user_uuid, "external"])

        r = await self.async_client.get(url, headers=headers, params=kwargs)

        try:
            r.raise_for_status()
        except httpx.HTTPStatusError:
            logger.error("Failed to list external auth for user: %s", user_uuid)
            self.raise_from_response(r)

        return cast(JSON, r.json())

    def list_(self, user_uuid: str, **kwargs: Any) -> JSON:
        """List external authentication entries for a user.

        Args:
            user_uuid: User identifier
            **kwargs: Additional parameters

        Returns:
            JSON: List of authentication entries

        Raises:
            AccentAPIError: If the request fails

        """
        headers = self._get_headers()
        url = "/".join([self.base_url, user_uuid, "external"])

        r = self.sync_client.get(url, headers=headers, params=kwargs)

        if r.status_code != 200:
            logger.error("Failed to list external auth for user: %s", user_uuid)
            self.raise_from_response(r)

        return cast(JSON, r.json())

    async def list_connected_users_async(self, auth_type: str, **kwargs: Any) -> JSON:
        """List users connected to an authentication type asynchronously.

        Args:
            auth_type: Authentication type
            **kwargs: Additional parameters

        Returns:
            JSON: List of connected users

        Raises:
            AccentAPIError: If the request fails

        """
        headers = self._get_headers()
        url = "/".join([self._client.url("external"), auth_type, "users"])

        r = await self.async_client.get(url, headers=headers, params=kwargs)

        try:
            r.raise_for_status()
        except httpx.HTTPStatusError:
            logger.error("Failed to list connected users for auth type: %s", auth_type)
            self.raise_from_response(r)

        return cast(JSON, r.json())

    def list_connected_users(self, auth_type: str, **kwargs: Any) -> JSON:
        """List users connected to an authentication type.

        Args:
            auth_type: Authentication type
            **kwargs: Additional parameters

        Returns:
            JSON: List of connected users

        Raises:
            AccentAPIError: If the request fails

        """
        headers = self._get_headers()
        url = "/".join([self._client.url("external"), auth_type, "users"])

        r = self.sync_client.get(url, headers=headers, params=kwargs)

        if r.status_code != 200:
            logger.error("Failed to list connected users for auth type: %s", auth_type)
            self.raise_from_response(r)

        return cast(JSON, r.json())

    async def update_async(
        self, auth_type: str, user_uuid: str, data: dict[str, JSON]
    ) -> JSON:
        """Update an external authentication entry asynchronously.

        Args:
            auth_type: Authentication type
            user_uuid: User identifier
            data: Updated authentication data

        Returns:
            JSON: Updated authentication entry

        Raises:
            AccentAPIError: If the request fails

        """
        headers = self._get_headers()
        url = self._build_url(auth_type, user_uuid)

        r = await self.async_client.put(url, headers=headers, json=data)

        try:
            r.raise_for_status()
        except httpx.HTTPStatusError:
            logger.error(
                "Failed to update external auth for user: %s, auth type: %s",
                user_uuid,
                auth_type,
            )
            self.raise_from_response(r)

        return cast(JSON, r.json())

    def update(self, auth_type: str, user_uuid: str, data: dict[str, JSON]) -> JSON:
        """Update an external authentication entry.

        Args:
            auth_type: Authentication type
            user_uuid: User identifier
            data: Updated authentication data

        Returns:
            JSON: Updated authentication entry

        Raises:
            AccentAPIError: If the request fails

        """
        headers = self._get_headers()
        url = self._build_url(auth_type, user_uuid)

        r = self.sync_client.put(url, headers=headers, json=data)

        if r.status_code != 200:
            logger.error(
                "Failed to update external auth for user: %s, auth type: %s",
                user_uuid,
                auth_type,
            )
            self.raise_from_response(r)

        return cast(JSON, r.json())

    async def update_config_async(
        self, auth_type: str, data: dict[str, JSON], tenant_uuid: str | None = None
    ) -> None:
        """Update an external authentication configuration asynchronously.

        Args:
            auth_type: Authentication type
            data: Updated configuration data
            tenant_uuid: Optional tenant identifier

        Raises:
            AccentAPIError: If the request fails

        """
        headers = self._get_headers(tenant_uuid=tenant_uuid)
        url = self._build_config_url(auth_type)

        r = await self.async_client.put(url, headers=headers, json=data)

        try:
            r.raise_for_status()
        except httpx.HTTPStatusError as e:
            if r.status_code != 204:
                logger.error(
                    "Failed to update external auth config: %s, status code: %s",
                    str(e),
                    r.status_code,
                )
                self.raise_from_response(r)

    def update_config(
        self, auth_type: str, data: dict[str, JSON], tenant_uuid: str | None = None
    ) -> None:
        """Update an external authentication configuration.

        Args:
            auth_type: Authentication type
            data: Updated configuration data
            tenant_uuid: Optional tenant identifier

        Raises:
            AccentAPIError: If the request fails

        """
        headers = self._get_headers(tenant_uuid=tenant_uuid)
        url = self._build_config_url(auth_type)

        r = self.sync_client.put(url, headers=headers, json=data)

        if r.status_code != 204:
            logger.error(
                "Failed to update external auth config for auth type: %s", auth_type
            )
            self.raise_from_response(r)

    def _build_url(self, auth_type: str, user_uuid: str) -> str:
        """Build a URL for user-specific external authentication operations.

        Args:
            auth_type: Authentication type
            user_uuid: User identifier

        Returns:
            str: Complete URL

        """
        return "/".join([self.base_url, user_uuid, "external", auth_type])

    def _build_config_url(self, auth_type: str) -> str:
        """Build a URL for external authentication configuration operations.

        Args:
            auth_type: Authentication type

        Returns:
            str: Complete URL

        """
        return "/".join([self._client.url("external"), auth_type, "config"])
