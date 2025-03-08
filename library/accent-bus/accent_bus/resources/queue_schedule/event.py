# Copyright 2023 Accent Communications

from ..common.event import TenantEvent
from ..common.types import UUIDStr


class QueueScheduleAssociatedEvent(TenantEvent):
    service = 'confd'
    name = 'queue_schedule_associated'
    routing_key_fmt = 'config.queues.schedules.updated'

    def __init__(
        self,
        queue_id: int,
        schedule_id: int,
        tenant_uuid: UUIDStr,
    ):
        content = {
            'queue_id': queue_id,
            'schedule_id': schedule_id,
        }
        super().__init__(content, tenant_uuid)


class QueueScheduleDissociatedEvent(TenantEvent):
    service = 'confd'
    name = 'queue_schedule_dissociated'
    routing_key_fmt = 'config.queues.schedules.deleted'

    def __init__(
        self,
        queue_id: int,
        schedule_id: int,
        tenant_uuid: UUIDStr,
    ):
        content = {
            'queue_id': queue_id,
            'schedule_id': schedule_id,
        }
        super().__init__(content, tenant_uuid)
