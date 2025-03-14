# Copyright 2023 Accent Communications

from ..common.event import TenantEvent
from ..common.types import UUIDStr


class FuncKeyTemplateCreatedEvent(TenantEvent):
    service = 'confd'
    name = 'func_key_template_created'
    routing_key_fmt = 'config.funckey.template.created'

    def __init__(self, template_id: int, tenant_uuid: UUIDStr):
        content = {'id': template_id}
        super().__init__(content, tenant_uuid)


class FuncKeyTemplateDeletedEvent(TenantEvent):
    service = 'confd'
    name = 'func_key_template_deleted'
    routing_key_fmt = 'config.funckey.template.deleted'

    def __init__(self, template_id: int, tenant_uuid: UUIDStr):
        content = {'id': template_id}
        super().__init__(content, tenant_uuid)


class FuncKeyTemplateEditedEvent(TenantEvent):
    service = 'confd'
    name = 'func_key_template_edited'
    routing_key_fmt = 'config.funckey.template.edited'

    def __init__(self, template_id: int, tenant_uuid: UUIDStr):
        content = {'id': template_id}
        super().__init__(content, tenant_uuid)
