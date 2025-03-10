# Copyright 2025 Accent Communications

"""Custom endpoints command module for the Configuration Daemon API."""

import logging
from typing import Any

from accent_confd_client.crud import MultiTenantCommand
from accent_confd_client.relations import (
    LineEndpointCustomRelation,
    TrunkEndpointCustomRelation,
)

# Configure standard logging
logger = logging.getLogger(__name__)


class EndpointCustomRelation:
    """Relations for custom endpoints."""

    def __init__(self, builder: Any, custom_id: str) -> None:
        """Initialize custom endpoint relations.

        Args:
            builder: Client instance
            custom_id: Custom endpoint ID

        """
        self.custom_id = custom_id
        self.line_endpoint_custom = LineEndpointCustomRelation(builder)
        self.trunk_endpoint_custom = TrunkEndpointCustomRelation(builder)

    def associate_line(self, line_id: str) -> None:
        """Associate a line with the custom endpoint.

        Args:
            line_id: Line ID

        """
        self.line_endpoint_custom.associate(line_id, self.custom_id)

    async def associate_line_async(self, line_id: str) -> None:
        """Associate a line with the custom endpoint asynchronously.

        Args:
            line_id: Line ID

        """
        await self.line_endpoint_custom.associate_async(line_id, self.custom_id)

    def dissociate_line(self, line_id: str) -> None:
        """Dissociate a line from the custom endpoint.

        Args:
            line_id: Line ID

        """
        self.line_endpoint_custom.dissociate(line_id, self.custom_id)

    async def dissociate_line_async(self, line_id: str) -> None:
        """Dissociate a line from the custom endpoint asynchronously.

        Args:
            line_id: Line ID

        """
        await self.line_endpoint_custom.dissociate_async(line_id, self.custom_id)


class EndpointsCustomCommand(MultiTenantCommand):
    """Command for managing custom endpoints."""

    resource = "endpoints/custom"
    relation_cmd = EndpointCustomRelation

    async def list_async(self, **kwargs: Any) -> dict[str, Any]:
        """List custom endpoints asynchronously.

        Args:
            **kwargs: Query parameters

        Returns:
            List of custom endpoints

        """
        return await super().list_async(**kwargs)

    async def get_async(self, resource_id: str, **kwargs: Any) -> dict[str, Any]:
        """Get a custom endpoint by ID asynchronously.

        Args:
            resource_id: Custom endpoint ID
            **kwargs: Additional parameters

        Returns:
            Custom endpoint data

        """
        return await super().get_async(resource_id, **kwargs)

    async def create_async(self, body: dict[str, Any], **kwargs: Any) -> dict[str, Any]:
        """Create a custom endpoint asynchronously.

        Args:
            body: Custom endpoint data
            **kwargs: Additional parameters

        Returns:
            Created custom endpoint data

        """
        return await super().create_async(body, **kwargs)

    async def update_async(self, body: dict[str, Any]) -> None:
        """Update a custom endpoint asynchronously.

        Args:
            body: Custom endpoint data

        """
        await super().update_async(body)

    async def delete_async(self, resource_id: str) -> None:
        """Delete a custom endpoint asynchronously.

        Args:
            resource_id: Custom endpoint ID

        """
        await super().delete_async(resource_id)
