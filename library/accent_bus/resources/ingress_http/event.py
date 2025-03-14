# Copyright 2023 Accent Communications

from ..common.event import TenantEvent
from ..common.types import UUIDStr
from .types import IngressHTTPDict


class IngressHTTPCreatedEvent(TenantEvent):
    service = 'confd'
    name = 'ingress_http_created'
    routing_key_fmt = 'config.ingresses.http.created'

    def __init__(
        self,
        ingress_http: IngressHTTPDict,
        tenant_uuid: UUIDStr,
    ):
        super().__init__(ingress_http, tenant_uuid)


class IngressHTTPDeletedEvent(TenantEvent):
    service = 'confd'
    name = 'ingress_http_deleted'
    routing_key_fmt = 'config.ingresses.http.deleted'

    def __init__(
        self,
        ingress_http: IngressHTTPDict,
        tenant_uuid: UUIDStr,
    ):
        super().__init__(ingress_http, tenant_uuid)


class IngressHTTPEditedEvent(TenantEvent):
    service = 'confd'
    name = 'ingress_http_edited'
    routing_key_fmt = 'config.ingresses.http.edited'

    def __init__(
        self,
        ingress_http: IngressHTTPDict,
        tenant_uuid: UUIDStr,
    ):
        super().__init__(ingress_http, tenant_uuid)
