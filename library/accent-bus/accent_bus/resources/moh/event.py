# Copyright 2023 Accent Communications

from ..common.event import TenantEvent
from ..common.types import UUIDStr
from .types import MOHDict


class MOHCreatedEvent(TenantEvent):
    service = 'confd'
    name = 'moh_created'
    routing_key_fmt = 'config.moh.created'

    def __init__(self, moh: MOHDict, tenant_uuid: UUIDStr):
        super().__init__(moh, tenant_uuid)


class MOHDeletedEvent(TenantEvent):
    service = 'confd'
    name = 'moh_deleted'
    routing_key_fmt = 'config.moh.deleted'

    def __init__(self, moh: MOHDict, tenant_uuid: UUIDStr):
        super().__init__(moh, tenant_uuid)


class MOHEditedEvent(TenantEvent):
    service = 'confd'
    name = 'moh_edited'
    routing_key_fmt = 'config.moh.edited'

    def __init__(self, moh: MOHDict, tenant_uuid: UUIDStr):
        super().__init__(moh, tenant_uuid)
