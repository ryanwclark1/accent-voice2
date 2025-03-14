# accent_bus/resources/user_external_app/event.py
# Copyright 2025 Accent Communications

"""User external app events."""

from accent_bus.resources.common.event import TenantEvent
from accent_bus.resources.common.types import UUIDStr

from .types import ExternalAppDict


class UserExternalAppCreatedEvent(TenantEvent):
    """Event for when a user external app is created."""

    service = "confd"
    name = "user_external_app_created"
    routing_key_fmt = "config.user_external_apps.created"

    def __init__(self, app: ExternalAppDict, tenant_uuid: UUIDStr) -> None:
        """Initialize event.

        Args:
          app: External App
          tenant_uuid: tenant UUID

        """
        super().__init__(app, tenant_uuid)


class UserExternalAppDeletedEvent(TenantEvent):
    """Event for when a user external app is deleted."""

    service = "confd"
    name = "user_external_app_deleted"
    routing_key_fmt = "config.user_external_apps.deleted"

    def __init__(self, app: ExternalAppDict, tenant_uuid: UUIDStr) -> None:
        """Initialize the event.

        Args:
            app (ExternalAppDict): The external app details.
            tenant_uuid (UUIDStr): The tenant UUID.

        """
        super().__init__(app, tenant_uuid)


class UserExternalAppEditedEvent(TenantEvent):
    """Event for when a user external app is edited."""

    service = "confd"
    name = "user_external_app_edited"
    routing_key_fmt = "config.user_external_apps.edited"

    def __init__(self, app: ExternalAppDict, tenant_uuid: UUIDStr) -> None:
        """Initialize event.

        Args:
            app (ExternalAppDict): The external app details.
            tenant_uuid (UUIDStr): The tenant UUID.

        """
        super().__init__(app, tenant_uuid)
