# Copyright 2023 Accent Communications

from ..common.event import TenantEvent
from ..common.types import UUIDStr
from .types import EndpointSIPDict


class SIPEndpointCreatedEvent(TenantEvent):
    service = 'confd'
    name = 'sip_endpoint_created'
    routing_key_fmt = 'config.sip_endpoint.created'

    def __init__(self, endpoint: EndpointSIPDict, tenant_uuid: UUIDStr):
        super().__init__(endpoint, tenant_uuid)


class SIPEndpointDeletedEvent(TenantEvent):
    service = 'confd'
    name = 'sip_endpoint_deleted'
    routing_key_fmt = 'config.sip_endpoint.deleted'

    def __init__(self, endpoint: EndpointSIPDict, tenant_uuid: UUIDStr):
        super().__init__(endpoint, tenant_uuid)


class SIPEndpointEditedEvent(TenantEvent):
    service = 'confd'
    name = 'sip_endpoint_edited'
    routing_key_fmt = 'config.sip_endpoint.edited'

    def __init__(self, endpoint: EndpointSIPDict, tenant_uuid: UUIDStr):
        super().__init__(endpoint, tenant_uuid)


class SIPEndpointTemplateCreatedEvent(TenantEvent):
    service = 'confd'
    name = 'sip_endpoint_template_created'
    routing_key_fmt = 'config.sip_endpoint_template.created'

    def __init__(self, endpoint: EndpointSIPDict, tenant_uuid: UUIDStr):
        super().__init__(endpoint, tenant_uuid)


class SIPEndpointTemplateDeletedEvent(TenantEvent):
    service = 'confd'
    name = 'sip_endpoint_template_deleted'
    routing_key_fmt = 'config.sip_endpoint_template.deleted'

    def __init__(self, endpoint: EndpointSIPDict, tenant_uuid: UUIDStr):
        super().__init__(endpoint, tenant_uuid)


class SIPEndpointTemplateEditedEvent(TenantEvent):
    service = 'confd'
    name = 'sip_endpoint_template_edited'
    routing_key_fmt = 'config.sip_endpoint_template.edited'

    def __init__(self, endpoint: EndpointSIPDict, tenant_uuid: UUIDStr):
        super().__init__(endpoint, tenant_uuid)
