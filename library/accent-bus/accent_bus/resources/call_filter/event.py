# resources/call_filter/event.py
from typing import ClassVar

from accent_bus.resources.common.event import TenantEvent


class CallFilterEvent(TenantEvent):
    """Base class for Call Filter events."""

    service: ClassVar[str] = "confd"
    content: dict


class CallFilterCreatedEvent(CallFilterEvent):
    """Event for when a call filter is created."""

    name: ClassVar[str] = "call_filter_created"
    routing_key_fmt: ClassVar[str] = "config.callfilter.created"

    def __init__(self, call_filter_id: int, **data):
        content = {"id": call_filter_id}
        super().__init__(content=content, **data)


class CallFilterDeletedEvent(CallFilterEvent):
    """Event for when a call filter is deleted."""

    name: ClassVar[str] = "call_filter_deleted"
    routing_key_fmt: ClassVar[str] = "config.callfilter.deleted"

    def __init__(self, call_filter_id: int, **data):
        content = {"id": call_filter_id}
        super().__init__(content=content, **data)


class CallFilterEditedEvent(CallFilterEvent):
    """Event for when a call filter is edited."""

    name: ClassVar[str] = "call_filter_edited"
    routing_key_fmt: ClassVar[str] = "config.callfilter.edited"

    def __init__(self, call_filter_id: int, **data):
        content = {"id": call_filter_id}
        super().__init__(content=content, **data)


class CallFilterFallbackEditedEvent(CallFilterEvent):
    """Event for when a call filter fallback is edited."""

    name: ClassVar[str] = "call_filter_fallback_edited"
    routing_key_fmt: ClassVar[str] = "config.callfilters.fallbacks.edited"

    def __init__(self, call_filter_id: int, **data):
        content = {"id": call_filter_id}
        super().__init__(content=content, **data)
