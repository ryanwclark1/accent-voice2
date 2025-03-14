# accent_bus/resources/endpoint_sip/event.py
# Copyright 2025 Accent Communications

"""SIP endpoint events."""

from accent_bus.resources.common.event import TenantEvent
from accent_bus.resources.common.types import UUIDStr

from .types import EndpointSIPDict


class SIPEndpointCreatedEvent(TenantEvent):
    """Event for when a SIP endpoint is created."""

    service = "confd"
    name = "sip_endpoint_created"
    routing_key_fmt = "config.sip_endpoint.created"

    def __init__(self, endpoint: EndpointSIPDict, tenant_uuid: UUIDStr):
        """Initialize event.

        Args:
          endpoint: Endpoint
          tenant_uuid: tenant UUID

        """
        super().__init__(endpoint, tenant_uuid)


class SIPEndpointDeletedEvent(TenantEvent):
    """Event for when a SIP endpoint is deleted."""

    service = "confd"
    name = "sip_endpoint_deleted"
    routing_key_fmt = "config.sip_endpoint.deleted"

    def __init__(self, endpoint: EndpointSIPDict, tenant_uuid: UUIDStr):
        """Initialize the event.

        Args:
            endpoint (EndpointSIPDict): sip endpoint.
            tenant_uuid (UUIDStr): tenant UUID.

        """
        super().__init__(endpoint, tenant_uuid)


class SIPEndpointEditedEvent(TenantEvent):
    """Event for when a SIP endpoint is edited."""

    service = "confd"
    name = "sip_endpoint_edited"
    routing_key_fmt = "config.sip_endpoint.edited"

    def __init__(self, endpoint: EndpointSIPDict, tenant_uuid: UUIDStr):
        """Initialize event.

        Args:
          endpoint: Endpoint
          tenant_uuid: tenant UUID

        """
        super().__init__(endpoint, tenant_uuid)


class SIPEndpointTemplateCreatedEvent(TenantEvent):
    """Event for creation of sip endpoint template."""

    service = "confd"
    name = "sip_endpoint_template_created"
    routing_key_fmt = "config.sip_endpoint_template.created"

    def __init__(self, endpoint: EndpointSIPDict, tenant_uuid: UUIDStr):
        """Initialize Event.

        Args:
            endpoint (EndpointSIPDict): sip endpoint.
            tenant_uuid (UUIDStr): tenant UUID

        """
        super().__init__(endpoint, tenant_uuid)


class SIPEndpointTemplateDeletedEvent(TenantEvent):
    """Event for deletion of sip endpoint template."""

    service = "confd"
    name = "sip_endpoint_template_deleted"
    routing_key_fmt = "config.sip_endpoint_template.deleted"

    def __init__(self, endpoint: EndpointSIPDict, tenant_uuid: UUIDStr):
        """Initialize event.

        Args:
            endpoint (EndpointSIPDict): sip endpoint.
            tenant_uuid (UUIDStr): tenant UUID.

        """
        super().__init__(endpoint, tenant_uuid)


class SIPEndpointTemplateEditedEvent(TenantEvent):
    """Event for when a SIP endpoint template is edited."""

    service = "confd"
    name = "sip_endpoint_template_edited"
    routing_key_fmt = "config.sip_endpoint_template.edited"

    def __init__(self, endpoint: EndpointSIPDict, tenant_uuid: UUIDStr):
        """Initialize Event.

        Args:
            endpoint (EndpointSIPDict):  SIP endpoint details.
            tenant_uuid (UUIDStr):  tenant UUID.

        """
        super().__init__(endpoint, tenant_uuid)
