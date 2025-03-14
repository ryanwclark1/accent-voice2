# accent_bus/resources/group_member/event.py
# Copyright 2025 Accent Communications

"""Group member events."""

from accent_bus.resources.common.event import TenantEvent
from accent_bus.resources.common.types import UUIDStr

from .types import GroupExtensionDict


class GroupMemberUsersAssociatedEvent(TenantEvent):
    """Event for when users are associated with a group member."""

    service = "confd"
    name = "group_member_users_associated"
    routing_key_fmt = "config.groups.members.users.updated"

    def __init__(
        self,
        group_id: int,
        group_uuid: UUIDStr,
        users: list[str],
        tenant_uuid: UUIDStr,
    ) -> None:
        """Initialize event.

        Args:
            group_id (int):  group ID.
            group_uuid (UUIDStr):  group UUID.
            users (list[str]): A list of user UUIDs.
            tenant_uuid (UUIDStr): tenant UUID.

        """
        content = {
            "group_id": group_id,
            "group_uuid": str(group_uuid),
            "user_uuids": users,
        }
        super().__init__(content, tenant_uuid)


class GroupMemberExtensionsAssociatedEvent(TenantEvent):
    """Event for when extensions are associated with a group member."""

    service = "confd"
    name = "group_member_extensions_associated"
    routing_key_fmt = "config.groups.members.extensions.updated"

    def __init__(
        self,
        group_id: int,
        group_uuid: UUIDStr,
        extensions: list[GroupExtensionDict],
        tenant_uuid: UUIDStr,
    ) -> None:
        """Initialize Event.

        Args:
            group_id (int): group ID.
            group_uuid (UUIDStr):  group UUID.
            extensions (list[GroupExtensionDict]): A list of extensions.
            tenant_uuid (UUIDStr):  tenant UUID.

        """
        content = {
            "group_id": group_id,
            "group_uuid": str(group_uuid),
            "extensions": extensions,
        }
        super().__init__(content, tenant_uuid)
