# Copyright 2023 Accent Communications

from ..common.event import TenantEvent
from ..common.types import UUIDStr


class LineExtensionAssociatedEvent(TenantEvent):
    service = 'confd'
    name = 'line_extension_associated'
    routing_key_fmt = 'config.line_extension_associated.updated'

    def __init__(
        self,
        line_id: int,
        extension_id: int,
        tenant_uuid: UUIDStr,
    ):
        content = {'line_id': line_id, 'extension_id': extension_id}
        super().__init__(content, tenant_uuid)


class LineExtensionDissociatedEvent(TenantEvent):
    service = 'confd'
    name = 'line_extension_dissociated'
    routing_key_fmt = 'config.line_extension_associated.deleted'

    def __init__(
        self,
        line_id: int,
        extension_id: int,
        tenant_uuid: UUIDStr,
    ):
        content = {'line_id': line_id, 'extension_id': extension_id}
        super().__init__(content, tenant_uuid)
