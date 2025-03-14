# resources/call_filter_user/event.py
from typing import ClassVar

from resources.common.event import TenantEvent


class CallFilterUserEvent(TenantEvent):
    """Base class for Call Filter User events."""

    service: ClassVar[str] = "confd"
    content: dict


class CallFilterRecipientUsersAssociatedEvent(CallFilterUserEvent):
    """Event for when recipient users are associated with a call filter."""

    name: ClassVar[str] = "call_filter_recipient_users_associated"
    routing_key_fmt: ClassVar[str] = "config.callfilters.recipients.users.updated"

    def __init__(self, call_filter_id: int, users: list[str], **data):
        content = {
            "call_filter_id": call_filter_id,
            "user_uuids": users,
        }
        super().__init__(content=content, **data)


class CallFilterSurrogateUsersAssociatedEvent(CallFilterUserEvent):
    """Event for when surrogate users are associated with a call filter."""

    name: ClassVar[str] = "call_filter_surrogate_users_associated"
    routing_key_fmt: ClassVar[str] = "config.callfilters.surrogates.users.updated"

    def __init__(self, call_filter_id: int, users: list[str], **data):
        content = {
            "call_filter_id": call_filter_id,
            "user_uuids": users,
        }
        super().__init__(content=content, **data)
