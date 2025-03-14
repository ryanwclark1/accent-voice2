# accent_bus/resources/group/event.py
# Copyright 2025 Accent Communications

"""Group events."""

from accent_bus.resources.common.event import TenantEvent
from accent_bus.resources.common.types import UUIDStr

from .types import GroupDict


class GroupCreatedEvent(TenantEvent):
    """Event for when a group is created."""

    service = "confd"
    name = "group_created"
    routing_key_fmt = "config.groups.created"

    def __init__(self, group: GroupDict, tenant_uuid: UUIDStr) -> None:
        """Initialize event.

        Args:
          group: Group
          tenant_uuid: tenant UUID

        """
        super().__init__(group, tenant_uuid)


class GroupDeletedEvent(TenantEvent):
    """Event for when a group is deleted."""

    service = "confd"
    name = "group_deleted"
    routing_key_fmt = "config.groups.deleted"

    def __init__(self, group: GroupDict, tenant_uuid: UUIDStr) -> None:
        """Initialize event.

        Args:
            group (GroupDict): group.
            tenant_uuid (UUIDStr): The tenant UUID.

        """
        super().__init__(group, tenant_uuid)


class GroupEditedEvent(TenantEvent):
    """Event for when a group is edited."""

    service = "confd"
    name = "group_edited"
    routing_key_fmt = "config.groups.edited"

    def __init__(self, group: GroupDict, tenant_uuid: UUIDStr) -> None:
        """Initialize event.

        Args:
            group (GroupDict): group details.
            tenant_uuid (UUIDStr): tenant UUID.

        """
        super().__init__(group, tenant_uuid)


class GroupFallbackEditedEvent(TenantEvent):
    """Event for when group fallback is edited."""

    service = "confd"
    name = "group_fallback_edited"
    routing_key_fmt = "config.groups.fallbacks.edited"

    def __init__(
        self,
        group_id: int,
        group_uuid: UUIDStr,
        tenant_uuid: UUIDStr,
    ) -> None:
        """Initialize the event.

        Args:
           group_id: Group ID
           group_uuid: Group UUID
           tenant_uuid: tenant UUID

        """
        content = {
            "id": group_id,
            "uuid": str(group_uuid),
        }
        super().__init__(content, tenant_uuid)
