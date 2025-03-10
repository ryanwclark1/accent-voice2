# Copyright 2025 Accent Communications

"""Pagings command module for the Configuration Daemon API."""

import logging
from typing import Any

from accent_confd_client.crud import MultiTenantCommand
from accent_confd_client.relations import (
    PagingCallerUserRelation,
    PagingMemberUserRelation,
)

# Configure standard logging
logger = logging.getLogger(__name__)


class PagingRelation:
    """Relations for pagings."""

    def __init__(self, builder: Any, paging_id: str) -> None:
        """Initialize paging relations.

        Args:
            builder: Client instance
            paging_id: Paging ID

        """
        self.paging_id = paging_id
        self.paging_user_callers = PagingCallerUserRelation(builder)
        self.paging_user_members = PagingMemberUserRelation(builder)

    def update_user_members(self, users: list[dict[str, Any]]) -> Any:
        """Update user members for the paging.

        Args:
            users: List of users

        Returns:
            API response

        """
        return self.paging_user_members.associate(self.paging_id, users)

    async def update_user_members_async(self, users: list[dict[str, Any]]) -> Any:
        """Update user members for the paging asynchronously.

        Args:
            users: List of users

        Returns:
            API response

        """
        return await self.paging_user_members.associate_async(self.paging_id, users)

    def update_user_callers(self, users: list[dict[str, Any]]) -> Any:
        """Update user callers for the paging.

        Args:
            users: List of users

        Returns:
            API response

        """
        return self.paging_user_callers.associate(self.paging_id, users)

    async def update_user_callers_async(self, users: list[dict[str, Any]]) -> Any:
        """Update user callers for the paging asynchronously.

        Args:
            users: List of users

        Returns:
            API response

        """
        return await self.paging_user_callers.associate_async(self.paging_id, users)


class PagingsCommand(MultiTenantCommand):
    """Command for managing pagings."""

    resource = "pagings"
    relation_cmd = PagingRelation
