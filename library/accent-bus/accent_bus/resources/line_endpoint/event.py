# resources/line_endpoint/event.py
from typing import ClassVar

from accent_bus.resources.common.event import TenantEvent

from .types import (
    LineDict,
    LineEndpointCustomDict,
    LineEndpointSCCPDict,
    LineEndpointSIPDict,
)


class LineEndpointEvent(TenantEvent):
    """Base class for Line Endpoint events."""

    service: ClassVar[str] = "confd"
    content: dict


class LineEndpointSIPAssociatedEvent(LineEndpointEvent):
    """Event for when a SIP endpoint is associated with a line."""

    name: ClassVar[str] = "line_endpoint_sip_associated"
    routing_key_fmt: ClassVar[str] = (
        "config.lines.{line[id]}.endpoints.sip.{endpoint_sip[uuid]}.updated"
    )

    def __init__(
        self,
        line: LineDict,
        sip: LineEndpointSIPDict,
        **data,
    ):
        content = {"line": line, "endpoint_sip": sip}
        super().__init__(content=content, **data)


class LineEndpointSIPDissociatedEvent(LineEndpointEvent):
    """Event for when a SIP endpoint is dissociated from a line."""

    name: ClassVar[str] = "line_endpoint_sip_dissociated"
    routing_key_fmt: ClassVar[str] = (
        "config.lines.{line[id]}.endpoints.sip.{endpoint_sip[uuid]}.deleted"
    )

    def __init__(self, line: LineDict, sip: LineEndpointSIPDict, **data):
        content = {"line": line, "endpoint_sip": sip}
        super().__init__(content=content, **data)


class LineEndpointSCCPAssociatedEvent(LineEndpointEvent):
    """Event for when an SCCP endpoint is associated with a line."""

    name: ClassVar[str] = "line_endpoint_sccp_associated"
    routing_key_fmt: ClassVar[str] = (
        "config.lines.{line[id]}.endpoints.sccp.{endpoint_sccp[id]}.updated"
    )

    def __init__(
        self,
        line: LineDict,
        sccp: LineEndpointSCCPDict,
        **data,
    ):
        content = {"line": line, "endpoint_sccp": sccp}
        super().__init__(content=content, **data)


class LineEndpointSCCPDissociatedEvent(LineEndpointEvent):
    """Event for when an SCCP endpoint is dissociated from a line."""

    name: ClassVar[str] = "line_endpoint_sccp_dissociated"
    routing_key_fmt: ClassVar[str] = (
        "config.lines.{line[id]}.endpoints.sccp.{endpoint_sccp[id]}.deleted"
    )

    def __init__(self, line: LineDict, sccp: LineEndpointSCCPDict, **data):
        content = {"line": line, "endpoint_sccp": sccp}
        super().__init__(content=content, **data)


class LineEndpointCustomAssociatedEvent(LineEndpointEvent):
    """Event for when a custom endpoint is associated with a line."""

    name: ClassVar[str] = "line_endpoint_custom_associated"
    routing_key_fmt: ClassVar[str] = (
        "config.lines.{line[id]}.endpoints.custom.{endpoint_custom[id]}.updated"
    )

    def __init__(self, line: LineDict, custom: LineEndpointCustomDict, **data):
        content = {"line": line, "endpoint_custom": custom}
        super().__init__(content=content, **data)


class LineEndpointCustomDissociatedEvent(LineEndpointEvent):
    """Event for when a custom endpoint is dissociated from a line."""

    name: ClassVar[str] = "line_endpoint_custom_dissociated"
    routing_key_fmt: ClassVar[str] = (
        "config.lines.{line[id]}.endpoints.custom.{endpoint_custom[id]}.deleted"
    )

    def __init__(self, line: LineDict, custom: LineEndpointCustomDict, **data):
        content = {"line": line, "endpoint_custom": custom}
        super().__init__(content=content, **data)
