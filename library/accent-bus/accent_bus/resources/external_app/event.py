# Copyright 2023 Accent Communications

from ..common.event import TenantEvent
from ..common.types import UUIDStr
from .types import ExternalAppDict


class ExternalAppCreatedEvent(TenantEvent):
    service = 'confd'
    name = 'external_app_created'
    routing_key_fmt = 'config.external_apps.created'

    def __init__(self, app: ExternalAppDict, tenant_uuid: UUIDStr):
        super().__init__(app, tenant_uuid)


class ExternalAppDeletedEvent(TenantEvent):
    service = 'confd'
    name = 'external_app_deleted'
    routing_key_fmt = 'config.external_apps.deleted'

    def __init__(self, app: ExternalAppDict, tenant_uuid: UUIDStr):
        super().__init__(app, tenant_uuid)


class ExternalAppEditedEvent(TenantEvent):
    service = 'confd'
    name = 'external_app_edited'
    routing_key_fmt = 'config.external_apps.edited'

    def __init__(self, app: ExternalAppDict, tenant_uuid: UUIDStr):
        super().__init__(app, tenant_uuid)
