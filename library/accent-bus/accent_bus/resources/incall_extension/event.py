# Copyright 2023 Accent Communications

from ..common.event import TenantEvent
from ..common.types import UUIDStr


class IncallExtensionAssociatedEvent(TenantEvent):
    service = 'confd'
    name = 'incall_extension_associated'
    routing_key_fmt = 'config.incalls.extensions.updated'

    def __init__(
        self,
        incall_id: int,
        extension_id: int,
        tenant_uuid: UUIDStr,
    ):
        content = {
            'incall_id': incall_id,
            'extension_id': extension_id,
        }
        super().__init__(content, tenant_uuid)


class IncallExtensionDissociatedEvent(TenantEvent):
    service = 'confd'
    name = 'incall_extension_dissociated'
    routing_key_fmt = 'config.incalls.extensions.deleted'

    def __init__(
        self,
        incall_id: int,
        extension_id: int,
        tenant_uuid: UUIDStr,
    ):
        content = {
            'incall_id': incall_id,
            'extension_id': extension_id,
        }
        super().__init__(content, tenant_uuid)
