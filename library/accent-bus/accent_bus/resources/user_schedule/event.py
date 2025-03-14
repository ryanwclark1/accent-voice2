# accent_bus/resources/user_schedule/event.py
# Copyright 2025 Accent Communications

"""User schedule events."""

from accent_bus.resources.common.event import UserEvent
from accent_bus.resources.common.types import UUIDStr


class UserScheduleAssociatedEvent(UserEvent):
    """Event for when a user schedule is associated."""

    service = "confd"
    name = "user_schedule_associated"
    routing_key_fmt = "config.users.schedules.updated"

    def __init__(
        self,
        schedule_id: int,
        tenant_uuid: UUIDStr,
        user_uuid: UUIDStr,
    ) -> None:
        """Initialize Event.

        Args:
           schedule_id: Schedule ID
           tenant_uuid: tenant UUID
           user_uuid: user UUID

        """
        content = {
            "user_uuid": str(user_uuid),
            "schedule_id": schedule_id,
        }
        super().__init__(content, tenant_uuid, user_uuid)


class UserScheduleDissociatedEvent(UserEvent):
    """Event for when a user schedule is dissociated."""

    service = "confd"
    name = "user_schedule_dissociated"
    routing_key_fmt = "config.users.schedules.deleted"

    def __init__(
        self,
        schedule_id: int,
        tenant_uuid: UUIDStr,
        user_uuid: UUIDStr,
    ) -> None:
        """Initialize Event.

        Args:
            schedule_id (int): The ID of the schedule.
            tenant_uuid (UUIDStr):  tenant UUID.
            user_uuid (UUIDStr): user UUID.

        """
        content = {
            "user_uuid": str(user_uuid),
            "schedule_id": schedule_id,
        }
        super().__init__(content, tenant_uuid, user_uuid)
