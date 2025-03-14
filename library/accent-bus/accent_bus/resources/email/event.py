# resources/email/event.py
from typing import ClassVar

from resources.common.event import ServiceEvent


class EmailEvent(ServiceEvent):
    """Base class for Email events."""

    service: ClassVar[str] = "confd"
    content: dict = {}  # All ServiceEvents should define 'content'


class EmailConfigUpdatedEvent(EmailEvent):
    """Event for when email configuration is updated."""

    name: ClassVar[str] = "email_config_updated"
    routing_key_fmt: ClassVar[str] = "config.email.updated"
