# accent_bus/resources/application/event.py
# Copyright 2025 Accent Communications

"""Application events."""

from accent_bus.resources.common.event import TenantEvent
from accent_bus.resources.common.types import UUIDStr

from .types import ApplicationDict


class ApplicationCreatedEvent(TenantEvent):
    """Event for when an application is created."""

    service = "confd"
    name = "application_created"
    routing_key_fmt = "config.applications.created"

    def __init__(
        self,
        application: ApplicationDict,
        tenant_uuid: UUIDStr,
    ) -> None:
        """Initialize the event.

        Args:
           application (ApplicationDict): Application Dict
           tenant_uuid (UUIDStr): tenant UUID

        """
        super().__init__(application, tenant_uuid)


class ApplicationDeletedEvent(TenantEvent):
    """Event for when an application is deleted."""

    service = "confd"
    name = "application_deleted"
    routing_key_fmt = "config.applications.deleted"

    def __init__(
        self,
        application: ApplicationDict,
        tenant_uuid: UUIDStr,
    ) -> None:
        """Initialize event.

        Args:
           application (ApplicationDict): Application
           tenant_uuid (UUIDStr):  tenant UUID

        """
        super().__init__(application, tenant_uuid)


class ApplicationEditedEvent(TenantEvent):
    """Event for when an application is edited."""

    service = "confd"
    name = "application_edited"
    routing_key_fmt = "config.applications.edited"

    def __init__(
        self,
        application: ApplicationDict,
        tenant_uuid: UUIDStr,
    ) -> None:
        """Initialize Event.

        Args:
            application (ApplicationDict): application
            tenant_uuid (UUIDStr): tenant UUID

        """
        super().__init__(application, tenant_uuid)
