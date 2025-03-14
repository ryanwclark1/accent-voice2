# resources/paging_user/event.py
from typing import ClassVar

from accent_bus.resources.common.event import TenantEvent


class PagingUserEvent(TenantEvent):
    """Base class for Paging User events."""

    service: ClassVar[str] = "confd"
    content: dict


class PagingCallerUsersAssociatedEvent(PagingUserEvent):
    """Event for associating caller users with a paging group."""

    name: ClassVar[str] = "paging_caller_users_associated"
    routing_key_fmt: ClassVar[str] = "config.pagings.callers.users.updated"

    def __init__(
        self,
        paging_id: int,
        users: list[str],
        **data,
    ):
        content = {
            "paging_id": paging_id,
            "user_uuids": users,
        }
        super().__init__(content=content, **data)


class PagingMemberUsersAssociatedEvent(PagingUserEvent):
    """Event for when member users are associated with a paging group."""

    name: ClassVar[str] = "paging_member_users_associated"
    routing_key_fmt: ClassVar[str] = "config.pagings.members.users.updated"

    def __init__(
        self,
        paging_id: int,
        users: list[str],
        **data,
    ):
        content = {
            "paging_id": paging_id,
            "user_uuids": users,
        }
        super().__init__(content=content, **data)
