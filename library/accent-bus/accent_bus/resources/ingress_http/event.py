# accent_bus/resources/ingress_http/event.py
# Copyright 2025 Accent Communications

"""Ingress HTTP events."""

from accent_bus.resources.common.event import TenantEvent
from accent_bus.resources.common.types import UUIDStr

from .types import IngressHTTPDict


class IngressHTTPCreatedEvent(TenantEvent):
    """Event for when an HTTP ingress is created."""

    service = "confd"
    name = "ingress_http_created"
    routing_key_fmt = "config.ingresses.http.created"

    def __init__(
        self,
        ingress_http: IngressHTTPDict,
        tenant_uuid: UUIDStr,
    ) -> None:
        """Initialize event.

        Args:
            ingress_http (IngressHTTPDict):  ingress HTTP details.
            tenant_uuid (UUIDStr): tenant UUID.

        """
        super().__init__(ingress_http, tenant_uuid)


class IngressHTTPDeletedEvent(TenantEvent):
    """Event for when an HTTP ingress is deleted."""

    service = "confd"
    name = "ingress_http_deleted"
    routing_key_fmt = "config.ingresses.http.deleted"

    def __init__(
        self,
        ingress_http: IngressHTTPDict,
        tenant_uuid: UUIDStr,
    ) -> None:
        """Initialize event.

        Args:
          ingress_http: Ingress Http
          tenant_uuid: tenant UUID

        """
        super().__init__(ingress_http, tenant_uuid)


class IngressHTTPEditedEvent(TenantEvent):
    """Event for when an HTTP ingress is edited."""

    service = "confd"
    name = "ingress_http_edited"
    routing_key_fmt = "config.ingresses.http.edited"

    def __init__(
        self,
        ingress_http: IngressHTTPDict,
        tenant_uuid: UUIDStr,
    ) -> None:
        """Initialize the event.

        Args:
           ingress_http (IngressHTTPDict):  ingress HTTP details.
           tenant_uuid (UUIDStr):  tenant UUID.

        """
        super().__init__(ingress_http, tenant_uuid)
