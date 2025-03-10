# Copyright 2025 Accent Communications

"""Skill rules command module for the Configuration Daemon API."""

import logging
from typing import Any

from accent_confd_client.crud import MultiTenantCommand

# Configure standard logging
logger = logging.getLogger(__name__)


class SkillRulesCommand(MultiTenantCommand):
    """Command for managing skill rules."""

    resource = "queues/skillrules"

    async def list_async(self, **kwargs: Any) -> dict[str, Any]:
        """List skill rules asynchronously.

        Args:
            **kwargs: Query parameters

        Returns:
            List of skill rules

        """
        return await super().list_async(**kwargs)

    async def get_async(self, resource_id: str, **kwargs: Any) -> dict[str, Any]:
        """Get a skill rule by ID asynchronously.

        Args:
            resource_id: Skill rule ID
            **kwargs: Additional parameters

        Returns:
            Skill rule data

        """
        return await super().get_async(resource_id, **kwargs)

    async def create_async(self, body: dict[str, Any], **kwargs: Any) -> dict[str, Any]:
        """Create a skill rule asynchronously.

        Args:
            body: Skill rule data
            **kwargs: Additional parameters

        Returns:
            Created skill rule data

        """
        return await super().create_async(body, **kwargs)

    async def update_async(self, body: dict[str, Any]) -> None:
        """Update a skill rule asynchronously.

        Args:
            body: Skill rule data

        """
        await super().update_async(body)

    async def delete_async(self, resource_id: str) -> None:
        """Delete a skill rule asynchronously.

        Args:
            resource_id: Skill rule ID

        """
        await super().delete_async(resource_id)
