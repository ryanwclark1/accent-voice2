# resources/endpoint_iax/event.py
from typing import ClassVar

from accent_bus.resources.common.event import TenantEvent

from .types import EndpointIAXDict


class IAXEndpointEvent(TenantEvent):
    """Base class for IAX Endpoint events."""

    service: ClassVar[str] = "confd"
    content: dict


class IAXEndpointCreatedEvent(IAXEndpointEvent):
    """Event for when an IAX endpoint is created."""

    name: ClassVar[str] = "iax_endpoint_created"
    routing_key_fmt: ClassVar[str] = "config.iax_endpoint.created"

    def __init__(self, endpoint: EndpointIAXDict, **data):
        super().__init__(content=endpoint, **data)


class IAXEndpointDeletedEvent(IAXEndpointEvent):
    """Event for when an IAX endpoint is deleted."""

    name: ClassVar[str] = "iax_endpoint_deleted"
    routing_key_fmt: ClassVar[str] = "config.iax_endpoint.deleted"

    def __init__(self, endpoint: EndpointIAXDict, **data):
        super().__init__(content=endpoint, **data)


class IAXEndpointEditedEvent(IAXEndpointEvent):
    """Event for when an IAX endpoint is edited."""

    name: ClassVar[str] = "iax_endpoint_edited"
    routing_key_fmt: ClassVar[str] = "config.iax_endpoint.edited"

    def __init__(self, endpoint: EndpointIAXDict, **data):
        super().__init__(content=endpoint, **data)
