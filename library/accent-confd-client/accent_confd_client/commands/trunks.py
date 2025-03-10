# Copyright 2025 Accent Communications

"""Trunks command module for the Configuration Daemon API."""

import logging
from typing import Any

from accent_confd_client.crud import MultiTenantCommand
from accent_confd_client.relations import (
    TrunkEndpointCustomRelation,
    TrunkEndpointIAXRelation,
    TrunkEndpointSipRelation,
    TrunkRegisterIAXRelation,
    TrunkRegisterSipRelation,
)
from accent_confd_client.util import extract_id

# Configure standard logging
logger = logging.getLogger(__name__)


class TrunkRelation:
    """Relations for trunks."""

    def __init__(self, builder: Any, trunk_id: str) -> None:
        """Initialize trunk relations.

        Args:
            builder: Client instance
            trunk_id: Trunk ID

        """
        self.trunk_id = trunk_id
        self.trunk_endpoint_sip = TrunkEndpointSipRelation(builder)
        self.trunk_endpoint_iax = TrunkEndpointIAXRelation(builder)
        self.trunk_endpoint_custom = TrunkEndpointCustomRelation(builder)
        self.trunk_register_iax = TrunkRegisterIAXRelation(builder)
        self.trunk_register_sip = TrunkRegisterSipRelation(builder)

    @extract_id
    def add_endpoint_sip(self, endpoint_sip_id: str) -> Any:
        """Add a SIP endpoint to the trunk.

        Args:
            endpoint_sip_id: SIP endpoint ID

        Returns:
            API response

        """
        return self.trunk_endpoint_sip.associate(self.trunk_id, endpoint_sip_id)

    @extract_id
    async def add_endpoint_sip_async(self, endpoint_sip_id: str) -> Any:
        """Add a SIP endpoint to the trunk asynchronously.

        Args:
            endpoint_sip_id: SIP endpoint ID

        Returns:
            API response

        """
        return await self.trunk_endpoint_sip.associate_async(
            self.trunk_id, endpoint_sip_id
        )

    @extract_id
    def remove_endpoint_sip(self, endpoint_sip_id: str) -> Any:
        """Remove a SIP endpoint from the trunk.

        Args:
            endpoint_sip_id: SIP endpoint ID

        Returns:
            API response

        """
        return self.trunk_endpoint_sip.dissociate(self.trunk_id, endpoint_sip_id)

    @extract_id
    async def remove_endpoint_sip_async(self, endpoint_sip_id: str) -> Any:
        """Remove a SIP endpoint from the trunk asynchronously.

        Args:
            endpoint_sip_id: SIP endpoint ID

        Returns:
            API response

        """
        return await self.trunk_endpoint_sip.dissociate_async(
            self.trunk_id, endpoint_sip_id
        )

    @extract_id
    def add_endpoint_iax(self, endpoint_iax_id: str) -> Any:
        """Add an IAX endpoint to the trunk.

        Args:
            endpoint_iax_id: IAX endpoint ID

        Returns:
            API response

        """
        return self.trunk_endpoint_iax.associate(self.trunk_id, endpoint_iax_id)

    @extract_id
    async def add_endpoint_iax_async(self, endpoint_iax_id: str) -> Any:
        """Add an IAX endpoint to the trunk asynchronously.

        Args:
            endpoint_iax_id: IAX endpoint ID

        Returns:
            API response

        """
        return await self.trunk_endpoint_iax.associate_async(
            self.trunk_id, endpoint_iax_id
        )

    @extract_id
    def remove_endpoint_iax(self, endpoint_iax_id: str) -> Any:
        """Remove an IAX endpoint from the trunk.

        Args:
            endpoint_iax_id: IAX endpoint ID

        Returns:
            API response

        """
        return self.trunk_endpoint_iax.dissociate(self.trunk_id, endpoint_iax_id)

    @extract_id
    async def remove_endpoint_iax_async(self, endpoint_iax_id: str) -> Any:
        """Remove an IAX endpoint from the trunk asynchronously.

        Args:
            endpoint_iax_id: IAX endpoint ID

        Returns:
            API response

        """
        return await self.trunk_endpoint_iax.dissociate_async(
            self.trunk_id, endpoint_iax_id
        )

    @extract_id
    def add_endpoint_custom(self, endpoint_custom_id: str) -> Any:
        """Add a custom endpoint to the trunk.

        Args:
            endpoint_custom_id: Custom endpoint ID

        Returns:
            API response

        """
        return self.trunk_endpoint_custom.associate(self.trunk_id, endpoint_custom_id)

    @extract_id
    async def add_endpoint_custom_async(self, endpoint_custom_id: str) -> Any:
        """Add a custom endpoint to the trunk asynchronously.

        Args:
            endpoint_custom_id: Custom endpoint ID

        Returns:
            API response

        """
        return await self.trunk_endpoint_custom.associate_async(
            self.trunk_id, endpoint_custom_id
        )

    @extract_id
    def remove_endpoint_custom(self, endpoint_custom_id: str) -> Any:
        """Remove a custom endpoint from the trunk.

        Args:
            endpoint_custom_id: Custom endpoint ID

        Returns:
            API response

        """
        return self.trunk_endpoint_custom.dissociate(self.trunk_id, endpoint_custom_id)

    @extract_id
    async def remove_endpoint_custom_async(self, endpoint_custom_id: str) -> Any:
        """Remove a custom endpoint from the trunk asynchronously.

        Args:
            endpoint_custom_id: Custom endpoint ID

        Returns:
            API response

        """
        return await self.trunk_endpoint_custom.dissociate_async(
            self.trunk_id, endpoint_custom_id
        )

    @extract_id
    def add_register_sip(self, register_sip_id: str) -> Any:
        """Add a SIP register to the trunk.

        Args:
            register_sip_id: SIP register ID

        Returns:
            API response

        """
        return self.trunk_register_sip.associate(self.trunk_id, register_sip_id)

    @extract_id
    async def add_register_sip_async(self, register_sip_id: str) -> Any:
        """Add a SIP register to the trunk asynchronously.

        Args:
            register_sip_id: SIP register ID

        Returns:
            API response

        """
        return await self.trunk_register_sip.associate_async(
            self.trunk_id, register_sip_id
        )

    @extract_id
    def remove_register_sip(self, register_sip_id: str) -> Any:
        """Remove a SIP register from the trunk.

        Args:
            register_sip_id: SIP register ID

        Returns:
            API response

        """
        return self.trunk_register_sip.dissociate(self.trunk_id, register_sip_id)

    @extract_id
    async def remove_register_sip_async(self, register_sip_id: str) -> Any:
        """Remove a SIP register from the trunk asynchronously.

        Args:
            register_sip_id: SIP register ID

        Returns:
            API response

        """
        return await self.trunk_register_sip.dissociate_async(
            self.trunk_id, register_sip_id
        )

    @extract_id
    def add_register_iax(self, register_iax_id: str) -> Any:
        """Add an IAX register to the trunk.

        Args:
            register_iax_id: IAX register ID

        Returns:
            API response

        """
        return self.trunk_register_iax.associate(self.trunk_id, register_iax_id)

    @extract_id
    async def add_register_iax_async(self, register_iax_id: str) -> Any:
        """Add an IAX register to the trunk asynchronously.

        Args:
            register_iax_id: IAX register ID

        Returns:
            API response

        """
        return await self.trunk_register_iax.associate_async(
            self.trunk_id, register_iax_id
        )

    @extract_id
    def remove_register_iax(self, register_iax_id: str) -> Any:
        """Remove an IAX register from the trunk.

        Args:
            register_iax_id: IAX register ID

        Returns:
            API response

        """
        return self.trunk_register_iax.dissociate(self.trunk_id, register_iax_id)

    @extract_id
    async def remove_register_iax_async(self, register_iax_id: str) -> Any:
        """Remove an IAX register from the trunk asynchronously.

        Args:
            register_iax_id: IAX register ID

        Returns:
            API response

        """
        return await self.trunk_register_iax.dissociate_async(
            self.trunk_id, register_iax_id
        )


class TrunksCommand(MultiTenantCommand):
    """Command for managing trunks."""

    resource = "trunks"
    relation_cmd = TrunkRelation
