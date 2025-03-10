# Copyright 2025 Accent Communications

"""Call filters command module for the Configuration Daemon API."""

import logging
from typing import Any

from accent_confd_client.crud import MultiTenantCommand
from accent_confd_client.relations import (
    CallFilterFallbackRelation,
    CallFilterRecipientUserRelation,
    CallFilterSurrogateUserRelation,
)

# Configure standard logging
logger = logging.getLogger(__name__)


class CallFilterRelation:
    """Relations for call filters."""

    def __init__(self, builder: Any, call_filter_id: str) -> None:
        """Initialize call filter relations.

        Args:
            builder: Client instance
            call_filter_id: Call filter ID

        """
        self.call_filter_id = call_filter_id
        self.call_filter_user_recipients = CallFilterRecipientUserRelation(builder)
        self.call_filter_user_surrogates = CallFilterSurrogateUserRelation(builder)
        self.call_filter_fallback = CallFilterFallbackRelation(builder)

    def update_user_surrogates(self, users: list[dict[str, Any]]) -> Any:
        """Update user surrogates for the call filter.

        Args:
            users: List of users

        Returns:
            API response

        """
        return self.call_filter_user_surrogates.associate(self.call_filter_id, users)

    async def update_user_surrogates_async(self, users: list[dict[str, Any]]) -> Any:
        """Update user surrogates for the call filter asynchronously.

        Args:
            users: List of users

        Returns:
            API response

        """
        return await self.call_filter_user_surrogates.associate_async(
            self.call_filter_id, users
        )

    def update_user_recipients(self, users: list[dict[str, Any]]) -> Any:
        """Update user recipients for the call filter.

        Args:
            users: List of users

        Returns:
            API response

        """
        return self.call_filter_user_recipients.associate(self.call_filter_id, users)

    async def update_user_recipients_async(self, users: list[dict[str, Any]]) -> Any:
        """Update user recipients for the call filter asynchronously.

        Args:
            users: List of users

        Returns:
            API response

        """
        return await self.call_filter_user_recipients.associate_async(
            self.call_filter_id, users
        )

    def update_fallbacks(self, fallbacks: dict[str, Any]) -> None:
        """Update fallbacks for the call filter.

        Args:
            fallbacks: Fallbacks data

        """
        self.call_filter_fallback.update_fallbacks(self.call_filter_id, fallbacks)

    async def update_fallbacks_async(self, fallbacks: dict[str, Any]) -> None:
        """Update fallbacks for the call filter asynchronously.

        Args:
            fallbacks: Fallbacks data

        """
        await self.call_filter_fallback.update_fallbacks_async(
            self.call_filter_id, fallbacks
        )


class CallFiltersCommand(MultiTenantCommand):
    """Command for managing call filters."""

    resource = "callfilters"
    relation_cmd = CallFilterRelation
