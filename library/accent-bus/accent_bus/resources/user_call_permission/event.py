# accent_bus/resources/user_call_permission/event.py
# Copyright 2025 Accent Communications

"""User call permission events."""

from accent_bus.resources.common.event import UserEvent
from accent_bus.resources.common.types import UUIDStr


class UserCallPermissionAssociatedEvent(UserEvent):
    """Event for when a user call permission is associated."""

    service = "confd"
    name = "user_call_permission_associated"
    routing_key_fmt = "config.users.{user_uuid}.callpermissions.updated"

    def __init__(
        self,
        call_permission_id: int,
        tenant_uuid: UUIDStr,
        user_uuid: UUIDStr,
    ) -> None:
        """Initialize the event.

        Args:
            call_permission_id (int):  call permission ID.
            tenant_uuid (UUIDStr): tenant UUID.
            user_uuid (UUIDStr):  user UUID.

        """
        content = {
            "user_uuid": str(user_uuid),
            "call_permission_id": call_permission_id,
        }
        super().__init__(content, tenant_uuid, user_uuid)


class UserCallPermissionDissociatedEvent(UserEvent):
    """Event for when a user call permission is dissociated."""

    service = "confd"
    name = "user_call_permission_dissociated"
    routing_key_fmt = "config.users.{user_uuid}.callpermissions.deleted"

    def __init__(
        self,
        call_permission_id: int,
        tenant_uuid: UUIDStr,
        user_uuid: UUIDStr,
    ) -> None:
        """Initialize Event.

        Args:
          call_permission_id: Call Permission ID
          tenant_uuid: tenant UUID
          user_uuid: user UUID

        """
        content = {
            "user_uuid": str(user_uuid),
            "call_permission_id": call_permission_id,
        }
        super().__init__(content, tenant_uuid, user_uuid)
