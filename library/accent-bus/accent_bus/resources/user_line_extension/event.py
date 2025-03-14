# resources/user_line_extension/event.py
from typing import ClassVar

from accent_bus.resources.common.event import UserEvent  # Correct import


class UserLineExtensionEvent(UserEvent):
    """Base class for User Line Extension events."""

    service: ClassVar[str] = "confd"
    content: dict


class UserLineExtensionCreatedEvent(UserLineExtensionEvent):
    """Event for when a user line extension is created."""

    name: ClassVar[str] = "user_line_extension_created"
    routing_key_fmt: ClassVar[str] = "config.users.lines.extensions.created"

    def __init__(
        self,
        user_line_extension_id: int,
        user_id: int,
        line_id: int,
        extension_id: int,
        main_user: bool,
        main_line: bool,
        **data,
    ):
        content = {
            "id": int(user_line_extension_id),
            "user_id": int(user_id),
            "line_id": int(line_id),
            "extension_id": int(extension_id),
            "main_user": bool(main_user),
            "main_line": bool(main_line),
        }
        super().__init__(content=content, **data)


class UserLineExtensionDeletedEvent(UserLineExtensionEvent):
    """Event for when a user line extension is deleted."""

    name: ClassVar[str] = "user_line_extension_deleted"
    routing_key_fmt: ClassVar[str] = "config.users.lines.extensions.deleted"

    def __init__(
        self,
        user_line_extension_id: int,
        user_id: int,
        line_id: int,
        extension_id: int,
        main_user: bool,
        main_line: bool,
        **data,
    ):
        content = {
            "id": int(user_line_extension_id),
            "user_id": int(user_id),
            "line_id": int(line_id),
            "extension_id": int(extension_id),
            "main_user": bool(main_user),
            "main_line": bool(main_line),
        }
        super().__init__(content=content, **data)


class UserLineExtensionEditedEvent(UserLineExtensionEvent):
    """Event for when a user line extension is edited."""

    name: ClassVar[str] = "user_line_extension_edited"
    routing_key_fmt: ClassVar[str] = "config.users.lines.extensions.edited"

    def __init__(
        self,
        user_line_extension_id: int,
        user_id: int,
        line_id: int,
        extension_id: int,
        main_user: bool,
        main_line: bool,
        **data,
    ):
        content = {
            "id": int(user_line_extension_id),
            "user_id": int(user_id),
            "line_id": int(line_id),
            "extension_id": int(extension_id),
            "main_user": bool(main_user),
            "main_line": bool(main_line),
        }
        super().__init__(content=content, **data)
