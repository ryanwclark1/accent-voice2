# accent_bus/resources/rtp/event.py
# Copyright 2025 Accent Communications

"""RTP events."""

from accent_bus.resources.common.event import ServiceEvent


class RTPGeneralEditedEvent(ServiceEvent):
    """Event for when general RTP settings are edited."""

    service = "confd"
    name = "rtp_general_edited"
    routing_key_fmt = "config.rtp_general.edited"

    def __init__(self) -> None:
        """Initialize event."""
        super().__init__()


class RTPIceHostCandidatesEditedEvent(ServiceEvent):
    """Event for when RTP ICE host candidates are edited."""

    service = "confd"
    name = "rtp_ice_host_candidates_edited"
    routing_key_fmt = "config.rtp_ice_host_candidates.edited"

    def __init__(self) -> None:
        """Initialize event."""
        super().__init__()
