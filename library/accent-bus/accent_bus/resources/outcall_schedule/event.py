# accent_bus/resources/outcall_schedule/event.py
# Copyright 2025 Accent Communications

"""Outcall schedule events."""

from accent_bus.resources.common.event import TenantEvent
from accent_bus.resources.common.types import UUIDStr


class OutcallScheduleAssociatedEvent(TenantEvent):
    """Event for when an outcall schedule is associated."""

    service = "confd"
    name = "outcall_schedule_associated"
    routing_key_fmt = "config.outcalls.schedules.updated"

    def __init__(
        self,
        outcall_id: int,
        schedule_id: int,
        tenant_uuid: UUIDStr,
    ) -> None:
        """Initialize the event.

        Args:
           outcall_id: Outcall ID
           schedule_id: Schedule ID
           tenant_uuid: tenant UUID

        """
        content = {
            "outcall_id": outcall_id,
            "schedule_id": schedule_id,
        }
        super().__init__(content, tenant_uuid)


class OutcallScheduleDissociatedEvent(TenantEvent):
    """Event for when an outcall schedule is dissociated."""

    service = "confd"
    name = "outcall_schedule_dissociated"
    routing_key_fmt = "config.outcalls.schedules.deleted"

    def __init__(
        self,
        outcall_id: int,
        schedule_id: int,
        tenant_uuid: UUIDStr,
    ) -> None:
        """Initialize event.

        Args:
           outcall_id: Outcall ID
           schedule_id: Schedule ID
           tenant_uuid: tenant UUID

        """
        content = {
            "outcall_id": outcall_id,
            "schedule_id": schedule_id,
        }
        super().__init__(content, tenant_uuid)
