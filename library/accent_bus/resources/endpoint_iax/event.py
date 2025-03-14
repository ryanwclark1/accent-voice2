# Copyright 2023 Accent Communications

from ..common.event import TenantEvent
from ..common.types import UUIDStr
from .types import EndpointIAXDict


class IAXEndpointCreatedEvent(TenantEvent):
    service = 'confd'
    name = 'iax_endpoint_created'
    routing_key_fmt = 'config.iax_endpoint.created'

    def __init__(self, endpoint: EndpointIAXDict, tenant_uuid: UUIDStr):
        super().__init__(endpoint, tenant_uuid)


class IAXEndpointDeletedEvent(TenantEvent):
    service = 'confd'
    name = 'iax_endpoint_deleted'
    routing_key_fmt = 'config.iax_endpoint.deleted'

    def __init__(self, endpoint: EndpointIAXDict, tenant_uuid: UUIDStr):
        super().__init__(endpoint, tenant_uuid)


class IAXEndpointEditedEvent(TenantEvent):
    service = 'confd'
    name = 'iax_endpoint_edited'
    routing_key_fmt = 'config.iax_endpoint.edited'

    def __init__(self, endpoint: EndpointIAXDict, tenant_uuid: UUIDStr):
        super().__init__(endpoint, tenant_uuid)
