# resources/endpoint_sip/event.py
from typing import ClassVar

from accent_bus.resources.common.event import TenantEvent

from .types import EndpointSIPDict


class SIPEndpointEvent(TenantEvent):
    """Base class for SIP Endpoint events."""

    service: ClassVar[str] = "confd"
    content: dict


class SIPEndpointCreatedEvent(SIPEndpointEvent):
    """Event for when a SIP endpoint is created."""

    name: ClassVar[str] = "sip_endpoint_created"
    routing_key_fmt: ClassVar[str] = "config.sip_endpoint.created"

    def __init__(self, endpoint: EndpointSIPDict, **data):
        super().__init__(content=endpoint, **data)


class SIPEndpointDeletedEvent(SIPEndpointEvent):
    """Event for when a SIP endpoint is deleted."""

    name: ClassVar[str] = "sip_endpoint_deleted"
    routing_key_fmt: ClassVar[str] = "config.sip_endpoint.deleted"

    def __init__(self, endpoint: EndpointSIPDict, **data):
        super().__init__(content=endpoint, **data)


class SIPEndpointEditedEvent(SIPEndpointEvent):
    """Event for when a SIP endpoint is edited."""

    name: ClassVar[str] = "sip_endpoint_edited"
    routing_key_fmt: ClassVar[str] = "config.sip_endpoint.edited"

    def __init__(self, endpoint: EndpointSIPDict, **data):
        super().__init__(content=endpoint, **data)


class SIPEndpointTemplateCreatedEvent(SIPEndpointEvent):
    """Event for when a SIP endpoint template is created."""

    name: ClassVar[str] = "sip_endpoint_template_created"
    routing_key_fmt: ClassVar[str] = "config.sip_endpoint_template.created"

    def __init__(self, endpoint: EndpointSIPDict, **data):
        super().__init__(content=endpoint, **data)


class SIPEndpointTemplateDeletedEvent(SIPEndpointEvent):
    """Event for when a SIP endpoint template is deleted."""

    name: ClassVar[str] = "sip_endpoint_template_deleted"
    routing_key_fmt: ClassVar[str] = "config.sip_endpoint_template.deleted"

    def __init__(self, endpoint: EndpointSIPDict, **data):
        super().__init__(content=endpoint, **data)


class SIPEndpointTemplateEditedEvent(SIPEndpointEvent):
    """Event for when a SIP endpoint template is edited."""

    name: ClassVar[str] = "sip_endpoint_template_edited"
    routing_key_fmt: ClassVar[str] = "config.sip_endpoint_template.edited"

    def __init__(self, endpoint: EndpointSIPDict, **data):
        super().__init__(content=endpoint, **data)
