# Copyright 2023 Accent Communications

from ..common.event import TenantEvent
from ..common.types import UUIDStr


class IncallCreatedEvent(TenantEvent):
    service = 'confd'
    name = 'incall_created'
    routing_key_fmt = 'config.incalls.created'

    def __init__(self, incall_id: int, tenant_uuid: UUIDStr):
        content = {'id': incall_id}
        super().__init__(content, tenant_uuid)


class IncallDeletedEvent(TenantEvent):
    service = 'confd'
    name = 'incall_deleted'
    routing_key_fmt = 'config.incalls.deleted'

    def __init__(self, incall_id: int, tenant_uuid: UUIDStr):
        content = {'id': incall_id}
        super().__init__(content, tenant_uuid)


class IncallEditedEvent(TenantEvent):
    service = 'confd'
    name = 'incall_edited'
    routing_key_fmt = 'config.incalls.edited'

    def __init__(self, incall_id: int, tenant_uuid: UUIDStr):
        content = {'id': incall_id}
        super().__init__(content, tenant_uuid)
