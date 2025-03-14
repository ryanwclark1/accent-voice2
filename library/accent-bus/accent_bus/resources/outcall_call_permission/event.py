# resources/outcall_call_permission/event.py
from typing import ClassVar

from accent_bus.resources.common.event import TenantEvent


class OutcallCallPermissionEvent(TenantEvent):
    """Base class for Outcall Call Permission events."""

    service: ClassVar[str] = "confd"
    content: dict


class OutcallCallPermissionAssociatedEvent(OutcallCallPermissionEvent):
    """Event for when a call permission is associated with an outcall."""

    name: ClassVar[str] = "outcall_call_permission_associated"
    routing_key_fmt: ClassVar[str] = (
        "config.outcalls.{outcall_id}.callpermissions.updated"
    )

    def __init__(
        self,
        outcall_id: int,
        call_permission_id: int,
        **data,
    ):
        content = {
            "outcall_id": outcall_id,
            "call_permission_id": call_permission_id,
        }
        super().__init__(content=content, **data)


class OutcallCallPermissionDissociatedEvent(OutcallCallPermissionEvent):
    """Event for when a call permission is dissociated from an outcall."""

    name: ClassVar[str] = "outcall_call_permission_dissociated"
    routing_key_fmt: ClassVar[str] = (
        "config.outcalls.{outcall_id}.callpermissions.deleted"
    )

    def __init__(self, outcall_id: int, call_permission_id: int, **data):
        content = {
            "outcall_id": outcall_id,
            "call_permission_id": call_permission_id,
        }
        super().__init__(content=content, **data)
