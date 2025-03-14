# resources/rtp/event.py
from typing import ClassVar

from accent_bus.resources.common.event import ServiceEvent


class RTPEvent(ServiceEvent):
    """Base class for RTP (Real-time Transport Protocol) events."""

    service: ClassVar[str] = "confd"
    content: dict = {}


class RTPGeneralEditedEvent(RTPEvent):
    """Event for when general RTP configuration is edited."""

    name: ClassVar[str] = "rtp_general_edited"
    routing_key_fmt: ClassVar[str] = "config.rtp_general.edited"


class RTPIceHostCandidatesEditedEvent(RTPEvent):
    """Event for when ICE host candidates are edited."""

    name: ClassVar[str] = "rtp_ice_host_candidates_edited"
    routing_key_fmt: ClassVar[str] = "config.rtp_ice_host_candidates.edited"
