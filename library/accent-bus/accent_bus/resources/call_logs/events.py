# resources/call_logs/events.py
from typing import ClassVar

from accent_bus.resources.common.event import TenantEvent, UserEvent

from .types import CDRDataDict  # Assuming this is now a Pydantic model


class CallLogEvent(TenantEvent):
    """Base class for call log events."""

    service: ClassVar[str] = "call_logd"
    content: CDRDataDict


class CallLogCreatedEvent(CallLogEvent):
    """Event for when a call log is created."""

    name: ClassVar[str] = "call_log_created"
    routing_key_fmt: ClassVar[str] = "call_log.created"

    def __init__(self, cdr_data: CDRDataDict, **data):
        super().__init__(content=cdr_data, **data)


class CallLogUserCreatedEvent(UserEvent):
    """Event for when a call log is created, targeted at a specific user."""

    name: ClassVar[str] = "call_log_user_created"
    routing_key_fmt: ClassVar[str] = "call_log.user.{user_uuid}.created"
    service: ClassVar[str] = "call_logd"
    content: CDRDataDict

    def __init__(self, cdr_data: CDRDataDict, **data):
        super().__init__(content=cdr_data, **data)
