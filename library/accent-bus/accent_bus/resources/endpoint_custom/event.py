# resources/endpoint_custom/event.py
from typing import ClassVar

from resources.common.event import TenantEvent

from .types import EndpointCustomDict


class CustomEndpointEvent(TenantEvent):
    """Base class for Custom Endpoint events."""

    service: ClassVar[str] = "confd"
    content: dict


class CustomEndpointCreatedEvent(CustomEndpointEvent):
    """Event for when a custom endpoint is created."""

    name: ClassVar[str] = "custom_endpoint_created"
    routing_key_fmt: ClassVar[str] = "config.custom_endpoint.created"

    def __init__(self, endpoint: EndpointCustomDict, **data):
        super().__init__(content=endpoint, **data)


class CustomEndpointDeletedEvent(CustomEndpointEvent):
    """Event for when a custom endpoint is deleted."""

    name: ClassVar[str] = "custom_endpoint_deleted"
    routing_key_fmt: ClassVar[str] = "config.custom_endpoint.deleted"

    def __init__(self, endpoint: EndpointCustomDict, **data):
        super().__init__(content=endpoint, **data)


class CustomEndpointEditedEvent(CustomEndpointEvent):
    """Event for when a custom endpoint is edited."""

    name: ClassVar[str] = "custom_endpoint_edited"
    routing_key_fmt: ClassVar[str] = "config.custom_endpoint.edited"

    def __init__(self, endpoint: EndpointCustomDict, **data):
        super().__init__(content=endpoint, **data)
