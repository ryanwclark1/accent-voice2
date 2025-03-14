# Copyright 2023 Accent Communications

from ..common.event import TenantEvent
from ..common.types import UUIDStr


class PagingCreatedEvent(TenantEvent):
    service = 'confd'
    name = 'paging_created'
    routing_key_fmt = 'config.pagings.created'

    def __init__(self, paging_id: int, tenant_uuid: UUIDStr):
        content = {'id': paging_id}
        super().__init__(content, tenant_uuid)


class PagingDeletedEvent(TenantEvent):
    service = 'confd'
    name = 'paging_deleted'
    routing_key_fmt = 'config.pagings.deleted'

    def __init__(self, paging_id: int, tenant_uuid: UUIDStr):
        content = {'id': paging_id}
        super().__init__(content, tenant_uuid)


class PagingEditedEvent(TenantEvent):
    service = 'confd'
    name = 'paging_edited'
    routing_key_fmt = 'config.pagings.edited'

    def __init__(self, paging_id: int, tenant_uuid: UUIDStr):
        content = {'id': paging_id}
        super().__init__(content, tenant_uuid)
