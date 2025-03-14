# resources/schedule/event.py
from typing import ClassVar

from resources.common.event import TenantEvent


class ScheduleEvent(TenantEvent):
    """Base class for Schedule events."""

    service: ClassVar[str] = "confd"
    content: dict


class ScheduleCreatedEvent(ScheduleEvent):
    """Event for when a schedule is created."""

    name: ClassVar[str] = "schedule_created"
    routing_key_fmt: ClassVar[str] = "config.schedules.created"

    def __init__(self, schedule_id: int, **data):
        content = {"id": int(schedule_id)}
        super().__init__(content=content, **data)


class ScheduleDeletedEvent(ScheduleEvent):
    """Event for when a schedule is deleted."""

    name: ClassVar[str] = "schedule_deleted"
    routing_key_fmt: ClassVar[str] = "config.schedules.deleted"

    def __init__(self, schedule_id: int, **data):
        content = {"id": int(schedule_id)}
        super().__init__(content=content, **data)


class ScheduleEditedEvent(ScheduleEvent):
    """Event for when a schedule is edited."""

    name: ClassVar[str] = "schedule_edited"
    routing_key_fmt: ClassVar[str] = "config.schedules.edited"

    def __init__(self, schedule_id: int, **data):
        content = {"id": int(schedule_id)}
        super().__init__(content=content, **data)
