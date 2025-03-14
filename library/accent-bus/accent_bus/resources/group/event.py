# resources/group/event.py
from typing import ClassVar

from pydantic import UUID4
from resources.common.event import TenantEvent

from .types import GroupDict


class GroupEvent(TenantEvent):
    """Base class for Group events."""

    service: ClassVar[str] = "confd"
    content: dict


class GroupCreatedEvent(GroupEvent):
    """Event for when a group is created."""

    name: ClassVar[str] = "group_created"
    routing_key_fmt: ClassVar[str] = "config.groups.created"

    def __init__(self, group: GroupDict, **data):
        super().__init__(content=group, **data)


class GroupDeletedEvent(GroupEvent):
    """Event for when a group is deleted."""

    name: ClassVar[str] = "group_deleted"
    routing_key_fmt: ClassVar[str] = "config.groups.deleted"

    def __init__(self, group: GroupDict, **data):
        super().__init__(content=group, **data)


class GroupEditedEvent(GroupEvent):
    """Event for when a group is edited."""

    name: ClassVar[str] = "group_edited"
    routing_key_fmt: ClassVar[str] = "config.groups.edited"

    def __init__(self, group: GroupDict, **data):
        super().__init__(content=group, **data)


class GroupFallbackEditedEvent(GroupEvent):
    """Event for group fallback is edited."""

    name: ClassVar[str] = "group_fallback_edited"
    routing_key_fmt: ClassVar[str] = "config.groups.fallbacks.edited"

    def __init__(
        self,
        group_id: int,
        group_uuid: UUID4,
        **data,
    ):
        content = {
            "id": group_id,
            "uuid": str(group_uuid),
        }
        super().__init__(content=content, **data)
