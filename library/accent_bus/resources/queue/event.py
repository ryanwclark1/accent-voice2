# Copyright 2023 Accent Communications

from ..common.event import TenantEvent
from ..common.types import UUIDStr


class QueueCreatedEvent(TenantEvent):
    service = 'confd'
    name = 'queue_created'
    routing_key_fmt = 'config.queues.created'

    def __init__(self, queue_id: int, tenant_uuid: UUIDStr):
        content = {'id': int(queue_id)}
        super().__init__(content, tenant_uuid)


class QueueDeletedEvent(TenantEvent):
    service = 'confd'
    name = 'queue_deleted'
    routing_key_fmt = 'config.queues.deleted'

    def __init__(self, queue_id: int, tenant_uuid: UUIDStr):
        content = {'id': int(queue_id)}
        super().__init__(content, tenant_uuid)


class QueueEditedEvent(TenantEvent):
    service = 'confd'
    name = 'queue_edited'
    routing_key_fmt = 'config.queues.edited'

    def __init__(self, queue_id: int, tenant_uuid: UUIDStr):
        content = {'id': int(queue_id)}
        super().__init__(content, tenant_uuid)


class QueueFallbackEditedEvent(TenantEvent):
    service = 'confd'
    name = 'queue_fallback_edited'
    routing_key_fmt = 'config.queues.fallbacks.edited'

    def __init__(self, queue_id: int, tenant_uuid: UUIDStr):
        content = {'id': int(queue_id)}
        super().__init__(content, tenant_uuid)
