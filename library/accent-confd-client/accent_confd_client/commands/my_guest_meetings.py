# Copyright 2025 Accent Communications

"""My guest meetings command module for the Configuration Daemon API."""

import logging
from typing import Any

from accent_confd_client.crud import MultiTenantCommand

# Configure standard logging
logger = logging.getLogger(__name__)


class GuestsMeMeetingsCommand(MultiTenantCommand):
    """Command for managing the current guest's meetings."""

    resource = "guests/me/meetings"

    async def list_async(self, **kwargs: Any) -> dict[str, Any]:
        """List the current guest's meetings asynchronously.

        Args:
            **kwargs: Query parameters

        Returns:
            List of meetings

        """
        return await super().list_async(**kwargs)

    async def get_async(self, resource_id: str, **kwargs: Any) -> dict[str, Any]:
        """Get a meeting by ID asynchronously.

        Args:
            resource_id: Meeting ID
            **kwargs: Additional parameters

        Returns:
            Meeting data

        """
        return await super().get_async(resource_id, **kwargs)

    async def create_async(self, body: dict[str, Any], **kwargs: Any) -> dict[str, Any]:
        """Create a meeting asynchronously.

        Args:
            body: Meeting data
            **kwargs: Additional parameters

        Returns:
            Created meeting data

        """
        return await super().create_async(body, **kwargs)

    async def update_async(self, body: dict[str, Any]) -> None:
        """Update a meeting asynchronously.

        Args:
            body: Meeting data

        """
        await super().update_async(body)

    async def delete_async(self, resource_id: str) -> None:
        """Delete a meeting asynchronously.

        Args:
            resource_id: Meeting ID

        """
        await super().delete_async(resource_id)
