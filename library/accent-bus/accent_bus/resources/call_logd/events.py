# resources/call_logd/events.py
from typing import ClassVar

from accent_bus.resources.common.event import TenantEvent

from .types import CallLogExportDataDict


class CallLogdEvent(TenantEvent):
    """Base class for call_logd events."""

    service: ClassVar[str] = "call_logd"
    content: dict


class CallLogExportCreatedEvent(CallLogdEvent):
    """Event for when a call log export is created."""

    name: ClassVar[str] = "call_logd_export_created"
    routing_key_fmt: ClassVar[str] = "call_logd.export.created"
    content: CallLogExportDataDict

    def __init__(
        self,
        export_data: CallLogExportDataDict,
        **data,
    ):
        super().__init__(content=export_data, **data)


class CallLogExportUpdatedEvent(CallLogdEvent):
    """Event for when a call log export is updated."""

    name: ClassVar[str] = "call_logd_export_updated"
    routing_key_fmt: ClassVar[str] = "call_logd.export.updated"
    content: CallLogExportDataDict

    def __init__(
        self,
        export_data: CallLogExportDataDict,
        **data,
    ):
        super().__init__(content=export_data, **data)


class CallLogRetentionUpdatedEvent(CallLogdEvent):
    """Event for when the call logs retention is updated."""

    name: ClassVar[str] = "call_logd_retention_updated"
    routing_key_fmt: ClassVar[str] = "call_logd.retention.updated"
    content: CallLogExportDataDict

    def __init__(
        self,
        retention_data: CallLogExportDataDict,
        **data,
    ):
        super().__init__(content=retention_data, **data)
