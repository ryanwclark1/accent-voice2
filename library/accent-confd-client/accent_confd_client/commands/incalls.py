# Copyright 2025 Accent Communications

"""Incalls command module for the Configuration Daemon API."""

import logging
from typing import Any

from accent_confd_client.crud import MultiTenantCommand
from accent_confd_client.relations import (
    IncallExtensionRelation,
    IncallScheduleRelation,
)
from accent_confd_client.util import extract_id

# Configure standard logging
logger = logging.getLogger(__name__)


class IncallRelation:
    """Relations for incalls."""

    def __init__(self, builder: Any, incall_id: str) -> None:
        """Initialize incall relations.

        Args:
            builder: Client instance
            incall_id: Incall ID

        """
        self.incall_id = incall_id
        self.incall_extension = IncallExtensionRelation(builder)
        self.incall_schedule = IncallScheduleRelation(builder)

    @extract_id
    def add_extension(self, extension_id: str) -> Any:
        """Add an extension to the incall.

        Args:
            extension_id: Extension ID

        Returns:
            API response

        """
        return self.incall_extension.associate(self.incall_id, extension_id)

    @extract_id
    async def add_extension_async(self, extension_id: str) -> Any:
        """Add an extension to the incall asynchronously.

        Args:
            extension_id: Extension ID

        Returns:
            API response

        """
        return await self.incall_extension.associate_async(self.incall_id, extension_id)

    @extract_id
    def remove_extension(self, extension_id: str) -> Any:
        """Remove an extension from the incall.

        Args:
            extension_id: Extension ID

        Returns:
            API response

        """
        return self.incall_extension.dissociate(self.incall_id, extension_id)

    @extract_id
    async def remove_extension_async(self, extension_id: str) -> Any:
        """Remove an extension from the incall asynchronously.

        Args:
            extension_id: Extension ID

        Returns:
            API response

        """
        return await self.incall_extension.dissociate_async(
            self.incall_id, extension_id
        )

    @extract_id
    def add_schedule(self, schedule_id: str) -> Any:
        """Add a schedule to the incall.

        Args:
            schedule_id: Schedule ID

        Returns:
            API response

        """
        return self.incall_schedule.associate(self.incall_id, schedule_id)

    @extract_id
    async def add_schedule_async(self, schedule_id: str) -> Any:
        """Add a schedule to the incall asynchronously.

        Args:
            schedule_id: Schedule ID

        Returns:
            API response

        """
        return await self.incall_schedule.associate_async(self.incall_id, schedule_id)

    @extract_id
    def remove_schedule(self, schedule_id: str) -> Any:
        """Remove a schedule from the incall.

        Args:
            schedule_id: Schedule ID

        Returns:
            API response

        """
        return self.incall_schedule.dissociate(self.incall_id, schedule_id)

    @extract_id
    async def remove_schedule_async(self, schedule_id: str) -> Any:
        """Remove a schedule from the incall asynchronously.

        Args:
            schedule_id: Schedule ID

        Returns:
            API response

        """
        return await self.incall_schedule.dissociate_async(self.incall_id, schedule_id)


class IncallsCommand(MultiTenantCommand):
    """Command for managing incalls."""

    resource = "incalls"
    relation_cmd = IncallRelation
