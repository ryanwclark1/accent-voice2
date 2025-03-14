# accent_bus/resources/line_endpoint/event.py
# Copyright 2025 Accent Communications

"""Line endpoint events."""

from accent_bus.resources.common.event import TenantEvent
from accent_bus.resources.common.types import UUIDStr

from .types import (
    LineDict,
    LineEndpointCustomDict,
    LineEndpointSCCPDict,
    LineEndpointSIPDict,
)


class LineEndpointSIPAssociatedEvent(TenantEvent):
    """Event for when a SIP line endpoint is associated."""

    service = "confd"
    name = "line_endpoint_sip_associated"
    routing_key_fmt = (
        "config.lines.{line[id]}.endpoints.sip.{endpoint_sip[uuid]}.updated"
    )

    def __init__(
        self,
        line: LineDict,
        sip: LineEndpointSIPDict,
        tenant_uuid: UUIDStr,
    ) -> None:
        """Initialize event.

        Args:
          line: Line
          sip: SIP
          tenant_uuid: tenant UUID

        """
        content = {"line": line, "endpoint_sip": sip}
        super().__init__(content, tenant_uuid)


class LineEndpointSIPDissociatedEvent(TenantEvent):
    """Event for when a SIP line endpoint is dissociated."""

    service = "confd"
    name = "line_endpoint_sip_dissociated"
    routing_key_fmt = (
        "config.lines.{line[id]}.endpoints.sip.{endpoint_sip[uuid]}.deleted"
    )

    def __init__(
        self,
        line: LineDict,
        sip: LineEndpointSIPDict,
        tenant_uuid: UUIDStr,
    ) -> None:
        """Initialize the event.

        Args:
           line: Line
           sip: SIP
           tenant_uuid: tenant UUID

        """
        content = {"line": line, "endpoint_sip": sip}
        super().__init__(content, tenant_uuid)


class LineEndpointSCCPAssociatedEvent(TenantEvent):
    """Event for when an SCCP line endpoint is associated."""

    service = "confd"
    name = "line_endpoint_sccp_associated"
    routing_key_fmt = (
        "config.lines.{line[id]}.endpoints.sccp.{endpoint_sccp[id]}.updated"
    )

    def __init__(
        self,
        line: LineDict,
        sccp: LineEndpointSCCPDict,
        tenant_uuid: UUIDStr,
    ) -> None:
        """Initialize event.

        Args:
          line: Line
          sccp: SCCP
          tenant_uuid: tenant UUID

        """
        content = {"line": line, "endpoint_sccp": sccp}
        super().__init__(content, tenant_uuid)


class LineEndpointSCCPDissociatedEvent(TenantEvent):
    """Event for when an SCCP line endpoint is dissociated."""

    service = "confd"
    name = "line_endpoint_sccp_dissociated"
    routing_key_fmt = (
        "config.lines.{line[id]}.endpoints.sccp.{endpoint_sccp[id]}.deleted"
    )

    def __init__(
        self,
        line: LineDict,
        sccp: LineEndpointSCCPDict,
        tenant_uuid: UUIDStr,
    ) -> None:
        """Initialize Event.

        Args:
          line: Line
          sccp: SCCP
          tenant_uuid: tenant UUID

        """
        content = {"line": line, "endpoint_sccp": sccp}
        super().__init__(content, tenant_uuid)


class LineEndpointCustomAssociatedEvent(TenantEvent):
    """Event for when a custom line endpoint is associated."""

    service = "confd"
    name = "line_endpoint_custom_associated"
    routing_key_fmt = (
        "config.lines.{line[id]}.endpoints.custom.{endpoint_custom[id]}.updated"
    )

    def __init__(
        self,
        line: LineDict,
        custom: LineEndpointCustomDict,
        tenant_uuid: UUIDStr,
    ) -> None:
        """Initialize the event.

        Args:
           line: Line
           custom: Custom
           tenant_uuid: tenant UUID

        """
        content = {"line": line, "endpoint_custom": custom}
        super().__init__(content, tenant_uuid)


class LineEndpointCustomDissociatedEvent(TenantEvent):
    """Event for when a custom line endpoint is dissociated."""

    service = "confd"
    name = "line_endpoint_custom_dissociated"
    routing_key_fmt = (
        "config.lines.{line[id]}.endpoints.custom.{endpoint_custom[id]}.deleted"
    )

    def __init__(
        self,
        line: LineDict,
        custom: LineEndpointCustomDict,
        tenant_uuid: UUIDStr,
    ) -> None:
        """Initialize the event.

        Args:
            line (LineDict): The line details.
            custom (LineEndpointCustomDict): The custom endpoint details.
            tenant_uuid (UUIDStr): The tenant UUID.

        """
        content = {"line": line, "endpoint_custom": custom}
        super().__init__(content, tenant_uuid)
