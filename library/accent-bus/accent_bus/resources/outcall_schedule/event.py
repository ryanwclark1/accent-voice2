# resources/outcall_schedule/event.py
from typing import ClassVar

from accent_bus.resources.common.event import TenantEvent


class OutcallScheduleEvent(TenantEvent):
    """Base class for Outcall Schedule events."""

    service: ClassVar[str] = "confd"
    content: dict


class OutcallScheduleAssociatedEvent(OutcallScheduleEvent):
    """Event for when a schedule is associated with an outcall."""

    name: ClassVar[str] = "outcall_schedule_associated"
    routing_key_fmt: ClassVar[str] = "config.outcalls.schedules.updated"

    def __init__(
        self,
        outcall_id: int,
        schedule_id: int,
        **data,
    ):
        content = {
            "outcall_id": outcall_id,
            "schedule_id": schedule_id,
        }
        super().__init__(content=content, **data)


class OutcallScheduleDissociatedEvent(OutcallScheduleEvent):
    """Event for when a schedule is dissociated from an outcall."""

    name: ClassVar[str] = "outcall_schedule_dissociated"
    routing_key_fmt: ClassVar[str] = "config.outcalls.schedules.deleted"

    def __init__(
        self,
        outcall_id: int,
        schedule_id: int,
        **data,
    ):
        content = {
            "outcall_id": outcall_id,
            "schedule_id": schedule_id,
        }
        super().__init__(content=content, **data)
