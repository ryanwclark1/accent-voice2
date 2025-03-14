# Copyright 2023 Accent Communications

from ..common.event import TenantEvent
from ..common.types import UUIDStr
from .types import EndpointSCCPDict


class SCCPEndpointCreatedEvent(TenantEvent):
    service = 'confd'
    name = 'sccp_endpoint_created'
    routing_key_fmt = 'config.sccp_endpoint.created'

    def __init__(
        self,
        endpoint: EndpointSCCPDict,
        tenant_uuid: UUIDStr,
    ):
        super().__init__(endpoint, tenant_uuid)


class SCCPEndpointDeletedEvent(TenantEvent):
    service = 'confd'
    name = 'sccp_endpoint_deleted'
    routing_key_fmt = 'config.sccp_endpoint.deleted'

    def __init__(
        self,
        endpoint: EndpointSCCPDict,
        tenant_uuid: UUIDStr,
    ):
        super().__init__(endpoint, tenant_uuid)


class SCCPEndpointEditedEvent(TenantEvent):
    service = 'confd'
    name = 'sccp_endpoint_edited'
    routing_key_fmt = 'config.sccp_endpoint.edited'

    def __init__(
        self,
        endpoint: EndpointSCCPDict,
        tenant_uuid: UUIDStr,
    ):
        super().__init__(endpoint, tenant_uuid)
