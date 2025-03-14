# accent_bus/resources/pjsip/event.py
# Copyright 2025 Accent Communications

"""PJSIP events."""

from accent_bus.resources.common.event import ServiceEvent

from .types import PJSIPTransportDict


class PJSIPGlobalUpdatedEvent(ServiceEvent):
    """Event for when global PJSIP settings are updated."""

    service = "confd"
    name = "pjsip_global_updated"
    routing_key_fmt = "config.pjsip_global.updated"

    def __init__(self) -> None:
        """Initialize the event."""
        super().__init__()


class PJSIPSystemUpdatedEvent(ServiceEvent):
    """Event for when system PJSIP settings are updated."""

    service = "confd"
    name = "pjsip_system_updated"
    routing_key_fmt = "config.pjsip_system.updated"

    def __init__(self) -> None:
        """Initialize event."""
        super().__init__()


class SIPTransportCreatedEvent(ServiceEvent):
    """Event for when a SIP transport is created."""

    service = "confd"
    name = "sip_transport_created"
    routing_key_fmt = "config.sip.transports.created"

    def __init__(self, transport: PJSIPTransportDict) -> None:
        """Initialize event.

        Args:
          transport: Transport

        """
        super().__init__(transport)


class SIPTransportDeletedEvent(ServiceEvent):
    """Event for when a SIP transport is deleted."""

    service = "confd"
    name = "sip_transport_deleted"
    routing_key_fmt = "config.sip.transports.deleted"

    def __init__(self, transport: PJSIPTransportDict) -> None:
        """Initialize Event.

        Args:
            transport (PJSIPTransportDict): The SIP transport details.

        """
        super().__init__(transport)


class SIPTransportEditedEvent(ServiceEvent):
    """Event for when a SIP transport is edited."""

    service = "confd"
    name = "sip_transport_edited"
    routing_key_fmt = "config.sip.transports.edited"

    def __init__(self, transport: PJSIPTransportDict) -> None:
        """Initialize event.

        Args:
           transport: Transport

        """
        super().__init__(transport)
