# resources/external_app/event.py
from typing import ClassVar

from resources.common.event import TenantEvent

from .types import ExternalAppDict


class ExternalAppEvent(TenantEvent):
    """Base class for External Application events."""

    service: ClassVar[str] = "confd"
    content: dict


class ExternalAppCreatedEvent(ExternalAppEvent):
    """Event for when an external application is created."""

    name: ClassVar[str] = "external_app_created"
    routing_key_fmt: ClassVar[str] = "config.external_apps.created"

    def __init__(self, app: ExternalAppDict, **data):
        super().__init__(content=app, **data)


class ExternalAppDeletedEvent(ExternalAppEvent):
    """Event for when an external application is deleted."""

    name: ClassVar[str] = "external_app_deleted"
    routing_key_fmt: ClassVar[str] = "config.external_apps.deleted"

    def __init__(self, app: ExternalAppDict, **data):
        super().__init__(content=app, **data)


class ExternalAppEditedEvent(ExternalAppEvent):
    """Event for when an external application is edited."""

    name: ClassVar[str] = "external_app_edited"
    routing_key_fmt: ClassVar[str] = "config.external_apps.edited"

    def __init__(self, app: ExternalAppDict, **data):
        super().__init__(content=app, **data)
