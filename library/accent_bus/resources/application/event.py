# Copyright 2023 Accent Communications

from ..common.event import TenantEvent
from ..common.types import UUIDStr
from .types import ApplicationDict


class ApplicationCreatedEvent(TenantEvent):
    service = 'confd'
    name = 'application_created'
    routing_key_fmt = 'config.applications.created'

    def __init__(
        self,
        application: ApplicationDict,
        tenant_uuid: UUIDStr,
    ):
        super().__init__(application, tenant_uuid)


class ApplicationDeletedEvent(TenantEvent):
    service = 'confd'
    name = 'application_deleted'
    routing_key_fmt = 'config.applications.deleted'

    def __init__(
        self,
        application: ApplicationDict,
        tenant_uuid: UUIDStr,
    ):
        super().__init__(application, tenant_uuid)


class ApplicationEditedEvent(TenantEvent):
    service = 'confd'
    name = 'application_edited'
    routing_key_fmt = 'config.applications.edited'

    def __init__(
        self,
        application: ApplicationDict,
        tenant_uuid: UUIDStr,
    ):
        super().__init__(application, tenant_uuid)
