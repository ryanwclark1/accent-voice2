# resources/application/event.py
from typing import ClassVar

from resources.common.event import TenantEvent  # Import TenantEvent

from .types import ApplicationDict


class ApplicationEvent(TenantEvent):
    """Base class for Application events."""

    service: ClassVar[str] = "confd"
    content: ApplicationDict


class ApplicationCreatedEvent(ApplicationEvent):
    """Event for when an application is created."""

    name: ClassVar[str] = "application_created"
    routing_key_fmt: ClassVar[str] = "config.applications.created"

    def __init__(self, application: ApplicationDict, **data):
        super().__init__(content=application, **data)


class ApplicationDeletedEvent(ApplicationEvent):
    """Event for when an application is deleted."""

    name: ClassVar[str] = "application_deleted"
    routing_key_fmt: ClassVar[str] = "config.applications.deleted"

    def __init__(self, application: ApplicationDict, **data):
        super().__init__(content=application, **data)


class ApplicationEditedEvent(ApplicationEvent):
    """Event for when an application is edited."""

    name: ClassVar[str] = "application_edited"
    routing_key_fmt: ClassVar[str] = "config.applications.edited"

    def __init__(self, application: ApplicationDict, **data):
        super().__init__(content=application, **data)
