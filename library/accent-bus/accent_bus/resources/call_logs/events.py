# accent_bus/resources/call_logs/events.py
# Copyright 2025 Accent Communications

"""Call log events."""

from accent_bus.resources.common.event import TenantEvent, UserEvent
from accent_bus.resources.common.types import UUIDStr

from .types import CDRDataDict


class CallLogCreatedEvent(TenantEvent):
    """Event for when a call log is created."""

    service = "call_logd"
    name = "call_log_created"
    routing_key_fmt = "call_log.created"

    def __init__(self, cdr_data: CDRDataDict, tenant_uuid: UUIDStr) -> None:
        """Initialize event.

        Args:
           cdr_data: CDR data
           tenant_uuid: tenant UUID

        """
        super().__init__(cdr_data, tenant_uuid)


class CallLogUserCreatedEvent(UserEvent):
    """Event for when a user call log is created."""

    service = "call_logd"
    name = "call_log_user_created"
    routing_key_fmt = "call_log.user.{user_uuid}.created"

    def __init__(
        self,
        cdr_data: CDRDataDict,
        tenant_uuid: UUIDStr,
        user_uuid: UUIDStr,
    ) -> None:
        """Initialize event.

        Args:
          cdr_data: CDR Data
          tenant_uuid: tenant UUID
          user_uuid: user UUID

        """
        super().__init__(cdr_data, tenant_uuid, user_uuid)
