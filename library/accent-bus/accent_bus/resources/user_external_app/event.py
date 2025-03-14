# resources/user_external_app/event.py
from typing import ClassVar

from resources.common.event import TenantEvent

from .types import ExternalAppDict


class UserExternalAppEvent(TenantEvent):
    """Base class for User External App events."""

    service: ClassVar[str] = "confd"
    content: dict


class UserExternalAppCreatedEvent(UserExternalAppEvent):
    """Event for when an external application is created for a user."""

    name: ClassVar[str] = "user_external_app_created"
    routing_key_fmt: ClassVar[str] = "config.user_external_apps.created"

    def __init__(self, app: ExternalAppDict, **data):
        super().__init__(content=app.model_dump(), **data)


class UserExternalAppDeletedEvent(UserExternalAppEvent):
    """Event for when an external application is deleted for a user."""

    name: ClassVar[str] = "user_external_app_deleted"
    routing_key_fmt: ClassVar[str] = "config.user_external_apps.deleted"

    def __init__(self, app: ExternalAppDict, **data):
        super().__init__(content=app.model_dump(), **data)


class UserExternalAppEditedEvent(UserExternalAppEvent):
    """Event for when an external application is edited for a user."""

    name: ClassVar[str] = "user_external_app_edited"
    routing_key_fmt: ClassVar[str] = "config.user_external_apps.edited"

    def __init__(self, app: ExternalAppDict, **data):
        super().__init__(content=app.model_dump(), **data)
