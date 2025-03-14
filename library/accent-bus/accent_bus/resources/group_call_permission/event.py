# resources/group_call_permission/event.py
from typing import ClassVar

from pydantic import UUID4

from accent_bus.resources.common.event import TenantEvent


class GroupCallPermissionEvent(TenantEvent):
    """Base class for Group Call Permission events."""

    service: ClassVar[str] = "confd"
    content: dict


class GroupCallPermissionAssociatedEvent(GroupCallPermissionEvent):
    """Event for when a call permission is associated with a group."""

    name: ClassVar[str] = "group_call_permission_associated"
    routing_key_fmt: ClassVar[str] = (
        "config.groups.{group_uuid}.callpermissions.updated"
    )

    def __init__(
        self,
        group_id: int,
        group_uuid: UUID4,
        call_permission_id: int,
        **data,
    ):
        content = {
            "group_id": group_id,
            "group_uuid": str(group_uuid),
            "call_permission_id": call_permission_id,
        }
        super().__init__(content=content, **data)


class GroupCallPermissionDissociatedEvent(GroupCallPermissionEvent):
    """Event for when a call permission is dissociated from a group."""

    name: ClassVar[str] = "group_call_permission_dissociated"
    routing_key_fmt: ClassVar[str] = (
        "config.groups.{group_uuid}.callpermissions.deleted"
    )

    def __init__(
        self,
        group_id: int,
        group_uuid: UUID4,
        call_permission_id: int,
        **data,
    ):
        content = {
            "group_id": group_id,
            "group_uuid": str(group_uuid),
            "call_permission_id": call_permission_id,
        }
        super().__init__(content=content, **data)
