# accent_bus/resources/external_app/event.py
# Copyright 2025 Accent Communications

"""External app events."""

from accent_bus.resources.common.event import TenantEvent
from accent_bus.resources.common.types import UUIDStr

from .types import ExternalAppDict


class ExternalAppCreatedEvent(TenantEvent):
    """Event for when an external app is created."""

    service = "confd"
    name = "external_app_created"
    routing_key_fmt = "config.external_apps.created"

    def __init__(self, app: ExternalAppDict, tenant_uuid: UUIDStr) -> None:
        """Initialize Event.

        Args:
           app: External App
           tenant_uuid: tenant UUID

        """
        super().__init__(app, tenant_uuid)


class ExternalAppDeletedEvent(TenantEvent):
    """Event for when an external app is deleted."""

    service = "confd"
    name = "external_app_deleted"
    routing_key_fmt = "config.external_apps.deleted"

    def __init__(self, app: ExternalAppDict, tenant_uuid: UUIDStr) -> None:
        """Initialize event.

        Args:
          app: External App
          tenant_uuid: tenant UUID

        """
        super().__init__(app, tenant_uuid)


class ExternalAppEditedEvent(TenantEvent):
    """Event for when an external app is edited."""

    service = "confd"
    name = "external_app_edited"
    routing_key_fmt = "config.external_apps.edited"

    def __init__(self, app: ExternalAppDict, tenant_uuid: UUIDStr) -> None:
        """Initialize the event.

        Args:
            app (ExternalAppDict): The external app details.
            tenant_uuid (UUIDStr): The tenant UUID.

        """
        super().__init__(app, tenant_uuid)
