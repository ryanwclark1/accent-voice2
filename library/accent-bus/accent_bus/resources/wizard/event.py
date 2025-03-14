# accent_bus/resources/wizard/event.py
# Copyright 2025 Accent Communications

"""Wizard events."""

from accent_bus.resources.common.event import ServiceEvent


class WizardCreatedEvent(ServiceEvent):
    """Event for when a wizard is created."""

    service = "confd"
    name = "wizard_created"
    routing_key_fmt = "config.wizard.created"

    def __init__(self) -> None:
        """Initialize the event."""
        super().__init__()
