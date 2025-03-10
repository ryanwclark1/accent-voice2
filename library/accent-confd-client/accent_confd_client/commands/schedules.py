# Copyright 2025 Accent Communications

"""Schedules command module for the Configuration Daemon API."""

import logging
from typing import Any

from accent_confd_client.crud import MultiTenantCommand

# Configure standard logging
logger = logging.getLogger(__name__)


class SchedulesCommand(MultiTenantCommand):
    """Command for managing schedules."""

    resource = "schedules"

    async def list_async(self, **kwargs: Any) -> dict[str, Any]:
        """List schedules asynchronously.

        Args:
            **kwargs: Query parameters

        Returns:
            List of schedules

        """
        return await super().list_async(**kwargs)

    async def get_async(self, resource_id: str, **kwargs: Any) -> dict[str, Any]:
        """Get a schedule by ID asynchronously.

        Args:
            resource_id: Schedule ID
            **kwargs: Additional parameters

        Returns:
            Schedule data

        """
        return await super().get_async(resource_id, **kwargs)

    async def create_async(self, body: dict[str, Any], **kwargs: Any) -> dict[str, Any]:
        """Create a schedule asynchronously.

        Args:
            body: Schedule data
            **kwargs: Additional parameters

        Returns:
            Created schedule data

        """
        return await super().create_async(body, **kwargs)

    async def update_async(self, body: dict[str, Any]) -> None:
        """Update a schedule asynchronously.

        Args:
            body: Schedule data

        """
        await super().update_async(body)

    async def delete_async(self, resource_id: str) -> None:
        """Delete a schedule asynchronously.

        Args:
            resource_id: Schedule ID

        """
        await super().delete_async(resource_id)
