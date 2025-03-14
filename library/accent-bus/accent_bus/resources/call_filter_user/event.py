# accent_bus/resources/call_filter_user/event.py
# Copyright 2025 Accent Communications

"""Call filter user events."""

from accent_bus.resources.common.event import TenantEvent
from accent_bus.resources.common.types import UUIDStr


class CallFilterRecipientUsersAssociatedEvent(TenantEvent):
    """Event for when recipient users are associated with a call filter."""

    service = "confd"
    name = "call_filter_recipient_users_associated"
    routing_key_fmt = "config.callfilters.recipients.users.updated"

    def __init__(
        self,
        call_filter_id: int,
        users: list[str],
        tenant_uuid: UUIDStr,
    ) -> None:
        """Initialize the event.

        Args:
           call_filter_id:  Call Filter ID
           users: List of User UUID
           tenant_uuid: tenant UUID

        """
        content = {
            "call_filter_id": call_filter_id,
            "user_uuids": users,
        }
        super().__init__(content, tenant_uuid)


class CallFilterSurrogateUsersAssociatedEvent(TenantEvent):
    """Event for when surrogate users are associated with a call filter."""

    service = "confd"
    name = "call_filter_surrogate_users_associated"
    routing_key_fmt = "config.callfilters.surrogates.users.updated"

    def __init__(
        self,
        call_filter_id: int,
        users: list[str],
        tenant_uuid: UUIDStr,
    ) -> None:
        """Initialize event.

        Args:
            call_filter_id (int): The ID of the call filter.
            users (list[str]): A list of user UUIDs.
            tenant_uuid (UUIDStr): The UUID of the tenant.

        """
        content = {
            "call_filter_id": call_filter_id,
            "user_uuids": users,
        }
        super().__init__(content, tenant_uuid)
