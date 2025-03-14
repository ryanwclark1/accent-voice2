# accent_bus/resources/iax_general/event.py
# Copyright 2025 Accent Communications

"""IAX general events."""

from accent_bus.resources.common.event import ServiceEvent


class IAXGeneralEditedEvent(ServiceEvent):
    """Event for when general IAX settings are edited."""

    service = "confd"
    name = "iax_general_edited"
    routing_key_fmt = "config.iax_general.edited"

    def __init__(self) -> None:
        """Initialize the event."""
        super().__init__()
