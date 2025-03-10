# Copyright 2025 Accent Communications

"""Applications command module for the Configuration Daemon API."""

import logging
from typing import Any

from accent_confd_client.crud import MultiTenantCommand

# Configure standard logging
logger = logging.getLogger(__name__)


class ApplicationsCommand(MultiTenantCommand):
    """Command for managing applications."""

    resource = "applications"

    async def list_async(self, **kwargs: Any) -> dict[str, Any]:
        """List applications asynchronously.

        Args:
            **kwargs: Query parameters

        Returns:
            List of applications

        """
        return await super().list_async(**kwargs)

    async def get_async(self, resource_id: str, **kwargs: Any) -> dict[str, Any]:
        """Get an application by ID asynchronously.

        Args:
            resource_id: Application ID
            **kwargs: Additional parameters

        Returns:
            Application data

        """
        return await super().get_async(resource_id, **kwargs)

    async def create_async(self, body: dict[str, Any], **kwargs: Any) -> dict[str, Any]:
        """Create an application asynchronously.

        Args:
            body: Application data
            **kwargs: Additional parameters

        Returns:
            Created application data

        """
        return await super().create_async(body, **kwargs)

    async def update_async(self, body: dict[str, Any]) -> None:
        """Update an application asynchronously.

        Args:
            body: Application data

        """
        await super().update_async(body)

    async def delete_async(self, resource_id: str) -> None:
        """Delete an application asynchronously.

        Args:
            resource_id: Application ID

        """
        await super().delete_async(resource_id)
