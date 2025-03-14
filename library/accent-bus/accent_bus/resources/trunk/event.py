# accent_bus/resources/trunk/event.py
# Copyright 2025 Accent Communications

"""Trunk events."""

from accent_bus.resources.common.event import TenantEvent
from accent_bus.resources.common.types import UUIDStr


class TrunkCreatedEvent(TenantEvent):
    """Event for when a trunk is created."""

    service = "confd"
    name = "trunk_created"
    routing_key_fmt = "config.trunk.created"

    def __init__(self, trunk_id: int, tenant_uuid: UUIDStr) -> None:
        """Initialize event.

        Args:
          trunk_id: Trunk ID
          tenant_uuid: tenant UUID

        """
        content = {"id": int(trunk_id)}
        super().__init__(content, tenant_uuid)


class TrunkDeletedEvent(TenantEvent):
    """Event for when a trunk is deleted."""

    service = "confd"
    name = "trunk_deleted"
    routing_key_fmt = "config.trunk.deleted"

    def __init__(self, trunk_id: int, tenant_uuid: UUIDStr) -> None:
        """Initialize Event.

        Args:
           trunk_id: Trunk ID
           tenant_uuid: tenant UUID

        """
        content = {"id": int(trunk_id)}
        super().__init__(content, tenant_uuid)


class TrunkEditedEvent(TenantEvent):
    """Event for when a trunk is edited."""

    service = "confd"
    name = "trunk_edited"
    routing_key_fmt = "config.trunk.edited"

    def __init__(self, trunk_id: int, tenant_uuid: UUIDStr) -> None:
        """Initialize event.

        Args:
            trunk_id (int): The ID of the trunk.
            tenant_uuid (UUIDStr): The tenant UUID.

        """
        content = {"id": int(trunk_id)}
        super().__init__(content, tenant_uuid)


class TrunkStatusUpdatedEvent(TenantEvent):
    """Event for when a trunk status is updated."""

    service = "calld"
    name = "trunk_status_updated"
    routing_key_fmt = "trunks.{id}.status.updated"

    def __init__(
        self,
        trunk_id: int,
        technology: str,
        endpoint_name: str,
        endpoint_registered: bool,
        endpoint_current_call_count: int,
        tenant_uuid: UUIDStr,
    ) -> None:
        """Initialize event.

        Args:
            trunk_id (int): The ID of the trunk.
            technology (str): technology.
            endpoint_name (str): endpoint name.
            endpoint_registered (bool): True if endpoint registered.
            endpoint_current_call_count (int): Number of calls.
            tenant_uuid (UUIDStr): The tenant UUID.

        """
        content = {
            "id": trunk_id,
            "technology": technology,
            "name": endpoint_name,
            "registered": endpoint_registered,
            "current_call_count": endpoint_current_call_count,
        }
        super().__init__(content, tenant_uuid)
