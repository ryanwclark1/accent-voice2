# accent_bus/resources/iax_callnumberlimits/event.py
# Copyright 2025 Accent Communications

"""IAX call number limits events."""

from accent_bus.resources.common.event import ServiceEvent


class IAXCallNumberLimitsEditedEvent(ServiceEvent):
    """Event for when IAX call number limits are edited."""

    service = "confd"
    name = "iax_callnumberlimits_edited"
    routing_key_fmt = "config.iax_callnumberlimits.edited"

    def __init__(self) -> None:
        """Initialize the event."""
        super().__init__()
