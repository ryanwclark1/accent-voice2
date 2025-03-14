# Copyright 2023 Accent Communications

from ..common.event import TenantEvent
from ..common.types import UUIDStr


class GroupExtensionAssociatedEvent(TenantEvent):
    service = 'confd'
    name = 'group_extension_associated'
    routing_key_fmt = 'config.groups.extensions.updated'

    def __init__(
        self,
        group_id: int,
        group_uuid: UUIDStr,
        extension_id: int,
        tenant_uuid: UUIDStr,
    ):
        content = {
            'group_id': group_id,
            'group_uuid': str(group_uuid),
            'extension_id': extension_id,
        }
        super().__init__(content, tenant_uuid)


class GroupExtensionDissociatedEvent(TenantEvent):
    service = 'confd'
    name = 'group_extension_dissociated'
    routing_key_fmt = 'config.groups.extensions.deleted'

    def __init__(
        self,
        group_id: int,
        group_uuid: UUIDStr,
        extension_id: int,
        tenant_uuid: UUIDStr,
    ):
        content = {
            'group_id': group_id,
            'group_uuid': str(group_uuid),
            'extension_id': extension_id,
        }
        super().__init__(content, tenant_uuid)
