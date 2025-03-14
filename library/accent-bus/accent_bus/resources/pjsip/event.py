# resources/pjsip/event.py
from typing import ClassVar

from accent_bus.resources.common.event import ServiceEvent

from .types import PJSIPTransportDict


class PJSIPEvent(ServiceEvent):
    """Base class for PJSIP events."""

    service: ClassVar[str] = "confd"
    content: dict = {}


class PJSIPGlobalUpdatedEvent(PJSIPEvent):
    """Event for when global PJSIP settings are updated."""

    name: ClassVar[str] = "pjsip_global_updated"
    routing_key_fmt: ClassVar[str] = "config.pjsip_global.updated"


class PJSIPSystemUpdatedEvent(PJSIPEvent):
    """Event for when system PJSIP settings are updated."""

    name: ClassVar[str] = "pjsip_system_updated"
    routing_key_fmt: ClassVar[str] = "config.pjsip_system.updated"


class SIPTransportEvent(PJSIPEvent):
    """Base class for SIP transport events."""

    content: PJSIPTransportDict


class SIPTransportCreatedEvent(SIPTransportEvent):
    """Event for when a SIP transport is created."""

    name: ClassVar[str] = "sip_transport_created"
    routing_key_fmt: ClassVar[str] = "config.sip.transports.created"

    def __init__(self, transport: PJSIPTransportDict, **data):
        super().__init__(content=transport, **data)


class SIPTransportDeletedEvent(SIPTransportEvent):
    """Event for when a SIP transport is deleted."""

    name: ClassVar[str] = "sip_transport_deleted"
    routing_key_fmt: ClassVar[str] = "config.sip.transports.deleted"

    def __init__(self, transport: PJSIPTransportDict, **data):
        super().__init__(content=transport, **data)


class SIPTransportEditedEvent(SIPTransportEvent):
    """Event for when a SIP transport is edited."""

    name: ClassVar[str] = "sip_transport_edited"
    routing_key_fmt: ClassVar[str] = "config.sip.transports.edited"

    def __init__(self, transport: PJSIPTransportDict, **data):
        super().__init__(content=transport, **data)
