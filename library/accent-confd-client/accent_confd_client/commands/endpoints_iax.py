# Copyright 2025 Accent Communications

"""IAX endpoints command module for the Configuration Daemon API."""

import logging
from typing import Any

from accent_confd_client.crud import MultiTenantCommand

# Configure standard logging
logger = logging.getLogger(__name__)


class EndpointsIAXCommand(MultiTenantCommand):
    """Command for managing IAX endpoints."""

    resource = "endpoints/iax"

    async def list_async(self, **kwargs: Any) -> dict[str, Any]:
        """List IAX endpoints asynchronously.

        Args:
            **kwargs: Query parameters

        Returns:
            List of IAX endpoints

        """
        return await super().list_async(**kwargs)

    async def get_async(self, resource_id: str, **kwargs: Any) -> dict[str, Any]:
        """Get an IAX endpoint by ID asynchronously.

        Args:
            resource_id: IAX endpoint ID
            **kwargs: Additional parameters

        Returns:
            IAX endpoint data

        """
        return await super().get_async(resource_id, **kwargs)

    async def create_async(self, body: dict[str, Any], **kwargs: Any) -> dict[str, Any]:
        """Create an IAX endpoint asynchronously.

        Args:
            body: IAX endpoint data
            **kwargs: Additional parameters

        Returns:
            Created IAX endpoint data

        """
        return await super().create_async(body, **kwargs)

    async def update_async(self, body: dict[str, Any]) -> None:
        """Update an IAX endpoint asynchronously.

        Args:
            body: IAX endpoint data

        """
        await super().update_async(body)

    async def delete_async(self, resource_id: str) -> None:
        """Delete an IAX endpoint asynchronously.

        Args:
            resource_id: IAX endpoint ID

        """
        await super().delete_async(resource_id)
