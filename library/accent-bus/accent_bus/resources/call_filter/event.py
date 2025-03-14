# accent_bus/resources/call_filter/event.py
# Copyright 2025 Accent Communications

"""Call filter events."""

from accent_bus.resources.common.event import TenantEvent
from accent_bus.resources.common.types import UUIDStr


class CallFilterCreatedEvent(TenantEvent):
    """Event for when a call filter is created."""

    service = "confd"
    name = "call_filter_created"
    routing_key_fmt = "config.callfilter.created"

    def __init__(self, call_filter_id: int, tenant_uuid: UUIDStr) -> None:
        """Initialize event.

        Args:
          call_filter_id: Call Filter ID
          tenant_uuid: Tenant UUID

        """
        content = {"id": call_filter_id}
        super().__init__(content, tenant_uuid)


class CallFilterDeletedEvent(TenantEvent):
    """Event for when a call filter is deleted."""

    service = "confd"
    name = "call_filter_deleted"
    routing_key_fmt = "config.callfilter.deleted"

    def __init__(self, call_filter_id: int, tenant_uuid: UUIDStr) -> None:
        """Initialize the event.

        Args:
          call_filter_id: Call Filter ID
          tenant_uuid: tenant UUID

        """
        content = {"id": call_filter_id}
        super().__init__(content, tenant_uuid)


class CallFilterEditedEvent(TenantEvent):
    """Event for when a call filter is edited."""

    service = "confd"
    name = "call_filter_edited"
    routing_key_fmt = "config.callfilter.edited"

    def __init__(self, call_filter_id: int, tenant_uuid: UUIDStr) -> None:
        """Initialize Event.

        Args:
            call_filter_id (int):  Call Filter ID
            tenant_uuid (UUIDStr):  tenant UUID

        """
        content = {"id": call_filter_id}
        super().__init__(content, tenant_uuid)


class CallFilterFallbackEditedEvent(TenantEvent):
    """Event for when a call filter fallback is edited."""

    service = "confd"
    name = "call_filter_fallback_edited"
    routing_key_fmt = "config.callfilters.fallbacks.edited"

    def __init__(self, call_filter_id: int, tenant_uuid: UUIDStr) -> None:
        """Initialize event.

        Args:
           call_filter_id: Call Filter ID
           tenant_uuid: tenant UUID

        """
        content = {"id": call_filter_id}
        super().__init__(content, tenant_uuid)
