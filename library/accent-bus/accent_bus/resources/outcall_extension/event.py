# Copyright 2023 Accent Communications

from ..common.event import TenantEvent
from ..common.types import UUIDStr


class OutcallExtensionAssociatedEvent(TenantEvent):
    service = 'confd'
    name = 'outcall_extension_associated'
    routing_key_fmt = 'config.outcalls.extensions.updated'

    def __init__(
        self,
        outcall_id: int,
        extension_id: int,
        tenant_uuid: UUIDStr,
    ):
        content = {
            'outcall_id': outcall_id,
            'extension_id': extension_id,
        }
        super().__init__(content, tenant_uuid)


class OutcallExtensionDissociatedEvent(TenantEvent):
    service = 'confd'
    name = 'outcall_extension_dissociated'
    routing_key_fmt = 'config.outcalls.extensions.deleted'

    def __init__(
        self,
        outcall_id: int,
        extension_id: int,
        tenant_uuid: UUIDStr,
    ):
        content = {
            'outcall_id': outcall_id,
            'extension_id': extension_id,
        }
        super().__init__(content, tenant_uuid)
