# accent_bus/resources/email/event.py
# Copyright 2025 Accent Communications

"""Email events."""

from accent_bus.resources.common.event import ServiceEvent


class EmailConfigUpdatedEvent(ServiceEvent):
    """Event for when email configuration is updated."""

    service = "confd"
    name = "email_config_updated"
    routing_key_fmt = "config.email.updated"

    def __init__(self) -> None:
        """Initialize the event."""
        super().__init__()
