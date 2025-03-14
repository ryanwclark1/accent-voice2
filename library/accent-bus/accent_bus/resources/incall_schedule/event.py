# resources/incall_schedule/event.py
from typing import ClassVar

from resources.common.event import TenantEvent


class IncallScheduleEvent(TenantEvent):
    """Base class for Incall Schedule events."""

    service: ClassVar[str] = "confd"
    content: dict


class IncallScheduleAssociatedEvent(IncallScheduleEvent):
    """Event for when a schedule is associated with an incall."""

    name: ClassVar[str] = "incall_schedule_associated"
    routing_key_fmt: ClassVar[str] = "config.incalls.schedules.updated"

    def __init__(self, incall_id: int, schedule_id: int, **data):
        content = {
            "incall_id": incall_id,
            "schedule_id": schedule_id,
        }
        super().__init__(content=content, **data)


class IncallScheduleDissociatedEvent(IncallScheduleEvent):
    """Event for when a schedule is dissociated from an incall."""

    name: ClassVar[str] = "incall_schedule_dissociated"
    routing_key_fmt: ClassVar[str] = "config.incalls.schedules.deleted"

    def __init__(self, incall_id: int, schedule_id: int, **data):
        content = {
            "incall_id": incall_id,
            "schedule_id": schedule_id,
        }
        super().__init__(content=content, **data)
