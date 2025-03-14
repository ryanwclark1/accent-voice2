# resources/push_notification/events.py
from typing import ClassVar

from accent_bus.resources.common.event import UserEvent

from .types import PushMobileDict


class PushNotificationEvent(UserEvent):
    """Base class for Push Notification events."""

    service: ClassVar[str] = "calld"
    required_acl_fmt: ClassVar[str] = "events.calls.{user_uuid}"
    content: dict


class CallPushNotificationEvent(PushNotificationEvent):
    """Event for sending a call push notification."""

    name: ClassVar[str] = "call_push_notification"
    routing_key_fmt: ClassVar[str] = "calls.call.push_notification"

    def __init__(self, push: PushMobileDict, **data):
        super().__init__(content=push.model_dump(), **data)


class CallCancelPushNotificationEvent(PushNotificationEvent):
    """Event for cancelling a call push notification."""

    name: ClassVar[str] = "call_cancel_push_notification"
    routing_key_fmt: ClassVar[str] = "calls.call.cancel_push_notification"

    def __init__(self, push: PushMobileDict, **data):
        super().__init__(content=push.model_dump(), **data)
