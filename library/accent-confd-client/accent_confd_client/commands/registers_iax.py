# Copyright 2025 Accent Communications

"""IAX registers command module for the Configuration Daemon API."""

import logging
from typing import Any

from accent_confd_client.crud import CRUDCommand

# Configure standard logging
logger = logging.getLogger(__name__)


class RegistersIAXCommand(CRUDCommand):
    """Command for managing IAX registrations."""

    resource = "registers/iax"

    async def list_async(self, **kwargs: Any) -> dict[str, Any]:
        """List IAX registrations asynchronously.

        Args:
            **kwargs: Query parameters

        Returns:
            List of IAX registrations

        """
        return await super().list_async(**kwargs)

    async def get_async(self, resource_id: str) -> dict[str, Any]:
        """Get an IAX registration by ID asynchronously.

        Args:
            resource_id: IAX registration ID

        Returns:
            IAX registration data

        """
        return await super().get_async(resource_id)

    async def create_async(self, body: dict[str, Any]) -> dict[str, Any]:
        """Create an IAX registration asynchronously.

        Args:
            body: IAX registration data

        Returns:
            Created IAX registration data

        """
        return await super().create_async(body)

    async def update_async(self, body: dict[str, Any]) -> None:
        """Update an IAX registration asynchronously.

        Args:
            body: IAX registration data

        """
        await super().update_async(body)

    async def delete_async(self, resource_id: str) -> None:
        """Delete an IAX registration asynchronously.

        Args:
            resource_id: IAX registration ID

        """
        await super().delete_async(resource_id)
