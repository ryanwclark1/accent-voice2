# Copyright 2025 Accent Communications

"""Commands for managing user presence information."""

import logging
from typing import Any

from .helpers.base import BaseCommand

logger = logging.getLogger(__name__)


class UserPresenceCommand(BaseCommand):
    """Command for managing user presence information."""

    resource = "users"

    async def list_async(self, **params: Any) -> list[dict[str, Any]]:
        """List user presences asynchronously.

        Args:
            **params: Query parameters, can include user_uuids

        Returns:
            List of user presence information

        Raises:
            ChatdError: If the API request fails

        """
        headers = self._get_headers(**params)
        if user_uuids := params.pop("user_uuids", None):
            params["user_uuid"] = ",".join(user_uuids)

        url = f"{self.base_url}/presences"
        response = await self.async_client.get(url, headers=headers, params=params)
        self.raise_from_response(response)
        return response.json()

    def list(self, **params: Any) -> list[dict[str, Any]]:
        """List user presences.

        Args:
            **params: Query parameters, can include user_uuids

        Returns:
            List of user presence information

        Raises:
            ChatdError: If the API request fails

        """
        headers = self._get_headers(**params)
        if user_uuids := params.pop("user_uuids", None):
            params["user_uuid"] = ",".join(user_uuids)

        url = f"{self.base_url}/presences"
        response = self.sync_client.get(url, headers=headers, params=params)
        self.raise_from_response(response)
        return response.json()

    async def get_async(
        self, user_uuid: str, tenant_uuid: str | None = None
    ) -> dict[str, Any]:
        """Get presence for a specific user asynchronously.

        Args:
            user_uuid: UUID of the user
            tenant_uuid: Optional tenant UUID

        Returns:
            User presence information

        Raises:
            ChatdError: If the API request fails

        """
        headers = self._get_headers(tenant_uuid=tenant_uuid)
        url = f"{self.base_url}/{user_uuid}/presences"
        response = await self.async_client.get(url, headers=headers)
        self.raise_from_response(response)
        return response.json()

    def get(self, user_uuid: str, tenant_uuid: str | None = None) -> dict[str, Any]:
        """Get presence for a specific user.

        Args:
            user_uuid: UUID of the user
            tenant_uuid: Optional tenant UUID

        Returns:
            User presence information

        Raises:
            ChatdError: If the API request fails

        """
        headers = self._get_headers(tenant_uuid=tenant_uuid)
        url = f"{self.base_url}/{user_uuid}/presences"
        response = self.sync_client.get(url, headers=headers)
        self.raise_from_response(response)
        return response.json()

    async def update_async(
        self, user_args: dict[str, Any], tenant_uuid: str | None = None
    ) -> None:
        """Update user presence asynchronously.

        Args:
            user_args: User presence data to update
            tenant_uuid: Optional tenant UUID

        Raises:
            ChatdError: If the API request fails

        """
        user_uuid = user_args["uuid"]
        headers = self._get_headers(tenant_uuid=tenant_uuid)
        url = f"{self.base_url}/{user_uuid}/presences"
        response = await self.async_client.put(url, json=user_args, headers=headers)
        self.raise_from_response(response)

    def update(
        self, user_args: dict[str, Any], tenant_uuid: str | None = None
    ) -> None:
        """Update user presence.

        Args:
            user_args: User presence data to update
            tenant_uuid: Optional tenant UUID

        Raises:
            ChatdError: If the API request fails

        """
        user_uuid = user_args["uuid"]
        headers = self._get_headers(tenant_uuid=tenant_uuid)
        url = f"{self.base_url}/{user_uuid}/presences"
        response = self.sync_client.put(url, json=user_args, headers=headers)
        self.raise_from_response(response)
