# Copyright 2025 Accent Communications

"""Skills command module for the Configuration Daemon API."""

import logging
from typing import Any

from accent_confd_client.crud import MultiTenantCommand

# Configure standard logging
logger = logging.getLogger(__name__)


class SkillsCommand(MultiTenantCommand):
    """Command for managing agent skills."""

    resource = "agents/skills"

    async def list_async(self, **kwargs: Any) -> dict[str, Any]:
        """List agent skills asynchronously.

        Args:
            **kwargs: Query parameters

        Returns:
            List of agent skills

        """
        return await super().list_async(**kwargs)

    async def get_async(self, resource_id: str, **kwargs: Any) -> dict[str, Any]:
        """Get an agent skill by ID asynchronously.

        Args:
            resource_id: Skill ID
            **kwargs: Additional parameters

        Returns:
            Skill data

        """
        return await super().get_async(resource_id, **kwargs)

    async def create_async(self, body: dict[str, Any], **kwargs: Any) -> dict[str, Any]:
        """Create an agent skill asynchronously.

        Args:
            body: Skill data
            **kwargs: Additional parameters

        Returns:
            Created skill data

        """
        return await super().create_async(body, **kwargs)

    async def update_async(self, body: dict[str, Any]) -> None:
        """Update an agent skill asynchronously.

        Args:
            body: Skill data

        """
        await super().update_async(body)

    async def delete_async(self, resource_id: str) -> None:
        """Delete an agent skill asynchronously.

        Args:
            resource_id: Skill ID

        """
        await super().delete_async(resource_id)
