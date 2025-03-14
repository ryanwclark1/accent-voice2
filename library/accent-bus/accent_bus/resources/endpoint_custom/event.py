# accent_bus/resources/endpoint_custom/event.py
# Copyright 2025 Accent Communications

"""Custom endpoint events."""

from accent_bus.resources.common.event import TenantEvent
from accent_bus.resources.common.types import UUIDStr

from .types import EndpointCustomDict


class CustomEndpointCreatedEvent(TenantEvent):
    """Event for when a custom endpoint is created."""

    service = "confd"
    name = "custom_endpoint_created"
    routing_key_fmt = "config.custom_endpoint.created"

    def __init__(
        self,
        endpoint: EndpointCustomDict,
        tenant_uuid: UUIDStr,
    ) -> None:
        """Initialize event.

        Args:
          endpoint: Endpoint
          tenant_uuid: tenant UUID

        """
        super().__init__(endpoint, tenant_uuid)


class CustomEndpointDeletedEvent(TenantEvent):
    """Event for when a custom endpoint is deleted."""

    service = "confd"
    name = "custom_endpoint_deleted"
    routing_key_fmt = "config.custom_endpoint.deleted"

    def __init__(
        self,
        endpoint: EndpointCustomDict,
        tenant_uuid: UUIDStr,
    ) -> None:
        """Initialize the event.

        Args:
            endpoint (EndpointCustomDict): custom endpoint details.
            tenant_uuid (UUIDStr): tenant UUID.

        """
        super().__init__(endpoint, tenant_uuid)


class CustomEndpointEditedEvent(TenantEvent):
    """Event for when a custom endpoint is edited."""

    service = "confd"
    name = "custom_endpoint_edited"
    routing_key_fmt = "config.custom_endpoint.edited"

    def __init__(
        self,
        endpoint: EndpointCustomDict,
        tenant_uuid: UUIDStr,
    ) -> None:
        """Initialize event.

        Args:
          endpoint: Endpoint
          tenant_uuid: tenant UUID

        """
        super().__init__(endpoint, tenant_uuid)
