# Copyright 2025 Accent Communications

"""Outcalls command module for the Configuration Daemon API."""

import logging
from typing import Any

from accent_confd_client.crud import MultiTenantCommand
from accent_confd_client.relations import (
    OutcallCallPermissionRelation,
    OutcallExtensionRelation,
    OutcallScheduleRelation,
    OutcallTrunkRelation,
)
from accent_confd_client.util import extract_id

# Configure standard logging
logger = logging.getLogger(__name__)


class OutcallRelation:
    """Relations for outcalls."""

    def __init__(self, builder: Any, outcall_id: str) -> None:
        """Initialize outcall relations.

        Args:
            builder: Client instance
            outcall_id: Outcall ID

        """
        self.outcall_id = outcall_id
        self.outcall_call_permission = OutcallCallPermissionRelation(builder)
        self.outcall_schedule = OutcallScheduleRelation(builder)
        self.outcall_trunk = OutcallTrunkRelation(builder)
        self.outcall_extension = OutcallExtensionRelation(builder)

    def update_trunks(self, trunks: list[dict[str, Any]]) -> Any:
        """Update trunks for the outcall.

        Args:
            trunks: List of trunks

        Returns:
            API response

        """
        return self.outcall_trunk.associate(self.outcall_id, trunks)

    async def update_trunks_async(self, trunks: list[dict[str, Any]]) -> Any:
        """Update trunks for the outcall asynchronously.

        Args:
            trunks: List of trunks

        Returns:
            API response

        """
        return await self.outcall_trunk.associate_async(self.outcall_id, trunks)

    @extract_id
    def add_extension(self, extension_id: str, **kwargs: Any) -> Any:
        """Add an extension to the outcall.

        Args:
            extension_id: Extension ID
            **kwargs: Additional parameters

        Returns:
            API response

        """
        return self.outcall_extension.associate(self.outcall_id, extension_id, **kwargs)

    @extract_id
    async def add_extension_async(self, extension_id: str, **kwargs: Any) -> Any:
        """Add an extension to the outcall asynchronously.

        Args:
            extension_id: Extension ID
            **kwargs: Additional parameters

        Returns:
            API response

        """
        return await self.outcall_extension.associate_async(
            self.outcall_id, extension_id, **kwargs
        )

    @extract_id
    def remove_extension(self, extension_id: str) -> Any:
        """Remove an extension from the outcall.

        Args:
            extension_id: Extension ID

        Returns:
            API response

        """
        return self.outcall_extension.dissociate(self.outcall_id, extension_id)

    @extract_id
    async def remove_extension_async(self, extension_id: str) -> Any:
        """Remove an extension from the outcall asynchronously.

        Args:
            extension_id: Extension ID

        Returns:
            API response

        """
        return await self.outcall_extension.dissociate_async(
            self.outcall_id, extension_id
        )

    @extract_id
    def add_schedule(self, schedule_id: str) -> Any:
        """Add a schedule to the outcall.

        Args:
            schedule_id: Schedule ID

        Returns:
            API response

        """
        return self.outcall_schedule.associate(self.outcall_id, schedule_id)

    @extract_id
    async def add_schedule_async(self, schedule_id: str) -> Any:
        """Add a schedule to the outcall asynchronously.

        Args:
            schedule_id: Schedule ID

        Returns:
            API response

        """
        return await self.outcall_schedule.associate_async(self.outcall_id, schedule_id)

    @extract_id
    def remove_schedule(self, schedule_id: str) -> Any:
        """Remove a schedule from the outcall.

        Args:
            schedule_id: Schedule ID

        Returns:
            API response

        """
        return self.outcall_schedule.dissociate(self.outcall_id, schedule_id)

    @extract_id
    async def remove_schedule_async(self, schedule_id: str) -> Any:
        """Remove a schedule from the outcall asynchronously.

        Args:
            schedule_id: Schedule ID

        Returns:
            API response

        """
        return await self.outcall_schedule.dissociate_async(
            self.outcall_id, schedule_id
        )

    @extract_id
    def add_call_permission(self, call_permission_id: str) -> Any:
        """Add a call permission to the outcall.

        Args:
            call_permission_id: Call permission ID

        Returns:
            API response

        """
        return self.outcall_call_permission.associate(
            self.outcall_id, call_permission_id
        )

    @extract_id
    async def add_call_permission_async(self, call_permission_id: str) -> Any:
        """Add a call permission to the outcall asynchronously.

        Args:
            call_permission_id: Call permission ID

        Returns:
            API response

        """
        return await self.outcall_call_permission.associate_async(
            self.outcall_id, call_permission_id
        )

    @extract_id
    def remove_call_permission(self, call_permission_id: str) -> None:
        """Remove a call permission from the outcall.

        Args:
            call_permission_id: Call permission ID

        """
        self.outcall_call_permission.dissociate(self.outcall_id, call_permission_id)

    @extract_id
    async def remove_call_permission_async(self, call_permission_id: str) -> None:
        """Remove a call permission from the outcall asynchronously.

        Args:
            call_permission_id: Call permission ID

        """
        await self.outcall_call_permission.dissociate_async(
            self.outcall_id, call_permission_id
        )


class OutcallsCommand(MultiTenantCommand):
    """Command for managing outcalls."""

    resource = "outcalls"
    relation_cmd = OutcallRelation
