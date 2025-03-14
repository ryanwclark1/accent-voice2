# Copyright 2023 Accent Communications

from ..common.event import TenantEvent
from ..common.types import UUIDStr
from .types import GroupDict


class GroupCreatedEvent(TenantEvent):
    service = 'confd'
    name = 'group_created'
    routing_key_fmt = 'config.groups.created'

    def __init__(self, group: GroupDict, tenant_uuid: UUIDStr):
        super().__init__(group, tenant_uuid)


class GroupDeletedEvent(TenantEvent):
    service = 'confd'
    name = 'group_deleted'
    routing_key_fmt = 'config.groups.deleted'

    def __init__(self, group: GroupDict, tenant_uuid: UUIDStr):
        super().__init__(group, tenant_uuid)


class GroupEditedEvent(TenantEvent):
    service = 'confd'
    name = 'group_edited'
    routing_key_fmt = 'config.groups.edited'

    def __init__(self, group: GroupDict, tenant_uuid: UUIDStr):
        super().__init__(group, tenant_uuid)


class GroupFallbackEditedEvent(TenantEvent):
    service = 'confd'
    name = 'group_fallback_edited'
    routing_key_fmt = 'config.groups.fallbacks.edited'

    def __init__(
        self,
        group_id: int,
        group_uuid: UUIDStr,
        tenant_uuid: UUIDStr,
    ):
        content = {
            'id': group_id,
            'uuid': str(group_uuid),
        }
        super().__init__(content, tenant_uuid)
