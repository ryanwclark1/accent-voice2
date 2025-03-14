# Copyright 2023 Accent Communications

from ..common.event import TenantEvent
from ..common.types import UUIDStr


class IVRCreatedEvent(TenantEvent):
    service = 'confd'
    name = 'ivr_created'
    routing_key_fmt = 'config.ivr.created'

    def __init__(self, ivr_id: int, tenant_uuid: UUIDStr):
        content = {'id': ivr_id}
        super().__init__(content, tenant_uuid)


class IVRDeletedEvent(TenantEvent):
    service = 'confd'
    name = 'ivr_deleted'
    routing_key_fmt = 'config.ivr.deleted'

    def __init__(self, ivr_id: int, tenant_uuid: UUIDStr):
        content = {'id': ivr_id}
        super().__init__(content, tenant_uuid)


class IVREditedEvent(TenantEvent):
    service = 'confd'
    name = 'ivr_edited'
    routing_key_fmt = 'config.ivr.edited'

    def __init__(self, ivr_id: int, tenant_uuid: UUIDStr):
        content = {'id': ivr_id}
        super().__init__(content, tenant_uuid)
