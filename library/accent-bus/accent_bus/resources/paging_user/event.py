# accent_bus/resources/paging_user/event.py
# Copyright 2025 Accent Communications

"""Paging user events."""

from accent_bus.resources.common.event import TenantEvent
from accent_bus.resources.common.types import UUIDStr


class PagingCallerUsersAssociatedEvent(TenantEvent):
    """Event for when caller users are associated with a paging."""

    service = "confd"
    name = "paging_caller_users_associated"
    routing_key_fmt = "config.pagings.callers.users.updated"

    def __init__(
        self,
        paging_id: int,
        users: list[str],
        tenant_uuid: UUIDStr,
    ) -> None:
        """Initialize event.

        Args:
          paging_id: Paging ID
          users: list of user UUIDs
          tenant_uuid: tenant UUID

        """
        content = {
            "paging_id": paging_id,
            "user_uuids": users,
        }
        super().__init__(content, tenant_uuid)


class PagingMemberUsersAssociatedEvent(TenantEvent):
    """Event for when member users are associated with a paging."""

    service = "confd"
    name = "paging_member_users_associated"
    routing_key_fmt = "config.pagings.members.users.updated"

    def __init__(
        self,
        paging_id: int,
        users: list[str],
        tenant_uuid: UUIDStr,
    ) -> None:
        """Initialize event.

        Args:
          paging_id: Paging ID
          users: list of user UUID
          tenant_uuid: tenant UUID

        """
        content = {
            "paging_id": paging_id,
            "user_uuids": users,
        }
        super().__init__(content, tenant_uuid)
