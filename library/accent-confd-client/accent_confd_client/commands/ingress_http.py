# Copyright 2025 Accent Communications

"""HTTP ingress command module for the Configuration Daemon API."""

import logging
from typing import Any

from accent_confd_client.crud import MultiTenantCommand

# Configure standard logging
logger = logging.getLogger(__name__)


class IngressHttpCommand(MultiTenantCommand):
    """Command for managing HTTP ingress points."""

    resource = "ingresses/http"

    async def list_async(self, **kwargs: Any) -> dict[str, Any]:
        """List HTTP ingress points asynchronously.

        Args:
            **kwargs: Query parameters

        Returns:
            List of HTTP ingress points

        """
        return await super().list_async(**kwargs)

    async def get_async(self, resource_id: str, **kwargs: Any) -> dict[str, Any]:
        """Get an HTTP ingress point by ID asynchronously.

        Args:
            resource_id: HTTP ingress point ID
            **kwargs: Additional parameters

        Returns:
            HTTP ingress point data

        """
        return await super().get_async(resource_id, **kwargs)

    async def create_async(self, body: dict[str, Any], **kwargs: Any) -> dict[str, Any]:
        """Create an HTTP ingress point asynchronously.

        Args:
            body: HTTP ingress point data
            **kwargs: Additional parameters

        Returns:
            Created HTTP ingress point data

        """
        return await super().create_async(body, **kwargs)

    async def update_async(self, body: dict[str, Any]) -> None:
        """Update an HTTP ingress point asynchronously.

        Args:
            body: HTTP ingress point data

        """
        await super().update_async(body)

    async def delete_async(self, resource_id: str) -> None:
        """Delete an HTTP ingress point asynchronously.

        Args:
            resource_id: HTTP ingress point ID

        """
        await super().delete_async(resource_id)
