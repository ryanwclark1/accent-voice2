# Copyright 2025 Accent Communications

"""SCCP endpoints command module for the Configuration Daemon API."""

import logging
from typing import Any

from accent_confd_client.crud import MultiTenantCommand
from accent_confd_client.relations import LineEndpointSccpRelation

# Configure standard logging
logger = logging.getLogger(__name__)


class EndpointSccpRelation:
    """Relations for SCCP endpoints."""

    def __init__(self, builder: Any, sccp_id: str) -> None:
        """Initialize SCCP endpoint relations.

        Args:
            builder: Client instance
            sccp_id: SCCP endpoint ID

        """
        self.sccp_id = sccp_id
        self.line_endpoint_sccp = LineEndpointSccpRelation(builder)

    def associate_line(self, line_id: str) -> None:
        """Associate a line with the SCCP endpoint.

        Args:
            line_id: Line ID

        """
        self.line_endpoint_sccp.associate(line_id, self.sccp_id)

    async def associate_line_async(self, line_id: str) -> None:
        """Associate a line with the SCCP endpoint asynchronously.

        Args:
            line_id: Line ID

        """
        await self.line_endpoint_sccp.associate_async(line_id, self.sccp_id)

    def dissociate_line(self, line_id: str) -> None:
        """Dissociate a line from the SCCP endpoint.

        Args:
            line_id: Line ID

        """
        self.line_endpoint_sccp.dissociate(line_id, self.sccp_id)

    async def dissociate_line_async(self, line_id: str) -> None:
        """Dissociate a line from the SCCP endpoint asynchronously.

        Args:
            line_id: Line ID

        """
        await self.line_endpoint_sccp.dissociate_async(line_id, self.sccp_id)


class EndpointsSccpCommand(MultiTenantCommand):
    """Command for managing SCCP endpoints."""

    resource = "endpoints/sccp"
    relation_cmd = EndpointSccpRelation

    async def list_async(self, **kwargs: Any) -> dict[str, Any]:
        """List SCCP endpoints asynchronously.

        Args:
            **kwargs: Query parameters

        Returns:
            List of SCCP endpoints

        """
        return await super().list_async(**kwargs)

    async def get_async(self, resource_id: str, **kwargs: Any) -> dict[str, Any]:
        """Get a SCCP endpoint by ID asynchronously.

        Args:
            resource_id: SCCP endpoint ID
            **kwargs: Additional parameters

        Returns:
            SCCP endpoint data

        """
        return await super().get_async(resource_id, **kwargs)

    async def create_async(self, body: dict[str, Any], **kwargs: Any) -> dict[str, Any]:
        """Create a SCCP endpoint asynchronously.

        Args:
            body: SCCP endpoint data
            **kwargs: Additional parameters

        Returns:
            Created SCCP endpoint data

        """
        return await super().create_async(body, **kwargs)

    async def update_async(self, body: dict[str, Any]) -> None:
        """Update a SCCP endpoint asynchronously.

        Args:
            body: SCCP endpoint data

        """
        await super().update_async(body)

    async def delete_async(self, resource_id: str) -> None:
        """Delete a SCCP endpoint asynchronously.

        Args:
            resource_id: SCCP endpoint ID

        """
        await super().delete_async(resource_id)
