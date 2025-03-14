# accent_bus/resources/group_schedule/event.py
# Copyright 2025 Accent Communications

"""Group schedule events."""

from accent_bus.resources.common.event import TenantEvent
from accent_bus.resources.common.types import UUIDStr


class GroupScheduleAssociatedEvent(TenantEvent):
    """Event for when a group schedule is associated."""

    service = "confd"
    name = "group_schedule_associated"
    routing_key_fmt = "config.groups.schedules.updated"

    def __init__(
        self,
        group_id: int,
        group_uuid: UUIDStr,
        schedule_id: int,
        tenant_uuid: UUIDStr,
    ) -> None:
        """Initialize Event.

        Args:
           group_id: Group ID
           group_uuid: Group UUID
           schedule_id: Schedule ID
           tenant_uuid: tenant UUID

        """
        content = {
            "group_id": group_id,
            "group_uuid": str(group_uuid),
            "schedule_id": schedule_id,
        }
        super().__init__(content, tenant_uuid)


class GroupScheduleDissociatedEvent(TenantEvent):
    """Event for when a group schedule is dissociated."""

    service = "confd"
    name = "group_schedule_dissociated"
    routing_key_fmt = "config.groups.schedules.deleted"

    def __init__(
        self,
        group_id: int,
        group_uuid: UUIDStr,
        schedule_id: int,
        tenant_uuid: UUIDStr,
    ) -> None:
        """Initialize the event.

        Args:
           group_id: Group ID
           group_uuid: Group UUID
           schedule_id: Schedule ID
           tenant_uuid: tenant UUID

        """
        content = {
            "group_id": group_id,
            "group_uuid": str(group_uuid),
            "schedule_id": schedule_id,
        }
        super().__init__(content, tenant_uuid)
