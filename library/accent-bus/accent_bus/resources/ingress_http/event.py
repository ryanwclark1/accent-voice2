# resources/ingress_http/event.py
from typing import ClassVar

from accent_bus.resources.common.event import TenantEvent

from .types import IngressHTTPDict


class IngressHTTPEvent(TenantEvent):
    """Base class for Ingress HTTP events."""

    service: ClassVar[str] = "confd"
    content: dict


class IngressHTTPCreatedEvent(IngressHTTPEvent):
    """Event for when an Ingress HTTP configuration is created."""

    name: ClassVar[str] = "ingress_http_created"
    routing_key_fmt: ClassVar[str] = "config.ingresses.http.created"

    def __init__(self, ingress_http: IngressHTTPDict, **data):
        super().__init__(content=ingress_http, **data)


class IngressHTTPDeletedEvent(IngressHTTPEvent):
    """Event for when an Ingress HTTP configuration is deleted."""

    name: ClassVar[str] = "ingress_http_deleted"
    routing_key_fmt: ClassVar[str] = "config.ingresses.http.deleted"

    def __init__(self, ingress_http: IngressHTTPDict, **data):
        super().__init__(content=ingress_http, **data)


class IngressHTTPEditedEvent(IngressHTTPEvent):
    """Event for when an Ingress HTTP configuration is edited."""

    name: ClassVar[str] = "ingress_http_edited"
    routing_key_fmt: ClassVar[str] = "config.ingresses.http.edited"

    def __init__(self, ingress_http: IngressHTTPDict, **data):
        super().__init__(content=ingress_http, **data)
