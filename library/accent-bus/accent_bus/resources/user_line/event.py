# accent_bus/resources/user_line/event.py
# Copyright 2025 Accent Communications

"""User line events."""

from accent_bus.resources.common.event import UserEvent
from accent_bus.resources.common.types import UUIDStr

from .types import LineDict, UserDict


class UserLineAssociatedEvent(UserEvent):
    """Event for when a user line is associated."""

    service = "confd"
    name = "user_line_associated"
    routing_key_fmt = "config.users.{user_uuid}.lines.{line[id]}.updated"

    def __init__(
        self,
        user: UserDict,
        line: LineDict,
        main_user: bool,
        main_line: bool,
        tenant_uuid: UUIDStr,
    ) -> None:
        """Initialize event.

        Args:
            user (UserDict): user details.
            line (LineDict): line details.
            main_user (bool): True if the user is the main user of the line.
            main_line (bool): True if the line is the main line of the user
            tenant_uuid (UUIDStr): The tenant UUID.

        """
        content = {
            "line": line,
            "main_line": main_line,
            "main_user": main_user,
            "user": user,
        }
        super().__init__(content, tenant_uuid, user["uuid"])


class UserLineDissociatedEvent(UserEvent):
    """Event for when a user line is dissociated."""

    service = "confd"
    name = "user_line_dissociated"
    routing_key_fmt = "config.users.{user_uuid}.lines.{line[id]}.deleted"

    def __init__(
        self,
        user: UserDict,
        line: LineDict,
        main_user: bool,
        main_line: bool,
        tenant_uuid: UUIDStr,
    ) -> None:
        """Initialize event.

        Args:
            user (UserDict): The user details.
            line (LineDict):  line details.
            main_user (bool): True if user is main user of the line
            main_line (bool): True if the line is main line of the user.
            tenant_uuid (UUIDStr): tenant UUID.

        """
        content = {
            "line": line,
            "main_line": main_line,
            "main_user": main_user,
            "user": user,
        }
        super().__init__(content, tenant_uuid, user["uuid"])
