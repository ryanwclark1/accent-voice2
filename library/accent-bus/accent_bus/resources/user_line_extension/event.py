# accent_bus/resources/user_line_extension/event.py
# Copyright 2025 Accent Communications

"""User line extension events."""

from accent_bus.resources.common.event import UserEvent
from accent_bus.resources.common.types import UUIDStr


class _BaseUserLineExtensionEvent(UserEvent):
    """Base class for user line extension events."""

    def __init__(
        self,
        user_line_extension_id: int,
        user_id: int,
        line_id: int,
        extension_id: int,
        main_user: bool,
        main_line: bool,
        tenant_uuid: UUIDStr,
        user_uuid: UUIDStr,
    ) -> None:
        """Initialize BaseUserLineExtension Event.

        Args:
           user_line_extension_id: User Line Extension ID
           user_id: User ID
           line_id: Line ID
           extension_id: Extension ID
           main_user: if user is main user
           main_line: if line is main line
           tenant_uuid: tenant UUID
           user_uuid: user UUID

        """
        content = {
            "id": int(user_line_extension_id),
            "user_id": int(user_id),
            "line_id": int(line_id),
            "extension_id": int(extension_id),
            "main_user": bool(main_user),
            "main_line": bool(main_line),
        }
        super().__init__(content, tenant_uuid, user_uuid)


class UserLineExtensionCreatedEvent(_BaseUserLineExtensionEvent):
    """Event for when a user line extension is created."""

    service = "confd"
    name = "user_line_extension_created"
    routing_key_fmt = "config.users.lines.extensions.created"


class UserLineExtensionDeletedEvent(_BaseUserLineExtensionEvent):
    """Event for when a user line extension is deleted."""

    service = "confd"
    name = "user_line_extension_deleted"
    routing_key_fmt = "config.users.lines.extensions.deleted"


class UserLineExtensionEditedEvent(_BaseUserLineExtensionEvent):
    """Event for when a user line extension is edited."""

    service = "confd"
    name = "user_line_extension_edited"
    routing_key_fmt = "config.users.lines.extensions.edited"
