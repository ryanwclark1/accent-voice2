# resources/queue_schedule/event.py
from typing import ClassVar

from accent_bus.resources.common.event import TenantEvent


class QueueScheduleEvent(TenantEvent):
    """Base class for Queue Schedule events."""

    service: ClassVar[str] = "confd"
    content: dict


class QueueScheduleAssociatedEvent(QueueScheduleEvent):
    """Event for when a schedule is associated with a queue."""

    name: ClassVar[str] = "queue_schedule_associated"
    routing_key_fmt: ClassVar[str] = "config.queues.schedules.updated"

    def __init__(
        self,
        queue_id: int,
        schedule_id: int,
        **data,
    ):
        content = {
            "queue_id": queue_id,
            "schedule_id": schedule_id,
        }
        super().__init__(content=content, **data)


class QueueScheduleDissociatedEvent(QueueScheduleEvent):
    """Event for when a schedule is dissociated from a queue."""

    name: ClassVar[str] = "queue_schedule_dissociated"
    routing_key_fmt: ClassVar[str] = "config.queues.schedules.deleted"

    def __init__(
        self,
        queue_id: int,
        schedule_id: int,
        **data,
    ):
        content = {
            "queue_id": queue_id,
            "schedule_id": schedule_id,
        }
        super().__init__(content=content, **data)
