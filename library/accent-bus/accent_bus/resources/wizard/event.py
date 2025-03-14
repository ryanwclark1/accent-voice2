# resources/wizard/event.py
from typing import ClassVar

from accent_bus.resources.common.event import ServiceEvent


class WizardEvent(ServiceEvent):
    """Base class for Wizard events."""

    service: ClassVar[str] = "confd"
    content: dict = {}  # ServiceEvents should define a content attribute


class WizardCreatedEvent(WizardEvent):
    """Event for when the wizard is created."""

    name: ClassVar[str] = "wizard_created"
    routing_key_fmt: ClassVar[str] = "config.wizard.created"
