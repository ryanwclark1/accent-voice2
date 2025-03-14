# accent_bus/resources/endpoint_iax/event.py
# Copyright 2025 Accent Communications

"""IAX endpoint events."""

from accent_bus.resources.common.event import TenantEvent
from accent_bus.resources.common.types import UUIDStr

from .types import EndpointIAXDict


class IAXEndpointCreatedEvent(TenantEvent):
    """Event for when an IAX endpoint is created."""

    service = "confd"
    name = "iax_endpoint_created"
    routing_key_fmt = "config.iax_endpoint.created"

    def __init__(self, endpoint: EndpointIAXDict, tenant_uuid: UUIDStr) -> None:
        """Initialize the event.

        Args:
           endpoint: Endpoint
           tenant_uuid: tenant UUID

        """
        super().__init__(endpoint, tenant_uuid)


class IAXEndpointDeletedEvent(TenantEvent):
    """Event for when an IAX endpoint is deleted."""

    service = "confd"
    name = "iax_endpoint_deleted"
    routing_key_fmt = "config.iax_endpoint.deleted"

    def __init__(self, endpoint: EndpointIAXDict, tenant_uuid: UUIDStr) -> None:
        """Initialize event.

        Args:
           endpoint: Endpoint
           tenant_uuid: tenant UUID

        """
        super().__init__(endpoint, tenant_uuid)


class IAXEndpointEditedEvent(TenantEvent):
    """Event for when an IAX endpoint is edited."""

    service = "confd"
    name = "iax_endpoint_edited"
    routing_key_fmt = "config.iax_endpoint.edited"

    def __init__(self, endpoint: EndpointIAXDict, tenant_uuid: UUIDStr) -> None:
        """Initialize Event.

        Args:
          endpoint: Endpoint
          tenant_uuid: tenant UUID

        """
        super().__init__(endpoint, tenant_uuid)
