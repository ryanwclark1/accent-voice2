# Copyright 2025 Accent Communications

"""IVR command module for the Configuration Daemon API."""

import logging
from typing import Any

from accent_confd_client.crud import MultiTenantCommand

# Configure standard logging
logger = logging.getLogger(__name__)


class IVRCommand(MultiTenantCommand):
    """Command for managing Interactive Voice Response (IVR) systems."""

    resource = "ivr"

    async def list_async(self, **kwargs: Any) -> dict[str, Any]:
        """List IVR systems asynchronously.

        Args:
            **kwargs: Query parameters

        Returns:
            List of IVR systems

        """
        return await super().list_async(**kwargs)

    async def get_async(self, resource_id: str, **kwargs: Any) -> dict[str, Any]:
        """Get an IVR system by ID asynchronously.

        Args:
            resource_id: IVR system ID
            **kwargs: Additional parameters

        Returns:
            IVR system data

        """
        return await super().get_async(resource_id, **kwargs)

    async def create_async(self, body: dict[str, Any], **kwargs: Any) -> dict[str, Any]:
        """Create an IVR system asynchronously.

        Args:
            body: IVR system data
            **kwargs: Additional parameters

        Returns:
            Created IVR system data

        """
        return await super().create_async(body, **kwargs)

    async def update_async(self, body: dict[str, Any]) -> None:
        """Update an IVR system asynchronously.

        Args:
            body: IVR system data

        """
        await super().update_async(body)

    async def delete_async(self, resource_id: str) -> None:
        """Delete an IVR system asynchronously.

        Args:
            resource_id: IVR system ID

        """
        await super().delete_async(resource_id)
