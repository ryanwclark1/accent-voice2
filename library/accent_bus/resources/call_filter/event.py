# Copyright 2023 Accent Communications

from ..common.event import TenantEvent
from ..common.types import UUIDStr


class CallFilterCreatedEvent(TenantEvent):
    service = 'confd'
    name = 'call_filter_created'
    routing_key_fmt = 'config.callfilter.created'

    def __init__(self, call_filter_id: int, tenant_uuid: UUIDStr):
        content = {'id': call_filter_id}
        super().__init__(content, tenant_uuid)


class CallFilterDeletedEvent(TenantEvent):
    service = 'confd'
    name = 'call_filter_deleted'
    routing_key_fmt = 'config.callfilter.deleted'

    def __init__(self, call_filter_id: int, tenant_uuid: UUIDStr):
        content = {'id': call_filter_id}
        super().__init__(content, tenant_uuid)


class CallFilterEditedEvent(TenantEvent):
    service = 'confd'
    name = 'call_filter_edited'
    routing_key_fmt = 'config.callfilter.edited'

    def __init__(self, call_filter_id: int, tenant_uuid: UUIDStr):
        content = {'id': call_filter_id}
        super().__init__(content, tenant_uuid)


class CallFilterFallbackEditedEvent(TenantEvent):
    service = 'confd'
    name = 'call_filter_fallback_edited'
    routing_key_fmt = 'config.callfilters.fallbacks.edited'

    def __init__(self, call_filter_id: int, tenant_uuid: UUIDStr):
        content = {'id': call_filter_id}
        super().__init__(content, tenant_uuid)
