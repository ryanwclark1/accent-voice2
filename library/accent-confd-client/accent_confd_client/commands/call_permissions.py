# Copyright 2025 Accent Communications

"""Call permissions command module for the Configuration Daemon API."""

import logging
from typing import Any

from accent_confd_client.crud import MultiTenantCommand
from accent_confd_client.relations import UserCallPermissionRelation
from accent_confd_client.util import extract_id

# Configure standard logging
logger = logging.getLogger(__name__)


class CallPermissionRelation:
    """Relations for call permissions."""

    def __init__(self, builder: Any, call_permission_id: str) -> None:
        """Initialize call permission relations.

        Args:
            builder: Client instance
            call_permission_id: Call permission ID

        """
        self.call_permission_id = call_permission_id
        self.user_call_permission = UserCallPermissionRelation(builder)

    @extract_id
    def add_user(self, user_id: str) -> Any:
        """Add a user to the call permission.

        Args:
            user_id: User ID

        Returns:
            API response

        """
        return self.user_call_permission.associate(user_id, self.call_permission_id)

    @extract_id
    async def add_user_async(self, user_id: str) -> Any:
        """Add a user to the call permission asynchronously.

        Args:
            user_id: User ID

        Returns:
            API response

        """
        return await self.user_call_permission.associate_async(
            user_id, self.call_permission_id
        )

    @extract_id
    def remove_user(self, user_id: str) -> Any:
        """Remove a user from the call permission.

        Args:
            user_id: User ID

        Returns:
            API response

        """
        return self.user_call_permission.dissociate(user_id, self.call_permission_id)

    @extract_id
    async def remove_user_async(self, user_id: str) -> Any:
        """Remove a user from the call permission asynchronously.

        Args:
            user_id: User ID

        Returns:
            API response

        """
        return await self.user_call_permission.dissociate_async(
            user_id, self.call_permission_id
        )


class CallPermissionsCommand(MultiTenantCommand):
    """Command for managing call permissions."""

    resource = "callpermissions"
    relation_cmd = CallPermissionRelation

    async def list_async(self, **kwargs: Any) -> dict[str, Any]:
        """List call permissions asynchronously.

        Args:
            **kwargs: Query parameters

        Returns:
            List of call permissions

        """
        return await super().list_async(**kwargs)

    async def get_async(self, resource_id: str, **kwargs: Any) -> dict[str, Any]:
        """Get a call permission by ID asynchronously.

        Args:
            resource_id: Call permission ID
            **kwargs: Additional parameters

        Returns:
            Call permission data

        """
        return await super().get_async(resource_id, **kwargs)

    async def create_async(self, body: dict[str, Any], **kwargs: Any) -> dict[str, Any]:
        """Create a call permission asynchronously.

        Args:
            body: Call permission data
            **kwargs: Additional parameters

        Returns:
            Created call permission data

        """
        return await super().create_async(body, **kwargs)

    async def update_async(self, body: dict[str, Any]) -> None:
        """Update a call permission asynchronously.

        Args:
            body: Call permission data

        """
        await super().update_async(body)

    async def delete_async(self, resource_id: str) -> None:
        """Delete a call permission asynchronously.

        Args:
            resource_id: Call permission ID

        """
        await super().delete_async(resource_id)
