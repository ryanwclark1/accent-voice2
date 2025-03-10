# Copyright 2025 Accent Communications

"""Registrars command module for the Configuration Daemon API."""

import logging
from typing import Any

from accent_confd_client.crud import CRUDCommand

# Configure standard logging
logger = logging.getLogger(__name__)


class RegistrarsCommand(CRUDCommand):
    """Command for managing registrars."""

    resource = "registrars"

    async def list_async(self, **kwargs: Any) -> dict[str, Any]:
        """List registrars asynchronously.

        Args:
            **kwargs: Query parameters

        Returns:
            List of registrars

        """
        return await super().list_async(**kwargs)

    async def get_async(self, resource_id: str) -> dict[str, Any]:
        """Get a registrar by ID asynchronously.

        Args:
            resource_id: Registrar ID

        Returns:
            Registrar data

        """
        return await super().get_async(resource_id)

    async def create_async(self, body: dict[str, Any]) -> dict[str, Any]:
        """Create a registrar asynchronously.

        Args:
            body: Registrar data

        Returns:
            Created registrar data

        """
        return await super().create_async(body)

    async def update_async(self, body: dict[str, Any]) -> None:
        """Update a registrar asynchronously.

        Args:
            body: Registrar data

        """
        await super().update_async(body)

    async def delete_async(self, resource_id: str) -> None:
        """Delete a registrar asynchronously.

        Args:
            resource_id: Registrar ID

        """
        await super().delete_async(resource_id)
