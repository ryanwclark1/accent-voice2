# resources/group_schedule/event.py
from typing import ClassVar

from pydantic import UUID4

from resources.common.event import TenantEvent


class GroupScheduleEvent(TenantEvent):
    """Base class for Group Schedule events."""

    service: ClassVar[str] = "confd"
    content: dict


class GroupScheduleAssociatedEvent(GroupScheduleEvent):
    """Event for when a schedule is associated with a group."""

    name: ClassVar[str] = "group_schedule_associated"
    routing_key_fmt: ClassVar[str] = "config.groups.schedules.updated"

    def __init__(
        self,
        group_id: int,
        group_uuid: UUID4,
        schedule_id: int,
        **data,
    ):
        content = {
            "group_id": group_id,
            "group_uuid": str(group_uuid),
            "schedule_id": schedule_id,
        }
        super().__init__(content=content, **data)


class GroupScheduleDissociatedEvent(GroupScheduleEvent):
    """Event for when a schedule is dissociated from a group."""

    name: ClassVar[str] = "group_schedule_dissociated"
    routing_key_fmt: ClassVar[str] = "config.groups.schedules.deleted"

    def __init__(
        self,
        group_id: int,
        group_uuid: UUID4,
        schedule_id: int,
        **data,
    ):
        content = {
            "group_id": group_id,
            "group_uuid": str(group_uuid),
            "schedule_id": schedule_id,
        }
        super().__init__(content=content, **data)
