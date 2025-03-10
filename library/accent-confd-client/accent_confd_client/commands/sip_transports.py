# Copyright 2025 Accent Communications

"""SIP transports command module for the Configuration Daemon API."""

import logging
from typing import Any

from accent_confd_client.crud import CRUDCommand

# Configure standard logging
logger = logging.getLogger(__name__)


class SIPTransportsCommand(CRUDCommand):
    """Command for managing SIP transports."""

    resource = "sip/transports"

    async def list_async(self, **kwargs: Any) -> dict[str, Any]:
        """List SIP transports asynchronously.

        Args:
            **kwargs: Query parameters

        Returns:
            List of SIP transports

        """
        return await super().list_async(**kwargs)

    async def get_async(self, resource_id: str) -> dict[str, Any]:
        """Get a SIP transport by ID asynchronously.

        Args:
            resource_id: SIP transport ID

        Returns:
            SIP transport data

        """
        return await super().get_async(resource_id)

    async def create_async(self, body: dict[str, Any]) -> dict[str, Any]:
        """Create a SIP transport asynchronously.

        Args:
            body: SIP transport data

        Returns:
            Created SIP transport data

        """
        return await super().create_async(body)

    async def update_async(self, body: dict[str, Any]) -> None:
        """Update a SIP transport asynchronously.

        Args:
            body: SIP transport data

        """
        await super().update_async(body)

    async def delete_async(self, resource_id: str) -> None:
        """Delete a SIP transport asynchronously.

        Args:
            resource_id: SIP transport ID

        """
        await super().delete_async(resource_id)
