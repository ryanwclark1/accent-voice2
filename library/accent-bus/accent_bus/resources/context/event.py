# accent_bus/resources/context/event.py
# Copyright 2025 Accent Communications

"""Context events."""

from accent_bus.resources.common.event import TenantEvent
from accent_bus.resources.common.types import UUIDStr

from .types import ContextDict


class ContextCreatedEvent(TenantEvent):
    """Event for when a context is created."""

    service = "confd"
    name = "context_created"
    routing_key_fmt = "config.contexts.created"

    def __init__(self, context_data: ContextDict, tenant_uuid: UUIDStr) -> None:
        """Initialize event.

        Args:
           context_data: Context data
           tenant_uuid:  tenant UUID

        """
        super().__init__(context_data, tenant_uuid)


class ContextDeletedEvent(TenantEvent):
    """Event for when a context is deleted."""

    service = "confd"
    name = "context_deleted"
    routing_key_fmt = "config.contexts.deleted"

    def __init__(self, context_data: ContextDict, tenant_uuid: UUIDStr) -> None:
        """Initialize event.

        Args:
            context_data (ContextDict): context data.
            tenant_uuid (UUIDStr): tenant UUID.

        """
        super().__init__(context_data, tenant_uuid)


class ContextEditedEvent(TenantEvent):
    """Event for when a context is edited."""

    service = "confd"
    name = "context_edited"
    routing_key_fmt = "config.contexts.edited"

    def __init__(self, context_data: ContextDict, tenant_uuid: UUIDStr) -> None:
        """Initialize event.

        Args:
           context_data: Context data
           tenant_uuid: tenant UUID

        """
        super().__init__(context_data, tenant_uuid)
