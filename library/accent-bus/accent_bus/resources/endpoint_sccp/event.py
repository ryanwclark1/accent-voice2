# accent_bus/resources/endpoint_sccp/event.py
# Copyright 2025 Accent Communications

"""SCCP endpoint events."""

from accent_bus.resources.common.event import TenantEvent
from accent_bus.resources.common.types import UUIDStr

from .types import EndpointSCCPDict


class SCCPEndpointCreatedEvent(TenantEvent):
    """Event for when an SCCP endpoint is created."""

    service = "confd"
    name = "sccp_endpoint_created"
    routing_key_fmt = "config.sccp_endpoint.created"

    def __init__(
        self,
        endpoint: EndpointSCCPDict,
        tenant_uuid: UUIDStr,
    ) -> None:
        """Initialize event.

        Args:
            endpoint (EndpointSCCPDict): sccp endpoint.
            tenant_uuid (UUIDStr):  tenant UUID.

        """
        super().__init__(endpoint, tenant_uuid)


class SCCPEndpointDeletedEvent(TenantEvent):
    """Event for when an SCCP endpoint is deleted."""

    service = "confd"
    name = "sccp_endpoint_deleted"
    routing_key_fmt = "config.sccp_endpoint.deleted"

    def __init__(
        self,
        endpoint: EndpointSCCPDict,
        tenant_uuid: UUIDStr,
    ) -> None:
        """Initialize the event.

        Args:
          endpoint: Endpoint
          tenant_uuid: tenant UUID

        """
        super().__init__(endpoint, tenant_uuid)


class SCCPEndpointEditedEvent(TenantEvent):
    """Event for when an SCCP endpoint is edited."""

    service = "confd"
    name = "sccp_endpoint_edited"
    routing_key_fmt = "config.sccp_endpoint.edited"

    def __init__(
        self,
        endpoint: EndpointSCCPDict,
        tenant_uuid: UUIDStr,
    ) -> None:
        """Initialize event.

        Args:
           endpoint: Endpoint
           tenant_uuid: tenant UUID

        """
        super().__init__(endpoint, tenant_uuid)
