# accent_bus/resources/outcall_call_permission/event.py
# Copyright 2025 Accent Communications

"""Outcall call permission events."""

from accent_bus.resources.common.event import TenantEvent
from accent_bus.resources.common.types import UUIDStr


class OutcallCallPermissionAssociatedEvent(TenantEvent):
    """Event for when an outcall call permission is associated."""

    service = "confd"
    name = "outcall_call_permission_associated"
    routing_key_fmt = "config.outcalls.{outcall_id}.callpermissions.updated"

    def __init__(
        self,
        outcall_id: int,
        call_permission_id: int,
        tenant_uuid: UUIDStr,
    ) -> None:
        """Initialize Event.

        Args:
           outcall_id: Outcall ID
           call_permission_id: Call permission ID
           tenant_uuid: tenant UUID

        """
        content = {
            "outcall_id": outcall_id,
            "call_permission_id": call_permission_id,
        }
        super().__init__(content, tenant_uuid)


class OutcallCallPermissionDissociatedEvent(TenantEvent):
    """Event for when an outcall call permission is dissociated."""

    service = "confd"
    name = "outcall_call_permission_dissociated"
    routing_key_fmt = "config.outcalls.{outcall_id}.callpermissions.deleted"

    def __init__(
        self,
        outcall_id: int,
        call_permission_id: int,
        tenant_uuid: UUIDStr,
    ) -> None:
        """Initialize the event.

        Args:
           outcall_id: Outcall ID
           call_permission_id: Call Permission ID
           tenant_uuid: tenant UUID

        """
        content = {
            "outcall_id": outcall_id,
            "call_permission_id": call_permission_id,
        }
        super().__init__(content, tenant_uuid)
