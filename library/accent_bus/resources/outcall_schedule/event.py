# Copyright 2023 Accent Communications

from ..common.event import TenantEvent
from ..common.types import UUIDStr


class OutcallScheduleAssociatedEvent(TenantEvent):
    service = 'confd'
    name = 'outcall_schedule_associated'
    routing_key_fmt = 'config.outcalls.schedules.updated'

    def __init__(
        self,
        outcall_id: int,
        schedule_id: int,
        tenant_uuid: UUIDStr,
    ):
        content = {
            'outcall_id': outcall_id,
            'schedule_id': schedule_id,
        }
        super().__init__(content, tenant_uuid)


class OutcallScheduleDissociatedEvent(TenantEvent):
    service = 'confd'
    name = 'outcall_schedule_dissociated'
    routing_key_fmt = 'config.outcalls.schedules.deleted'

    def __init__(
        self,
        outcall_id: int,
        schedule_id: int,
        tenant_uuid: UUIDStr,
    ):
        content = {
            'outcall_id': outcall_id,
            'schedule_id': schedule_id,
        }
        super().__init__(content, tenant_uuid)
