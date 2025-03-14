# resources/user_call_permission/event.py
from typing import ClassVar

from resources.common.event import UserEvent


class UserCallPermissionEvent(UserEvent):
    """Base class for User Call Permission events."""

    service: ClassVar[str] = "confd"
    content: dict


class UserCallPermissionAssociatedEvent(UserCallPermissionEvent):
    """Event for when a call permission is associated with a user."""

    name: ClassVar[str] = "user_call_permission_associated"
    routing_key_fmt: ClassVar[str] = "config.users.{user_uuid}.callpermissions.updated"

    def __init__(self, call_permission_id: int, **data):
        content = {
            "user_uuid": str(data["user_uuid"]),
            "call_permission_id": call_permission_id,
        }
        super().__init__(content=content, **data)


class UserCallPermissionDissociatedEvent(UserCallPermissionEvent):
    """Event for when a call permission is dissociated from a user."""

    name: ClassVar[str] = "user_call_permission_dissociated"
    routing_key_fmt: ClassVar[str] = "config.users.{user_uuid}.callpermissions.deleted"

    def __init__(self, call_permission_id: int, **data):
        content = {
            "user_uuid": str(data["user_uuid"]),
            "call_permission_id": call_permission_id,
        }
        super().__init__(content=content, **data)
