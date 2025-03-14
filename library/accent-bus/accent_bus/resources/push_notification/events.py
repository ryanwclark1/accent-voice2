# accent_bus/resources/push_notification/events.py
# Copyright 2025 Accent Communications

"""Push notification events."""

from accent_bus.resources.common.event import UserEvent
from accent_bus.resources.common.types import UUIDStr

from .types import PushMobileDict


class CallPushNotificationEvent(UserEvent):
    """Event for sending a push notification for a call."""

    service = "calld"
    name = "call_push_notification"
    routing_key_fmt = "calls.call.push_notification"
    required_acl_fmt = "events.calls.{user_uuid}"

    def __init__(
        self,
        push: PushMobileDict,
        tenant_uuid: UUIDStr,
        user_uuid: UUIDStr,
    ) -> None:
        """Initialize the event.

        Args:
            push (PushMobileDict): Push notification details.
            tenant_uuid (UUIDStr): The tenant UUID.
            user_uuid (UUIDStr): The user UUID.

        """
        super().__init__(push, tenant_uuid, user_uuid)


class CallCancelPushNotificationEvent(UserEvent):
    """Event for canceling a push notification for a call."""

    service = "calld"
    name = "call_cancel_push_notification"
    routing_key_fmt = "calls.call.cancel_push_notification"
    required_acl_fmt = "events.calls.{user_uuid}"

    def __init__(
        self,
        push: PushMobileDict,
        tenant_uuid: UUIDStr,
        user_uuid: UUIDStr,
    ) -> None:
        """Initialize event.

        Args:
          push: Push
          tenant_uuid: tenant UUID
          user_uuid: user UUID

        """
        super().__init__(push, tenant_uuid, user_uuid)
