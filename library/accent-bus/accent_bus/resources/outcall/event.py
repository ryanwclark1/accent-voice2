# accent_bus/resources/outcall/event.py
# Copyright 2025 Accent Communications

"""Outcall events."""

from accent_bus.resources.common.event import TenantEvent
from accent_bus.resources.common.types import UUIDStr


class OutcallCreatedEvent(TenantEvent):
    """Event for when an outcall is created."""

    service = "confd"
    name = "outcall_created"
    routing_key_fmt = "config.outcalls.created"

    def __init__(self, outcall_id: int, tenant_uuid: UUIDStr) -> None:
        """Initialize Event.

        Args:
            outcall_id (int): outcall ID.
            tenant_uuid (UUIDStr):  tenant UUID.

        """
        content = {"id": outcall_id}
        super().__init__(content, tenant_uuid)


class OutcallDeletedEvent(TenantEvent):
    """Event for when an outcall is deleted."""

    service = "confd"
    name = "outcall_deleted"
    routing_key_fmt = "config.outcalls.deleted"

    def __init__(self, outcall_id: int, tenant_uuid: UUIDStr) -> None:
        """Initialize event.

        Args:
          outcall_id: Outcall ID
          tenant_uuid: tenant UUID

        """
        content = {"id": outcall_id}
        super().__init__(content, tenant_uuid)


class OutcallEditedEvent(TenantEvent):
    """Event for when an outcall is edited."""

    service = "confd"
    name = "outcall_edited"
    routing_key_fmt = "config.outcalls.edited"

    def __init__(self, outcall_id: int, tenant_uuid: UUIDStr) -> None:
        """Initialize the event.

        Args:
            outcall_id (int): outcall ID.
            tenant_uuid (UUIDStr): The tenant UUID.

        """
        content = {"id": outcall_id}
        super().__init__(content, tenant_uuid)
