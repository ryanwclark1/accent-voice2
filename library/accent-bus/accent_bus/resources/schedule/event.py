# accent_bus/resources/schedule/event.py
# Copyright 2025 Accent Communications

"""Schedule events."""

from accent_bus.resources.common.event import TenantEvent
from accent_bus.resources.common.types import UUIDStr


class ScheduleCreatedEvent(TenantEvent):
    """Event for when a schedule is created."""

    service = "confd"
    name = "schedule_created"
    routing_key_fmt = "config.schedules.created"

    def __init__(self, schedule_id: int, tenant_uuid: UUIDStr) -> None:
        """Initialize event.

        Args:
            schedule_id: Schedule ID
            tenant_uuid: tenant UUID

        """
        content = {"id": int(schedule_id)}
        super().__init__(content, tenant_uuid)


class ScheduleDeletedEvent(TenantEvent):
    """Event for when a schedule is deleted."""

    service = "confd"
    name = "schedule_deleted"
    routing_key_fmt = "config.schedules.deleted"

    def __init__(self, schedule_id: int, tenant_uuid: UUIDStr) -> None:
        """Initialize the event.

        Args:
            schedule_id (int):  schedule ID.
            tenant_uuid (UUIDStr): tenant UUID.

        """
        content = {"id": int(schedule_id)}
        super().__init__(content, tenant_uuid)


class ScheduleEditedEvent(TenantEvent):
    """Event for when a schedule is edited."""

    service = "confd"
    name = "schedule_edited"
    routing_key_fmt = "config.schedules.edited"

    def __init__(self, schedule_id: int, tenant_uuid: UUIDStr) -> None:
        """Initialize event.

        Args:
           schedule_id: Schedule ID
           tenant_uuid: tenant UUID

        """
        content = {"id": int(schedule_id)}
        super().__init__(content, tenant_uuid)
