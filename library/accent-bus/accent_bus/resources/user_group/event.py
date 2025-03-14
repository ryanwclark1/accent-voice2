# resources/user_group/event.py
from typing import ClassVar

from resources.common.event import UserEvent


class UserGroupEvent(UserEvent):
    """Base class for User Group events."""

    service: ClassVar[str] = "confd"
    content: dict


class UserGroupsAssociatedEvent(UserGroupEvent):
    """Event for when groups are associated with a user."""

    name: ClassVar[str] = "user_groups_associated"
    routing_key_fmt: ClassVar[str] = "config.users.groups.updated"

    def __init__(self, group_ids: list[int], **data):
        content = {
            "user_uuid": str(data["user_uuid"]),
            "group_ids": group_ids,
        }
        super().__init__(content=content, **data)
