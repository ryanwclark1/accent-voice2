# resources/user_schedule/event.py
from typing import ClassVar

from accent_bus.resources.common.event import UserEvent  # Correct import


class UserScheduleEvent(UserEvent):
    """Base class for User Schedule events."""

    service: ClassVar[str] = "confd"
    content: dict


class UserScheduleAssociatedEvent(UserScheduleEvent):
    """Event for when a schedule is associated with a user."""

    name: ClassVar[str] = "user_schedule_associated"
    routing_key_fmt: ClassVar[str] = "config.users.schedules.updated"

    def __init__(self, schedule_id: int, **data):
        content = {
            "user_uuid": str(data["user_uuid"]),
            "schedule_id": schedule_id,
        }
        super().__init__(content=content, **data)


class UserScheduleDissociatedEvent(UserScheduleEvent):
    """Event for when a schedule is dissociated from a user."""

    name: ClassVar[str] = "user_schedule_dissociated"
    routing_key_fmt: ClassVar[str] = "config.users.schedules.deleted"

    def __init__(self, schedule_id: int, **data):
        content = {
            "user_uuid": str(data["user_uuid"]),
            "schedule_id": schedule_id,
        }
        super().__init__(content=content, **data)
