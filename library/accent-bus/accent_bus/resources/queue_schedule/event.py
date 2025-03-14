# accent_bus/resources/queue_schedule/event.py
# Copyright 2025 Accent Communications

"""Queue schedule events."""

from accent_bus.resources.common.event import TenantEvent
from accent_bus.resources.common.types import UUIDStr


class QueueScheduleAssociatedEvent(TenantEvent):
    """Event for when a queue schedule is associated."""

    service = "confd"
    name = "queue_schedule_associated"
    routing_key_fmt = "config.queues.schedules.updated"

    def __init__(
        self,
        queue_id: int,
        schedule_id: int,
        tenant_uuid: UUIDStr,
    ) -> None:
        """Initialize Event.

        Args:
            queue_id (int): queue ID.
            schedule_id (int): schedule ID.
            tenant_uuid (UUIDStr):  tenant UUID.

        """
        content = {
            "queue_id": queue_id,
            "schedule_id": schedule_id,
        }
        super().__init__(content, tenant_uuid)


class QueueScheduleDissociatedEvent(TenantEvent):
    """Event for when a queue schedule is dissociated."""

    service = "confd"
    name = "queue_schedule_dissociated"
    routing_key_fmt = "config.queues.schedules.deleted"

    def __init__(
        self,
        queue_id: int,
        schedule_id: int,
        tenant_uuid: UUIDStr,
    ) -> None:
        """Initialize the event.

        Args:
           queue_id: Queue ID
           schedule_id: Schedule ID
           tenant_uuid: tenant UUID

        """
        content = {
            "queue_id": queue_id,
            "schedule_id": schedule_id,
        }
        super().__init__(content, tenant_uuid)
