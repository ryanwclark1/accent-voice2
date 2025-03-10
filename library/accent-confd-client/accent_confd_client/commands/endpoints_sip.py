# Copyright 2025 Accent Communications

"""SIP endpoints command module for the Configuration Daemon API."""

import logging
from typing import Any

from accent_confd_client.crud import MultiTenantCommand
from accent_confd_client.relations import (
    LineEndpointSipRelation,
    TrunkEndpointSipRelation,
)

# Configure standard logging
logger = logging.getLogger(__name__)


class EndpointSipRelation:
    """Relations for SIP endpoints."""

    def __init__(self, builder: Any, sip_id: str) -> None:
        """Initialize SIP endpoint relations.

        Args:
            builder: Client instance
            sip_id: SIP endpoint ID

        """
        self.sip_id = sip_id
        self.line_endpoint_sip = LineEndpointSipRelation(builder)
        self.trunk_endpoint_sip = TrunkEndpointSipRelation(builder)

    def associate_line(self, line_id: str) -> None:
        """Associate a line with the SIP endpoint.

        Args:
            line_id: Line ID

        """
        self.line_endpoint_sip.associate(line_id, self.sip_id)

    async def associate_line_async(self, line_id: str) -> None:
        """Associate a line with the SIP endpoint asynchronously.

        Args:
            line_id: Line ID

        """
        await self.line_endpoint_sip.associate_async(line_id, self.sip_id)

    def dissociate_line(self, line_id: str) -> None:
        """Dissociate a line from the SIP endpoint.

        Args:
            line_id: Line ID

        """
        self.line_endpoint_sip.dissociate(line_id, self.sip_id)

    async def dissociate_line_async(self, line_id: str) -> None:
        """Dissociate a line from the SIP endpoint asynchronously.

        Args:
            line_id: Line ID

        """
        await self.line_endpoint_sip.dissociate_async(line_id, self.sip_id)


class EndpointsSipCommand(MultiTenantCommand):
    """Command for managing SIP endpoints."""

    resource = "endpoints/sip"
    relation_cmd = EndpointSipRelation

    async def list_async(self, **kwargs: Any) -> dict[str, Any]:
        """List SIP endpoints asynchronously.

        Args:
            **kwargs: Query parameters

        Returns:
            List of SIP endpoints

        """
        return await super().list_async(**kwargs)

    async def get_async(self, resource_id: str, **kwargs: Any) -> dict[str, Any]:
        """Get a SIP endpoint by ID asynchronously.

        Args:
            resource_id: SIP endpoint ID
            **kwargs: Additional parameters

        Returns:
            SIP endpoint data

        """
        return await super().get_async(resource_id, **kwargs)

    async def create_async(self, body: dict[str, Any], **kwargs: Any) -> dict[str, Any]:
        """Create a SIP endpoint asynchronously.

        Args:
            body: SIP endpoint data
            **kwargs: Additional parameters

        Returns:
            Created SIP endpoint data

        """
        return await super().create_async(body, **kwargs)

    async def update_async(self, body: dict[str, Any]) -> None:
        """Update a SIP endpoint asynchronously.

        Args:
            body: SIP endpoint data

        """
        await super().update_async(body)

    async def delete_async(self, resource_id: str) -> None:
        """Delete a SIP endpoint asynchronously.

        Args:
            resource_id: SIP endpoint ID

        """
        await super().delete_async(resource_id)
