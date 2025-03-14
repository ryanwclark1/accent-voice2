# accent_bus/resources/incall_schedule/event.py
# Copyright 2025 Accent Communications

"""Incall schedule events."""

from accent_bus.resources.common.event import TenantEvent
from accent_bus.resources.common.types import UUIDStr


class IncallScheduleAssociatedEvent(TenantEvent):
    """Event for when an incall schedule is associated."""

    service = "confd"
    name = "incall_schedule_associated"
    routing_key_fmt = "config.incalls.schedules.updated"

    def __init__(
        self,
        incall_id: int,
        schedule_id: int,
        tenant_uuid: UUIDStr,
    ) -> None:
        """Initialize the event.

        Args:
           incall_id: Incall ID
           schedule_id: Schedule ID
           tenant_uuid: tenant UUID

        """
        content = {
            "incall_id": incall_id,
            "schedule_id": schedule_id,
        }
        super().__init__(content, tenant_uuid)


class IncallScheduleDissociatedEvent(TenantEvent):
    """Event for when an incall schedule is dissociated."""

    service = "confd"
    name = "incall_schedule_dissociated"
    routing_key_fmt = "config.incalls.schedules.deleted"

    def __init__(
        self,
        incall_id: int,
        schedule_id: int,
        tenant_uuid: UUIDStr,
    ) -> None:
        """Initialize event.

        Args:
          incall_id: Incall ID
          schedule_id: Schedule ID
          tenant_uuid: tenant UUID

        """
        content = {
            "incall_id": incall_id,
            "schedule_id": schedule_id,
        }
        super().__init__(content, tenant_uuid)
