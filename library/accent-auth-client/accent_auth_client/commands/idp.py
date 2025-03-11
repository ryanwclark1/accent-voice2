# Copyright 2025 Accent Communications

from __future__ import annotations

import logging
from typing import cast

import httpx
from accent_lib_rest_client import RESTCommand

from accent_auth_client.type_definitions import JSON

logger = logging.getLogger(__name__)


class IDPCommand(RESTCommand):
    """Command for identity provider operations.

    Provides methods for managing identity providers and user associations.
    """

    resource = "idp"
    _ro_headers = {"Accept": "application/json"}

    async def list_async(self) -> JSON:
        """List available identity providers asynchronously.

        Returns:
            JSON: List of identity providers

        Raises:
            AccentAPIError: If the request fails

        """
        headers = self._get_headers()

        r = await self.async_client.get(self.base_url, headers=headers)

        try:
            r.raise_for_status()
        except httpx.HTTPStatusError:
            logger.error("Failed to list identity providers")
            self.raise_from_response(r)

        return cast(JSON, r.json())

    def list(self) -> JSON:
        """List available identity providers.

        Returns:
            JSON: List of identity providers

        Raises:
            AccentAPIError: If the request fails

        """
        headers = self._get_headers()

        r = self.sync_client.get(self.base_url, headers=headers)

        if r.status_code != 200:
            logger.error("Failed to list identity providers")
            self.raise_from_response(r)

        return cast(JSON, r.json())

    async def add_user_async(self, idp_type: str, user_uuid: str) -> None:
        """Add a user to an identity provider asynchronously.

        Args:
            idp_type: Identity provider type
            user_uuid: User identifier

        Raises:
            AccentAPIError: If the request fails

        """
        headers = self._get_headers()
        url = self._relation_url("users", idp_type, user_uuid)

        r = await self.async_client.put(url, headers=headers)

        try:
            r.raise_for_status()
        except httpx.HTTPStatusError as e:
            if r.status_code != 204:
                logger.error(
                    "Failed to add user to IDP: %s, status code: %s",
                    str(e),
                    r.status_code,
                )
                self.raise_from_response(r)

    def add_user(self, idp_type: str, user_uuid: str) -> None:
        """Add a user to an identity provider.

        Args:
            idp_type: Identity provider type
            user_uuid: User identifier

        Raises:
            AccentAPIError: If the request fails

        """
        headers = self._get_headers()
        url = self._relation_url("users", idp_type, user_uuid)

        r = self.sync_client.put(url, headers=headers)

        if r.status_code != 204:
            logger.error("Failed to add user to IDP: %s", idp_type)
            self.raise_from_response(r)

    async def add_users_async(self, idp_type: str, users: JSON) -> None:
        """Add multiple users to an identity provider asynchronously.

        Args:
            idp_type: Identity provider type
            users: List of user data

        Raises:
            AccentAPIError: If the request fails

        """
        headers = self._get_headers()
        url = self._relation_url("users", idp_type)

        r = await self.async_client.put(url, headers=headers, json={"users": users})

        try:
            r.raise_for_status()
        except httpx.HTTPStatusError as e:
            if r.status_code != 204:
                logger.error(
                    "Failed to add users to IDP: %s, status code: %s",
                    str(e),
                    r.status_code,
                )
                self.raise_from_response(r)

    def add_users(self, idp_type: str, users: JSON) -> None:
        """Add multiple users to an identity provider.

        Args:
            idp_type: Identity provider type
            users: List of user data

        Raises:
            AccentAPIError: If the request fails

        """
        headers = self._get_headers()
        url = self._relation_url("users", idp_type)

        r = self.sync_client.put(url, headers=headers, json={"users": users})

        if r.status_code != 204:
            logger.error("Failed to add users to IDP: %s", idp_type)
            self.raise_from_response(r)

    async def remove_user_async(self, idp_type: str, user_uuid: str) -> None:
        """Remove a user from an identity provider asynchronously.

        Args:
            idp_type: Identity provider type
            user_uuid: User identifier

        Raises:
            AccentAPIError: If the request fails

        """
        headers = self._get_headers()
        url = self._relation_url("users", idp_type, user_uuid)

        r = await self.async_client.delete(url, headers=headers)

        try:
            r.raise_for_status()
        except httpx.HTTPStatusError as e:
            if r.status_code != 204:
                logger.error(
                    "Failed to remove user from IDP: %s, status code: %s",
                    str(e),
                    r.status_code,
                )
                self.raise_from_response(r)

    def remove_user(self, idp_type: str, user_uuid: str) -> None:
        """Remove a user from an identity provider.

        Args:
            idp_type: Identity provider type
            user_uuid: User identifier

        Raises:
            AccentAPIError: If the request fails

        """
        headers = self._get_headers()
        url = self._relation_url("users", idp_type, user_uuid)

        r = self.sync_client.delete(url, headers=headers)

        if r.status_code != 204:
            logger.error("Failed to remove user from IDP: %s", idp_type)
            self.raise_from_response(r)

    def _relation_url(
        self,
        resource: str,
        idp_type: str,
        resource_uuid: str | None = None,
    ) -> str:
        """Build a URL for identity provider relation operations.

        Args:
            resource: Resource type (e.g., 'users')
            idp_type: Identity provider type
            resource_uuid: Optional resource identifier

        Returns:
            str: Complete URL

        """
        if resource_uuid:
            return "/".join([self.base_url, idp_type, resource, resource_uuid])
        return "/".join([self.base_url, idp_type, resource])
