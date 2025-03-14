# Copyright 2023 Accent Communications

from ..common.event import TenantEvent
from ..common.types import UUIDStr
from .types import ContextDict


class ContextCreatedEvent(TenantEvent):
    service = 'confd'
    name = 'context_created'
    routing_key_fmt = 'config.contexts.created'

    def __init__(self, context_data: ContextDict, tenant_uuid: UUIDStr):
        super().__init__(context_data, tenant_uuid)


class ContextDeletedEvent(TenantEvent):
    service = 'confd'
    name = 'context_deleted'
    routing_key_fmt = 'config.contexts.deleted'

    def __init__(self, context_data: ContextDict, tenant_uuid: UUIDStr):
        super().__init__(context_data, tenant_uuid)


class ContextEditedEvent(TenantEvent):
    service = 'confd'
    name = 'context_edited'
    routing_key_fmt = 'config.contexts.edited'

    def __init__(self, context_data: ContextDict, tenant_uuid: UUIDStr):
        super().__init__(context_data, tenant_uuid)
