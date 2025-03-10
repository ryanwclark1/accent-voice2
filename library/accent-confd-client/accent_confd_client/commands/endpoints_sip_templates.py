# Copyright 2025 Accent Communications

"""SIP endpoint templates command module for the Configuration Daemon API."""

import logging
from typing import Any

from accent_confd_client.crud import MultiTenantCommand

# Configure standard logging
logger = logging.getLogger(__name__)


class EndpointsSipTemplatesCommand(MultiTenantCommand):
    """Command for managing SIP endpoint templates."""

    resource = "endpoints/sip/templates"

    async def list_async(self, **kwargs: Any) -> dict[str, Any]:
        """List SIP endpoint templates asynchronously.

        Args:
            **kwargs: Query parameters

        Returns:
            List of SIP endpoint templates

        """
        return await super().list_async(**kwargs)

    async def get_async(self, resource_id: str, **kwargs: Any) -> dict[str, Any]:
        """Get a SIP endpoint template by ID asynchronously.

        Args:
            resource_id: SIP endpoint template ID
            **kwargs: Additional parameters

        Returns:
            SIP endpoint template data

        """
        return await super().get_async(resource_id, **kwargs)

    async def create_async(self, body: dict[str, Any], **kwargs: Any) -> dict[str, Any]:
        """Create a SIP endpoint template asynchronously.

        Args:
            body: SIP endpoint template data
            **kwargs: Additional parameters

        Returns:
            Created SIP endpoint template data

        """
        return await super().create_async(body, **kwargs)

    async def update_async(self, body: dict[str, Any]) -> None:
        """Update a SIP endpoint template asynchronously.

        Args:
            body: SIP endpoint template data

        """
        await super().update_async(body)

    async def delete_async(self, resource_id: str) -> None:
        """Delete a SIP endpoint template asynchronously.

        Args:
            resource_id: SIP endpoint template ID

        """
        await super().delete_async(resource_id)
