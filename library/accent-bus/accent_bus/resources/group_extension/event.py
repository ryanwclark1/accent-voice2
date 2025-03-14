# accent_bus/resources/group_extension/event.py
# Copyright 2025 Accent Communications

"""Group extension events."""

from accent_bus.resources.common.event import TenantEvent
from accent_bus.resources.common.types import UUIDStr


class GroupExtensionAssociatedEvent(TenantEvent):
    """Event for when a group extension is associated."""

    service = "confd"
    name = "group_extension_associated"
    routing_key_fmt = "config.groups.extensions.updated"

    def __init__(
        self,
        group_id: int,
        group_uuid: UUIDStr,
        extension_id: int,
        tenant_uuid: UUIDStr,
    ) -> None:
        """Initialize event.

        Args:
           group_id: Group ID
           group_uuid: Group UUID
           extension_id: Extension ID
           tenant_uuid: tenant UUID

        """
        content = {
            "group_id": group_id,
            "group_uuid": str(group_uuid),
            "extension_id": extension_id,
        }
        super().__init__(content, tenant_uuid)


class GroupExtensionDissociatedEvent(TenantEvent):
    """Event for when a group extension is dissociated."""

    service = "confd"
    name = "group_extension_dissociated"
    routing_key_fmt = "config.groups.extensions.deleted"

    def __init__(
        self,
        group_id: int,
        group_uuid: UUIDStr,
        extension_id: int,
        tenant_uuid: UUIDStr,
    ) -> None:
        """Initialize the event.

        Args:
            group_id (int):  group ID.
            group_uuid (UUIDStr): group UUID.
            extension_id (int): Extension ID.
            tenant_uuid (UUIDStr): tenant UUID.

        """
        content = {
            "group_id": group_id,
            "group_uuid": str(group_uuid),
            "extension_id": extension_id,
        }
        super().__init__(content, tenant_uuid)
