# Copyright 2025 Accent Communications

"""Tenants command module for the Configuration Daemon API."""

import logging
from typing import Any

from accent_confd_client.crud import MultiTenantCommand

# Configure standard logging
logger = logging.getLogger(__name__)


class TenantsCommand(MultiTenantCommand):
    """Command for managing tenants."""

    resource = "tenants"

    async def list_async(self, **kwargs: Any) -> dict[str, Any]:
        """List tenants asynchronously.

        Args:
            **kwargs: Query parameters

        Returns:
            List of tenants

        """
        return await super().list_async(**kwargs)

    async def get_async(self, resource_id: str, **kwargs: Any) -> dict[str, Any]:
        """Get a tenant by ID asynchronously.

        Args:
            resource_id: Tenant ID
            **kwargs: Additional parameters

        Returns:
            Tenant data

        """
        return await super().get_async(resource_id, **kwargs)

    async def create_async(self, body: dict[str, Any], **kwargs: Any) -> dict[str, Any]:
        """Create a tenant asynchronously.

        Args:
            body: Tenant data
            **kwargs: Additional parameters

        Returns:
            Created tenant data

        """
        return await super().create_async(body, **kwargs)

    async def update_async(self, body: dict[str, Any]) -> None:
        """Update a tenant asynchronously.

        Args:
            body: Tenant data

        """
        await super().update_async(body)

    async def delete_async(self, resource_id: str) -> None:
        """Delete a tenant asynchronously.

        Args:
            resource_id: Tenant ID

        """
        await super().delete_async(resource_id)
