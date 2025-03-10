# Copyright 2025 Accent Communications

"""Call pickups command module for the Configuration Daemon API."""

import logging
from typing import Any

from accent_confd_client.crud import MultiTenantCommand
from accent_confd_client.relations import (
    CallPickupInterceptorGroupRelation,
    CallPickupInterceptorUserRelation,
    CallPickupTargetGroupRelation,
    CallPickupTargetUserRelation,
)

# Configure standard logging
logger = logging.getLogger(__name__)


class CallPickupRelation:
    """Relations for call pickups."""

    def __init__(self, builder: Any, call_pickup_id: str) -> None:
        """Initialize call pickup relations.

        Args:
            builder: Client instance
            call_pickup_id: Call pickup ID

        """
        self.call_pickup_id = call_pickup_id
        self.call_pickup_group_interceptors = CallPickupInterceptorGroupRelation(
            builder
        )
        self.call_pickup_group_targets = CallPickupTargetGroupRelation(builder)
        self.call_pickup_user_interceptors = CallPickupInterceptorUserRelation(builder)
        self.call_pickup_user_targets = CallPickupTargetUserRelation(builder)

    def update_group_targets(self, groups: list[dict[str, Any]]) -> Any:
        """Update group targets for the call pickup.

        Args:
            groups: List of groups

        Returns:
            API response

        """
        return self.call_pickup_group_targets.associate(self.call_pickup_id, groups)

    async def update_group_targets_async(self, groups: list[dict[str, Any]]) -> Any:
        """Update group targets for the call pickup asynchronously.

        Args:
            groups: List of groups

        Returns:
            API response

        """
        return await self.call_pickup_group_targets.associate_async(
            self.call_pickup_id, groups
        )

    def update_group_interceptors(self, groups: list[dict[str, Any]]) -> Any:
        """Update group interceptors for the call pickup.

        Args:
            groups: List of groups

        Returns:
            API response

        """
        return self.call_pickup_group_interceptors.associate(
            self.call_pickup_id, groups
        )

    async def update_group_interceptors_async(
        self, groups: list[dict[str, Any]]
    ) -> Any:
        """Update group interceptors for the call pickup asynchronously.

        Args:
            groups: List of groups

        Returns:
            API response

        """
        return await self.call_pickup_group_interceptors.associate_async(
            self.call_pickup_id, groups
        )

    def update_user_targets(self, users: list[dict[str, Any]]) -> Any:
        """Update user targets for the call pickup.

        Args:
            users: List of users

        Returns:
            API response

        """
        return self.call_pickup_user_targets.associate(self.call_pickup_id, users)

    async def update_user_targets_async(self, users: list[dict[str, Any]]) -> Any:
        """Update user targets for the call pickup asynchronously.

        Args:
            users: List of users

        Returns:
            API response

        """
        return await self.call_pickup_user_targets.associate_async(
            self.call_pickup_id, users
        )

    def update_user_interceptors(self, users: list[dict[str, Any]]) -> Any:
        """Update user interceptors for the call pickup.

        Args:
            users: List of users

        Returns:
            API response

        """
        return self.call_pickup_user_interceptors.associate(self.call_pickup_id, users)

    async def update_user_interceptors_async(self, users: list[dict[str, Any]]) -> Any:
        """Update user interceptors for the call pickup asynchronously.

        Args:
            users: List of users

        Returns:
            API response

        """
        return await self.call_pickup_user_interceptors.associate_async(
            self.call_pickup_id, users
        )


class CallPickupsCommand(MultiTenantCommand):
    """Command for managing call pickups."""

    resource = "callpickups"
    relation_cmd = CallPickupRelation
