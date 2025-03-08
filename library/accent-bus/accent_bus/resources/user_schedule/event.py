# Copyright 2023 Accent Communications

from ..common.event import UserEvent
from ..common.types import UUIDStr


class UserScheduleAssociatedEvent(UserEvent):
    service = 'confd'
    name = 'user_schedule_associated'
    routing_key_fmt = 'config.users.schedules.updated'

    def __init__(
        self,
        schedule_id: int,
        tenant_uuid: UUIDStr,
        user_uuid: UUIDStr,
    ):
        content = {
            'user_uuid': str(user_uuid),
            'schedule_id': schedule_id,
        }
        super().__init__(content, tenant_uuid, user_uuid)


class UserScheduleDissociatedEvent(UserEvent):
    service = 'confd'
    name = 'user_schedule_dissociated'
    routing_key_fmt = 'config.users.schedules.deleted'

    def __init__(
        self,
        schedule_id: int,
        tenant_uuid: UUIDStr,
        user_uuid: UUIDStr,
    ):
        content = {
            'user_uuid': str(user_uuid),
            'schedule_id': schedule_id,
        }
        super().__init__(content, tenant_uuid, user_uuid)
