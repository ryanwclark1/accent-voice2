# Copyright 2025 Accent Communications

"""Switchboards command module for the Configuration Daemon API."""

import logging
from typing import Any

from accent_confd_client.crud import MultiTenantCommand
from accent_confd_client.relations import (
    SwitchboardFallbackRelation,
    SwitchboardMemberUserRelation,
)

# Configure standard logging
logger = logging.getLogger(__name__)


class SwitchboardRelation:
    """Relations for switchboards."""

    def __init__(self, builder: Any, switchboard_id: str) -> None:
        """Initialize switchboard relations.

        Args:
            builder: Client instance
            switchboard_id: Switchboard ID

        """
        self.switchboard_id = switchboard_id
        self.switchboard_user_members = SwitchboardMemberUserRelation(builder)
        self.switchboard_fallback = SwitchboardFallbackRelation(builder)

    def update_user_members(self, users: list[dict[str, Any]]) -> Any:
        """Update user members for the switchboard.

        Args:
            users: List of users

        Returns:
            API response

        """
        return self.switchboard_user_members.associate(self.switchboard_id, users)

    async def update_user_members_async(self, users: list[dict[str, Any]]) -> Any:
        """Update user members for the switchboard asynchronously.

        Args:
            users: List of users

        Returns:
            API response

        """
        return await self.switchboard_user_members.associate_async(
            self.switchboard_id, users
        )

    def update_fallbacks(self, fallbacks: dict[str, Any]) -> None:
        """Update fallbacks for the switchboard.

        Args:
            fallbacks: Fallbacks data

        """
        self.switchboard_fallback.update_fallbacks(self.switchboard_id, fallbacks)

    async def update_fallbacks_async(self, fallbacks: dict[str, Any]) -> None:
        """Update fallbacks for the switchboard asynchronously.

        Args:
            fallbacks: Fallbacks data

        """
        await self.switchboard_fallback.update_fallbacks_async(
            self.switchboard_id, fallbacks
        )

    def list_fallbacks(self) -> dict[str, Any]:
        """List fallbacks for the switchboard.

        Returns:
            Fallbacks data

        """
        return self.switchboard_fallback.list_fallbacks(self.switchboard_id)

    async def list_fallbacks_async(self) -> dict[str, Any]:
        """List fallbacks for the switchboard asynchronously.

        Returns:
            Fallbacks data

        """
        return await self.switchboard_fallback.list_fallbacks_async(self.switchboard_id)


class SwitchboardsCommand(MultiTenantCommand):
    """Command for managing switchboards."""

    resource = "switchboards"
    relation_cmd = SwitchboardRelation
