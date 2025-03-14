# Copyright 2023 Accent Communications

from ..common.event import TenantEvent
from ..common.types import UUIDStr


class TrunkCreatedEvent(TenantEvent):
    service = 'confd'
    name = 'trunk_created'
    routing_key_fmt = 'config.trunk.created'

    def __init__(self, trunk_id: int, tenant_uuid: UUIDStr):
        content = {'id': int(trunk_id)}
        super().__init__(content, tenant_uuid)


class TrunkDeletedEvent(TenantEvent):
    service = 'confd'
    name = 'trunk_deleted'
    routing_key_fmt = 'config.trunk.deleted'

    def __init__(self, trunk_id: int, tenant_uuid: UUIDStr):
        content = {'id': int(trunk_id)}
        super().__init__(content, tenant_uuid)


class TrunkEditedEvent(TenantEvent):
    service = 'confd'
    name = 'trunk_edited'
    routing_key_fmt = 'config.trunk.edited'

    def __init__(self, trunk_id: int, tenant_uuid: UUIDStr):
        content = {'id': int(trunk_id)}
        super().__init__(content, tenant_uuid)


class TrunkStatusUpdatedEvent(TenantEvent):
    service = 'calld'
    name = 'trunk_status_updated'
    routing_key_fmt = 'trunks.{id}.status.updated'

    def __init__(
        self,
        trunk_id: int,
        technology: str,
        endpoint_name: str,
        endpoint_registered: bool,
        endpoint_current_call_count: int,
        tenant_uuid: UUIDStr,
    ):
        content = {
            'id': trunk_id,
            'technology': technology,
            'name': endpoint_name,
            'registered': endpoint_registered,
            'current_call_count': endpoint_current_call_count,
        }
        super().__init__(content, tenant_uuid)
