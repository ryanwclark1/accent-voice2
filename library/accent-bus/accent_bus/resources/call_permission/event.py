# resources/call_permission/event.py
from typing import ClassVar

from accent_bus.resources.common.event import TenantEvent


class CallPermissionEvent(TenantEvent):
    """Base class for Call Permission events."""

    service: ClassVar[str] = "confd"
    content: dict


class CallPermissionCreatedEvent(CallPermissionEvent):
    """Event for when a call permission is created."""

    name: ClassVar[str] = "call_permission_created"
    routing_key_fmt: ClassVar[str] = "config.callpermission.created"

    def __init__(self, call_permission_id: int, **data):
        content = {"id": call_permission_id}
        super().__init__(content=content, **data)


class CallPermissionDeletedEvent(CallPermissionEvent):
    """Event for when a call permission is deleted."""

    name: ClassVar[str] = "call_permission_deleted"
    routing_key_fmt: ClassVar[str] = "config.callpermission.deleted"

    def __init__(self, call_permission_id: int, **data):
        content = {"id": call_permission_id}
        super().__init__(content=content, **data)


class CallPermissionEditedEvent(CallPermissionEvent):
    """Event for when a call permission is edited."""

    name: ClassVar[str] = "call_permission_edited"
    routing_key_fmt: ClassVar[str] = "config.callpermission.edited"

    def __init__(self, call_permission_id: int, **data):
        content = {"id": call_permission_id}
        super().__init__(content=content, **data)
