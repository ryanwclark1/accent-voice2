# accent_bus/resources/queue_general/event.py
# Copyright 2025 Accent Communications

"""Queue general events."""

from accent_bus.resources.common.event import ServiceEvent


class QueueGeneralEditedEvent(ServiceEvent):
    """Event for when general queue settings are edited."""

    service = "confd"
    name = "queue_general_edited"
    routing_key_fmt = "config.queue_general.edited"

    def __init__(self) -> None:
        """Initialize the event."""
        super().__init__()
