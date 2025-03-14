# accent_bus/resources/trunk_register/event.py
# Copyright 2025 Accent Communications

"""Trunk register events."""

from accent_bus.resources.common.event import TenantEvent
from accent_bus.resources.common.types import UUIDStr


class TrunkRegisterIAXAssociatedEvent(TenantEvent):
    """Event for when an IAX trunk register is associated."""

    service = "confd"
    name = "trunk_register_iax_associated"
    routing_key_fmt = "config.trunks.registers.iax.updated"

    def __init__(
        self,
        trunk_id: int,
        register_id: int,
        tenant_uuid: UUIDStr,
    ) -> None:
        """Initialize the event.

        Args:
           trunk_id: Trunk ID
           register_id: Register ID
           tenant_uuid: tenant UUID

        """
        content = {"trunk_id": trunk_id, "register_id": register_id}
        super().__init__(content, tenant_uuid)


class TrunkRegisterIAXDissociatedEvent(TenantEvent):
    """Event for when an IAX trunk register is dissociated."""

    service = "confd"
    name = "trunk_register_iax_dissociated"
    routing_key_fmt = "config.trunks.registers.iax.deleted"

    def __init__(
        self,
        trunk_id: int,
        register_id: int,
        tenant_uuid: UUIDStr,
    ) -> None:
        """Initialize event.

        Args:
            trunk_id (int): The trunk ID.
            register_id (int): The register ID.
            tenant_uuid (UUIDStr): The tenant UUID.

        """
        content = {
            "trunk_id": trunk_id,
            "register_id": register_id,
        }
        super().__init__(content, tenant_uuid)
