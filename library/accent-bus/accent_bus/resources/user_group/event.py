# accent_bus/resources/user_group/event.py
# Copyright 2025 Accent Communications

"""User group events."""

from accent_bus.resources.common.event import UserEvent
from accent_bus.resources.common.types import UUIDStr


class UserGroupsAssociatedEvent(UserEvent):
    """Event for when groups are associated with a user."""

    service = "confd"
    name = "user_groups_associated"
    routing_key_fmt = "config.users.groups.updated"

    def __init__(
        self,
        group_ids: list[int],
        tenant_uuid: UUIDStr,
        user_uuid: UUIDStr,
    ) -> None:
        """Initialize event.

        Args:
           group_ids: List of Group ID
           tenant_uuid: tenant UUID
           user_uuid: user UUID

        """
        content = {
            "user_uuid": str(user_uuid),
            "group_ids": group_ids,
        }
        super().__init__(content, tenant_uuid, user_uuid)
