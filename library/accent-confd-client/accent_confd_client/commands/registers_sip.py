# Copyright 2025 Accent Communications

"""SIP registers command module for the Configuration Daemon API."""

import logging
from typing import Any

from accent_confd_client.crud import CRUDCommand

# Configure standard logging
logger = logging.getLogger(__name__)


class RegistersSipCommand(CRUDCommand):
    """Command for managing SIP registrations."""

    resource = "registers/sip"

    async def list_async(self, **kwargs: Any) -> dict[str, Any]:
        """List SIP registrations asynchronously.

        Args:
            **kwargs: Query parameters

        Returns:
            List of SIP registrations

        """
        return await super().list_async(**kwargs)

    async def get_async(self, resource_id: str) -> dict[str, Any]:
        """Get a SIP registration by ID asynchronously.

        Args:
            resource_id: SIP registration ID

        Returns:
            SIP registration data

        """
        return await super().get_async(resource_id)

    async def create_async(self, body: dict[str, Any]) -> dict[str, Any]:
        """Create a SIP registration asynchronously.

        Args:
            body: SIP registration data

        Returns:
            Created SIP registration data

        """
        return await super().create_async(body)

    async def update_async(self, body: dict[str, Any]) -> None:
        """Update a SIP registration asynchronously.

        Args:
            body: SIP registration data

        """
        await super().update_async(body)

    async def delete_async(self, resource_id: str) -> None:
        """Delete a SIP registration asynchronously.

        Args:
            resource_id: SIP registration ID

        """
        await super().delete_async(resource_id)
