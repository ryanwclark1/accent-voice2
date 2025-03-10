# Copyright 2025 Accent Communications

"""Contexts command module for the Configuration Daemon API."""

import logging
from typing import Any

from accent_confd_client.crud import MultiTenantCommand
from accent_confd_client.relations import ContextContextRelation, ContextRangeRelation

# Configure standard logging
logger = logging.getLogger(__name__)


class ContextRelation:
    """Relations for contexts."""

    def __init__(self, builder: Any, context_id: str) -> None:
        """Initialize context relations.

        Args:
            builder: Client instance
            context_id: Context ID

        """
        self.context_id = context_id
        self.context_context = ContextContextRelation(builder)
        self.context_range = ContextRangeRelation(builder)

    def update_contexts(self, contexts: list[dict[str, Any]]) -> Any:
        """Update related contexts.

        Args:
            contexts: List of contexts

        Returns:
            API response

        """
        return self.context_context.associate(self.context_id, contexts)

    async def update_contexts_async(self, contexts: list[dict[str, Any]]) -> Any:
        """Update related contexts asynchronously.

        Args:
            contexts: List of contexts

        Returns:
            API response

        """
        return await self.context_context.associate_async(self.context_id, contexts)

    def list_ranges(self, range_type: str, **kwargs: Any) -> dict[str, Any]:
        """List ranges for the context.

        Args:
            range_type: Range type
            **kwargs: Additional parameters

        Returns:
            List of ranges

        """
        return self.context_range.list_ranges(self.context_id, range_type, **kwargs)

    async def list_ranges_async(self, range_type: str, **kwargs: Any) -> dict[str, Any]:
        """List ranges for the context asynchronously.

        Args:
            range_type: Range type
            **kwargs: Additional parameters

        Returns:
            List of ranges

        """
        return await self.context_range.list_ranges_async(
            self.context_id, range_type, **kwargs
        )


class ContextsCommand(MultiTenantCommand):
    """Command for managing contexts."""

    resource = "contexts"
    relation_cmd = ContextRelation
