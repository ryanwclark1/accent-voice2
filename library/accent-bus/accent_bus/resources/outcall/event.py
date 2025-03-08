# Copyright 2023 Accent Communications

from ..common.event import TenantEvent
from ..common.types import UUIDStr


class OutcallCreatedEvent(TenantEvent):
    service = 'confd'
    name = 'outcall_created'
    routing_key_fmt = 'config.outcalls.created'

    def __init__(self, outcall_id: int, tenant_uuid: UUIDStr):
        content = {'id': outcall_id}
        super().__init__(content, tenant_uuid)


class OutcallDeletedEvent(TenantEvent):
    service = 'confd'
    name = 'outcall_deleted'
    routing_key_fmt = 'config.outcalls.deleted'

    def __init__(self, outcall_id: int, tenant_uuid: UUIDStr):
        content = {'id': outcall_id}
        super().__init__(content, tenant_uuid)


class OutcallEditedEvent(TenantEvent):
    service = 'confd'
    name = 'outcall_edited'
    routing_key_fmt = 'config.outcalls.edited'

    def __init__(self, outcall_id: int, tenant_uuid: UUIDStr):
        content = {'id': outcall_id}
        super().__init__(content, tenant_uuid)
