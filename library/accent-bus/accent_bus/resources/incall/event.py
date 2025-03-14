# accent_bus/resources/incall/event.py
# Copyright 2025 Accent Communications

"""Incall events."""

from accent_bus.resources.common.event import TenantEvent
from accent_bus.resources.common.types import UUIDStr


class IncallCreatedEvent(TenantEvent):
    """Event for when an incall is created."""

    service = "confd"
    name = "incall_created"
    routing_key_fmt = "config.incalls.created"

    def __init__(self, incall_id: int, tenant_uuid: UUIDStr) -> None:
        """Initialize the event.

        Args:
            incall_id (int): The ID of the incall.
            tenant_uuid (UUIDStr): The tenant UUID.

        """
        content = {"id": incall_id}
        super().__init__(content, tenant_uuid)


class IncallDeletedEvent(TenantEvent):
    """Event for when an incall is deleted."""

    service = "confd"
    name = "incall_deleted"
    routing_key_fmt = "config.incalls.deleted"

    def __init__(self, incall_id: int, tenant_uuid: UUIDStr) -> None:
        """Initialize the event.

        Args:
            incall_id (int): The ID of the incall.
            tenant_uuid (UUIDStr): The tenant UUID.

        """
        content = {"id": incall_id}
        super().__init__(content, tenant_uuid)


class IncallEditedEvent(TenantEvent):
    """Event for when an incall is edited."""

    service = "confd"
    name = "incall_edited"
    routing_key_fmt = "config.incalls.edited"

    def __init__(self, incall_id: int, tenant_uuid: UUIDStr) -> None:
        """Initialize event.

        Args:
          incall_id: Incall ID
          tenant_uuid: tenant UUID

        """
        content = {"id": incall_id}
        super().__init__(content, tenant_uuid)
