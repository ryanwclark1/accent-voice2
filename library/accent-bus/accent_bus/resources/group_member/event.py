# resources/group_member/event.py
from typing import ClassVar

from pydantic import UUID4

from resources.common.event import TenantEvent
from .types import GroupExtensionDict


class GroupMemberEvent(TenantEvent):
    """Base class for Group Member events."""

    service: ClassVar[str] = "confd"
    content: dict


class GroupMemberUsersAssociatedEvent(GroupMemberEvent):
    """Event for when users are associated as members of a group."""

    name: ClassVar[str] = "group_member_users_associated"
    routing_key_fmt: ClassVar[str] = "config.groups.members.users.updated"

    def __init__(
        self,
        group_id: int,
        group_uuid: UUID4,
        users: list[str],
        **data,
    ):
        content = {
            "group_id": group_id,
            "group_uuid": str(group_uuid),
            "user_uuids": users,
        }
        super().__init__(content=content, **data)


class GroupMemberExtensionsAssociatedEvent(GroupMemberEvent):
    """Event for when extensions are associated as members of a group."""

    name: ClassVar[str] = "group_member_extensions_associated"
    routing_key_fmt: ClassVar[str] = "config.groups.members.extensions.updated"

    def __init__(
        self,
        group_id: int,
        group_uuid: UUID4,
        extensions: list[GroupExtensionDict],
        **data,
    ):
        content = {
            "group_id": group_id,
            "group_uuid": str(group_uuid),
            "extensions": extensions,
        }
        super().__init__(content=content, **data)
