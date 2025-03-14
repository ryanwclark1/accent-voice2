# accent_bus/resources/call_logd/events.py
# Copyright 2025 Accent Communications

"""Call logd events."""

from accent_bus.resources.common.event import TenantEvent
from accent_bus.resources.common.types import UUIDStr

from .types import CallLogExportDataDict


class CallLogExportCreatedEvent(TenantEvent):
    """Event for when a call log export is created."""

    service = "call_logd"
    name = "call_logd_export_created"
    routing_key_fmt = "call_logd.export.created"

    def __init__(
        self,
        export_data: CallLogExportDataDict,
        tenant_uuid: UUIDStr,
    ) -> None:
        """Initialize the event.

        Args:
           export_data: Export data
           tenant_uuid: tenant UUID

        """
        super().__init__(export_data, tenant_uuid)


class CallLogExportUpdatedEvent(TenantEvent):
    """Event for when a call log export is updated."""

    service = "call_logd"
    name = "call_logd_export_updated"
    routing_key_fmt = "call_logd.export.updated"

    def __init__(
        self,
        export_data: CallLogExportDataDict,
        tenant_uuid: UUIDStr,
    ) -> None:
        """Initialize event.

        Args:
           export_data: Export data
           tenant_uuid: tenant UUID

        """
        super().__init__(export_data, tenant_uuid)


class CallLogRetentionUpdatedEvent(TenantEvent):
    """Event for when call log retention is updated."""

    service = "call_logd"
    name = "call_logd_retention_updated"
    routing_key_fmt = "call_logd.retention.updated"

    def __init__(
        self,
        retention_data: CallLogExportDataDict,
        tenant_uuid: UUIDStr,
    ) -> None:
        """Initialize event.

        Args:
          retention_data: Retention data
          tenant_uuid: tenant UUID

        """
        super().__init__(retention_data, tenant_uuid)
