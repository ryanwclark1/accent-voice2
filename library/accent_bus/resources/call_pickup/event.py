# Copyright 2023 Accent Communications

from ..common.event import TenantEvent
from ..common.types import UUIDStr


class CallPickupCreatedEvent(TenantEvent):
    service = 'confd'
    name = 'call_pickup_created'
    routing_key_fmt = 'config.callpickup.created'

    def __init__(self, call_pickup_id: int, tenant_uuid: UUIDStr):
        content = {'id': call_pickup_id}
        super().__init__(content, tenant_uuid)


class CallPickupDeletedEvent(TenantEvent):
    service = 'confd'
    name = 'call_pickup_deleted'
    routing_key_fmt = 'config.callpickup.deleted'

    def __init__(self, call_pickup_id: int, tenant_uuid: UUIDStr):
        content = {'id': call_pickup_id}
        super().__init__(content, tenant_uuid)


class CallPickupEditedEvent(TenantEvent):
    service = 'confd'
    name = 'call_pickup_edited'
    routing_key_fmt = 'config.callpickup.edited'

    def __init__(self, call_pickup_id: int, tenant_uuid: UUIDStr):
        content = {'id': call_pickup_id}
        super().__init__(content, tenant_uuid)
