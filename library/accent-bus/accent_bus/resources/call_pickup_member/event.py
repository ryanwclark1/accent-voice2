# accent_bus/resources/call_pickup_member/event.py
# Copyright 2025 Accent Communications

"""Call pickup member events."""

from accent_bus.resources.common.event import TenantEvent
from accent_bus.resources.common.types import UUIDStr


class CallPickupInterceptorUsersAssociatedEvent(TenantEvent):
    """Event for when interceptor users are associated with a call pickup."""

    service = "confd"
    name = "call_pickup_interceptor_users_associated"
    routing_key_fmt = "config.callpickups.interceptors.users.updated"

    def __init__(
        self,
        call_pickup_id: int,
        users: list[str],
        tenant_uuid: UUIDStr,
    ) -> None:
        """Initialize the event.

        Args:
           call_pickup_id: Call Pickup ID
           users: List of User UUID
           tenant_uuid:  tenant UUID

        """
        content = {
            "call_pickup_id": call_pickup_id,
            "user_uuids": users,
        }
        super().__init__(content, tenant_uuid)


class CallPickupTargetUsersAssociatedEvent(TenantEvent):
    """Event for when target users are associated with a call pickup."""

    service = "confd"
    name = "call_pickup_target_users_associated"
    routing_key_fmt = "config.callpickups.targets.users.updated"

    def __init__(
        self,
        call_pickup_id: int,
        users: list[str],
        tenant_uuid: UUIDStr,
    ) -> None:
        """Initialize Event.

        Args:
          call_pickup_id: Call Pickup ID
          users: List of User UUID
          tenant_uuid: tenant UUID

        """
        content = {
            "call_pickup_id": call_pickup_id,
            "user_uuids": users,
        }
        super().__init__(content, tenant_uuid)


class CallPickupInterceptorGroupsAssociatedEvent(TenantEvent):
    """Event for when interceptor groups are associated with a call pickup."""

    service = "confd"
    name = "call_pickup_interceptor_groups_associated"
    routing_key_fmt = "config.callpickups.interceptors.groups.updated"

    def __init__(
        self,
        call_pickup_id: int,
        group_ids: list[int],
        tenant_uuid: UUIDStr,
    ) -> None:
        """Initialize event.

        Args:
           call_pickup_id: Call Pickup ID
           group_ids: List of Group ID
           tenant_uuid: tenant UUID

        """
        content = {
            "call_pickup_id": call_pickup_id,
            "group_ids": group_ids,
        }
        super().__init__(content, tenant_uuid)


class CallPickupTargetGroupsAssociatedEvent(TenantEvent):
    """Event for when target groups are associated with a call pickup."""

    service = "confd"
    name = "call_pickup_target_groups_associated"
    routing_key_fmt = "config.callpickups.targets.groups.updated"

    def __init__(
        self,
        call_pickup_id: int,
        group_ids: list[int],
        tenant_uuid: UUIDStr,
    ) -> None:
        """Initialize Event.

        Args:
          call_pickup_id: Call Pickup ID
          group_ids: List of Group ID
          tenant_uuid: tenant UUID

        """
        content = {
            "call_pickup_id": call_pickup_id,
            "group_ids": group_ids,
        }
        super().__init__(content, tenant_uuid)
