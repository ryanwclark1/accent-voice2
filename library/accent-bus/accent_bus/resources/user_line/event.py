# resources/user_line/event.py
from typing import ClassVar

from accent_bus.resources.common.event import UserEvent  # Correct import

from .types import LineDict, UserDict


class UserLineEvent(UserEvent):
    """Base class for User Line events."""

    service: ClassVar[str] = "confd"
    content: dict


class UserLineAssociatedEvent(UserLineEvent):
    """Event for when a line is associated with a user."""

    name: ClassVar[str] = "user_line_associated"
    routing_key_fmt: ClassVar[str] = "config.users.{user_uuid}.lines.{line[id]}.updated"

    def __init__(
        self,
        user: UserDict,
        line: LineDict,
        main_user: bool,
        main_line: bool,
        **data,
    ):
        content = {
            "line": line,
            "main_line": main_line,
            "main_user": main_user,
            "user": user,
        }
        super().__init__(content=content, **data)


class UserLineDissociatedEvent(UserLineEvent):
    """Event for when a line is dissociated from a user."""

    name: ClassVar[str] = "user_line_dissociated"
    routing_key_fmt: ClassVar[str] = "config.users.{user_uuid}.lines.{line[id]}.deleted"

    def __init__(
        self,
        user: UserDict,
        line: LineDict,
        main_user: bool,
        main_line: bool,
        **data,
    ):
        content = {
            "line": line,
            "main_line": main_line,
            "main_user": main_user,
            "user": user,
        }
        super().__init__(content=content, **data)
