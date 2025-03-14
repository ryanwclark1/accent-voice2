# accent_bus/resources/call_permission/event.py
# Copyright 2025 Accent Communications

"""Call permission events."""

from accent_bus.resources.common.event import TenantEvent
from accent_bus.resources.common.types import UUIDStr


class CallPermissionCreatedEvent(TenantEvent):
    """Event for when a call permission is created."""

    service = "confd"
    name = "call_permission_created"
    routing_key_fmt = "config.callpermission.created"

    def __init__(self, call_permission_id: int, tenant_uuid: UUIDStr) -> None:
        """Initialize event.

        Args:
          call_permission_id: Call permission ID.
          tenant_uuid: tenant UUID.

        """
        content = {"id": call_permission_id}
        super().__init__(content, tenant_uuid)


class CallPermissionDeletedEvent(TenantEvent):
    """Event for when a call permission is deleted."""

    service = "confd"
    name = "call_permission_deleted"
    routing_key_fmt = "config.callpermission.deleted"

    def __init__(self, call_permission_id: int, tenant_uuid: UUIDStr) -> None:
        """Initialize event.

        Args:
            call_permission_id: Call permission ID.
            tenant_uuid:  tenant UUID

        """
        content = {"id": call_permission_id}
        super().__init__(content, tenant_uuid)


class CallPermissionEditedEvent(TenantEvent):
    """Event for when a call permission is edited."""

    service = "confd"
    name = "call_permission_edited"
    routing_key_fmt = "config.callpermission.edited"

    def __init__(self, call_permission_id: int, tenant_uuid: UUIDStr) -> None:
        """Initialize the event.

        Args:
          call_permission_id: Call Permission ID
          tenant_uuid: tenant UUID

        """
        content = {"id": call_permission_id}
        super().__init__(content, tenant_uuid)
