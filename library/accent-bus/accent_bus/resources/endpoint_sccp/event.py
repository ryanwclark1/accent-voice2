# resources/endpoint_sccp/event.py
from typing import ClassVar

from accent_bus.resources.common.event import TenantEvent

from .types import EndpointSCCPDict


class SCCPEndpointEvent(TenantEvent):
    """Base class for SCCP Endpoint events."""

    service: ClassVar[str] = "confd"
    content: dict


class SCCPEndpointCreatedEvent(SCCPEndpointEvent):
    """Event for when an SCCP endpoint is created."""

    name: ClassVar[str] = "sccp_endpoint_created"
    routing_key_fmt: ClassVar[str] = "config.sccp_endpoint.created"

    def __init__(self, endpoint: EndpointSCCPDict, **data):
        super().__init__(content=endpoint, **data)


class SCCPEndpointDeletedEvent(SCCPEndpointEvent):
    """Event for when an SCCP endpoint is deleted."""

    name: ClassVar[str] = "sccp_endpoint_deleted"
    routing_key_fmt: ClassVar[str] = "config.sccp_endpoint.deleted"

    def __init__(self, endpoint: EndpointSCCPDict, **data):
        super().__init__(content=endpoint, **data)


class SCCPEndpointEditedEvent(SCCPEndpointEvent):
    """Event for when an SCCP endpoint is edited."""

    name: ClassVar[str] = "sccp_endpoint_edited"
    routing_key_fmt: ClassVar[str] = "config.sccp_endpoint.edited"

    def __init__(self, endpoint: EndpointSCCPDict, **data):
        super().__init__(content=endpoint, **data)
