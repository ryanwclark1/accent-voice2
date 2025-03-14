# accent_bus/resources/group_call_permission/event.py
# Copyright 2025 Accent Communications

"""Group call permission events."""

from accent_bus.resources.common.event import TenantEvent
from accent_bus.resources.common.types import UUIDStr


class GroupCallPermissionAssociatedEvent(TenantEvent):
    """Event for when a group call permission is associated."""

    service = "confd"
    name = "group_call_permission_associated"
    routing_key_fmt = "config.groups.{group_uuid}.callpermissions.updated"

    def __init__(
        self,
        group_id: int,
        group_uuid: UUIDStr,
        call_permission_id: int,
        tenant_uuid: UUIDStr,
    ) -> None:
        """Initialize event.

        Args:
          group_id: Group ID
          group_uuid: Group UUID
          call_permission_id: Call permission ID
          tenant_uuid: tenant UUID

        """
        content = {
            "group_id": group_id,
            "group_uuid": str(group_uuid),
            "call_permission_id": call_permission_id,
        }
        super().__init__(content, tenant_uuid)


class GroupCallPermissionDissociatedEvent(TenantEvent):
    """Event for when a group call permission is dissociated."""

    service = "confd"
    name = "group_call_permission_dissociated"
    routing_key_fmt = "config.groups.{group_uuid}.callpermissions.deleted"

    def __init__(
        self,
        group_id: int,
        group_uuid: UUIDStr,
        call_permission_id: int,
        tenant_uuid: UUIDStr,
    ) -> None:
        """Initialize the event.

        Args:
           group_id: Group ID
           group_uuid: Group UUID
           call_permission_id: Call Permission ID
           tenant_uuid: tenant UUID

        """
        content = {
            "group_id": group_id,
            "group_uuid": str(group_uuid),
            "call_permission_id": call_permission_id,
        }
        super().__init__(content, tenant_uuid)
