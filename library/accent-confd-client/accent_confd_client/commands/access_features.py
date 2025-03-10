# Copyright 2025 Accent Communications

"""Access features command module for the Configuration Daemon API."""

import logging
from typing import Any

from accent_confd_client.crud import CRUDCommand

# Configure standard logging
logger = logging.getLogger(__name__)


class AccessFeaturesCommand(CRUDCommand):
    """Command for managing access features."""

    resource = "access_features"

    async def list_async(self, **kwargs: Any) -> dict[str, Any]:
        """List access features asynchronously.

        Args:
            **kwargs: Query parameters

        Returns:
            List of access features

        """
        return await super().list_async(**kwargs)

    async def get_async(self, resource_id: str) -> dict[str, Any]:
        """Get an access feature by ID asynchronously.

        Args:
            resource_id: Access feature ID

        Returns:
            Access feature data

        """
        return await super().get_async(resource_id)

    async def create_async(self, body: dict[str, Any]) -> dict[str, Any]:
        """Create an access feature asynchronously.

        Args:
            body: Access feature data

        Returns:
            Created access feature data

        """
        return await super().create_async(body)

    async def update_async(self, body: dict[str, Any]) -> None:
        """Update an access feature asynchronously.

        Args:
            body: Access feature data

        """
        await super().update_async(body)

    async def delete_async(self, resource_id: str) -> None:
        """Delete an access feature asynchronously.

        Args:
            resource_id: Access feature ID

        """
        await super().delete_async(resource_id)
