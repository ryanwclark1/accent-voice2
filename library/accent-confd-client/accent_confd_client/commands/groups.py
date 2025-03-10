# Copyright 2025 Accent Communications

"""Groups command module for the Configuration Daemon API."""

import logging
from typing import Any

from accent_confd_client.crud import MultiTenantCommand
from accent_confd_client.relations import (
    GroupCallPermissionRelation,
    GroupExtensionRelation,
    GroupFallbackRelation,
    GroupMemberExtensionRelation,
    GroupMemberUserRelation,
    GroupScheduleRelation,
)
from accent_confd_client.util import extract_id

# Configure standard logging
logger = logging.getLogger(__name__)


class GroupRelation:
    """Relations for groups."""

    def __init__(self, builder: Any, group_id: str) -> None:
        """Initialize group relations.

        Args:
            builder: Client instance
            group_id: Group ID

        """
        self.group_id = group_id
        self.group_call_permission = GroupCallPermissionRelation(builder)
        self.group_extension = GroupExtensionRelation(builder)
        self.group_user_members = GroupMemberUserRelation(builder)
        self.group_extension_members = GroupMemberExtensionRelation(builder)
        self.group_fallback = GroupFallbackRelation(builder)
        self.group_schedule = GroupScheduleRelation(builder)

    def update_user_members(self, users: list[dict[str, Any]]) -> Any:
        """Update user members for the group.

        Args:
            users: List of users

        Returns:
            API response

        """
        return self.group_user_members.associate(self.group_id, users)

    async def update_user_members_async(self, users: list[dict[str, Any]]) -> Any:
        """Update user members for the group asynchronously.

        Args:
            users: List of users

        Returns:
            API response

        """
        return await self.group_user_members.associate_async(self.group_id, users)

    def update_extension_members(self, extensions: list[dict[str, Any]]) -> Any:
        """Update extension members for the group.

        Args:
            extensions: List of extensions

        Returns:
            API response

        """
        return self.group_extension_members.associate(self.group_id, extensions)

    async def update_extension_members_async(
        self, extensions: list[dict[str, Any]]
    ) -> Any:
        """Update extension members for the group asynchronously.

        Args:
            extensions: List of extensions

        Returns:
            API response

        """
        return await self.group_extension_members.associate_async(
            self.group_id, extensions
        )

    @extract_id
    def add_extension(self, extension_id: str) -> Any:
        """Add an extension to the group.

        Args:
            extension_id: Extension ID

        Returns:
            API response

        """
        return self.group_extension.associate(self.group_id, extension_id)

    @extract_id
    async def add_extension_async(self, extension_id: str) -> Any:
        """Add an extension to the group asynchronously.

        Args:
            extension_id: Extension ID

        Returns:
            API response

        """
        return await self.group_extension.associate_async(self.group_id, extension_id)

    @extract_id
    def remove_extension(self, extension_id: str) -> Any:
        """Remove an extension from the group.

        Args:
            extension_id: Extension ID

        Returns:
            API response

        """
        return self.group_extension.dissociate(self.group_id, extension_id)

    @extract_id
    async def remove_extension_async(self, extension_id: str) -> Any:
        """Remove an extension from the group asynchronously.

        Args:
            extension_id: Extension ID

        Returns:
            API response

        """
        return await self.group_extension.dissociate_async(self.group_id, extension_id)

    def update_fallbacks(self, fallbacks: dict[str, Any]) -> None:
        """Update fallbacks for the group.

        Args:
            fallbacks: Fallbacks data

        """
        self.group_fallback.update_fallbacks(self.group_id, fallbacks)

    async def update_fallbacks_async(self, fallbacks: dict[str, Any]) -> None:
        """Update fallbacks for the group asynchronously.

        Args:
            fallbacks: Fallbacks data

        """
        await self.group_fallback.update_fallbacks_async(self.group_id, fallbacks)

    def list_fallbacks(self) -> dict[str, Any]:
        """List fallbacks for the group.

        Returns:
            Fallbacks data

        """
        return self.group_fallback.list_fallbacks(self.group_id)

    async def list_fallbacks_async(self) -> dict[str, Any]:
        """List fallbacks for the group asynchronously.

        Returns:
            Fallbacks data

        """
        return await self.group_fallback.list_fallbacks_async(self.group_id)

    @extract_id
    def add_schedule(self, schedule_id: str) -> Any:
        """Add a schedule to the group.

        Args:
            schedule_id: Schedule ID

        Returns:
            API response

        """
        return self.group_schedule.associate(self.group_id, schedule_id)

    @extract_id
    async def add_schedule_async(self, schedule_id: str) -> Any:
        """Add a schedule to the group asynchronously.

        Args:
            schedule_id: Schedule ID

        Returns:
            API response

        """
        return await self.group_schedule.associate_async(self.group_id, schedule_id)

    @extract_id
    def remove_schedule(self, schedule_id: str) -> Any:
        """Remove a schedule from the group.

        Args:
            schedule_id: Schedule ID

        Returns:
            API response

        """
        return self.group_schedule.dissociate(self.group_id, schedule_id)

    @extract_id
    async def remove_schedule_async(self, schedule_id: str) -> Any:
        """Remove a schedule from the group asynchronously.

        Args:
            schedule_id: Schedule ID

        Returns:
            API response

        """
        return await self.group_schedule.dissociate_async(self.group_id, schedule_id)

    @extract_id
    def add_call_permission(self, call_permission_id: str) -> Any:
        """Add a call permission to the group.

        Args:
            call_permission_id: Call permission ID

        Returns:
            API response

        """
        return self.group_call_permission.associate(self.group_id, call_permission_id)

    @extract_id
    async def add_call_permission_async(self, call_permission_id: str) -> Any:
        """Add a call permission to the group asynchronously.

        Args:
            call_permission_id: Call permission ID

        Returns:
            API response

        """
        return await self.group_call_permission.associate_async(
            self.group_id, call_permission_id
        )

    @extract_id
    def remove_call_permission(self, call_permission_id: str) -> None:
        """Remove a call permission from the group.

        Args:
            call_permission_id: Call permission ID

        """
        self.group_call_permission.dissociate(self.group_id, call_permission_id)

    @extract_id
    async def remove_call_permission_async(self, call_permission_id: str) -> None:
        """Remove a call permission from the group asynchronously.

        Args:
            call_permission_id: Call permission ID

        """
        await self.group_call_permission.dissociate_async(
            self.group_id, call_permission_id
        )


class GroupsCommand(MultiTenantCommand):
    """Command for managing groups."""

    resource = "groups"
    relation_cmd = GroupRelation
