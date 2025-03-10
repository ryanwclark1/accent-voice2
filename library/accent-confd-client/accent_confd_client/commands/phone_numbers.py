# Copyright 2025 Accent Communications

"""Phone numbers command module for the Configuration Daemon API."""

import logging
from typing import Any

from accent_confd_client.crud import MultiTenantCommand

# Configure standard logging
logger = logging.getLogger(__name__)


class PhoneNumbersCommand(MultiTenantCommand):
    """Command for managing phone numbers."""

    resource = "phone-numbers"

    async def list_async(self, **kwargs: Any) -> dict[str, Any]:
        """List phone numbers asynchronously.

        Args:
            **kwargs: Query parameters

        Returns:
            List of phone numbers

        """
        return await super().list_async(**kwargs)

    async def get_async(self, resource_id: str, **kwargs: Any) -> dict[str, Any]:
        """Get a phone number by ID asynchronously.

        Args:
            resource_id: Phone number ID
            **kwargs: Additional parameters

        Returns:
            Phone number data

        """
        return await super().get_async(resource_id, **kwargs)

    async def create_async(self, body: dict[str, Any], **kwargs: Any) -> dict[str, Any]:
        """Create a phone number asynchronously.

        Args:
            body: Phone number data
            **kwargs: Additional parameters

        Returns:
            Created phone number data

        """
        return await super().create_async(body, **kwargs)

    async def update_async(self, body: dict[str, Any]) -> None:
        """Update a phone number asynchronously.

        Args:
            body: Phone number data

        """
        await super().update_async(body)

    async def delete_async(self, resource_id: str) -> None:
        """Delete a phone number asynchronously.

        Args:
            resource_id: Phone number ID

        """
        await super().delete_async(resource_id)
