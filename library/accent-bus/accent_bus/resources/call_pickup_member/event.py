# resources/call_pickup_member/event.py
from typing import ClassVar

from accent_bus.resources.common.event import TenantEvent


class CallPickupMemberEvent(TenantEvent):
    """Base class for Call Pickup Member events."""

    service: ClassVar[str] = "confd"
    content: dict


class CallPickupInterceptorUsersAssociatedEvent(CallPickupMemberEvent):
    """Event for when interceptor users are associated with a call pickup."""

    name: ClassVar[str] = "call_pickup_interceptor_users_associated"
    routing_key_fmt: ClassVar[str] = "config.callpickups.interceptors.users.updated"

    def __init__(self, call_pickup_id: int, users: list[str], **data):
        content = {
            "call_pickup_id": call_pickup_id,
            "user_uuids": users,
        }
        super().__init__(content=content, **data)


class CallPickupTargetUsersAssociatedEvent(CallPickupMemberEvent):
    """Event for when target users are associated with a call pickup."""

    name: ClassVar[str] = "call_pickup_target_users_associated"
    routing_key_fmt: ClassVar[str] = "config.callpickups.targets.users.updated"

    def __init__(self, call_pickup_id: int, users: list[str], **data):
        content = {
            "call_pickup_id": call_pickup_id,
            "user_uuids": users,
        }
        super().__init__(content=content, **data)


class CallPickupInterceptorGroupsAssociatedEvent(CallPickupMemberEvent):
    """Event for when interceptor groups are associated."""

    name: ClassVar[str] = "call_pickup_interceptor_groups_associated"
    routing_key_fmt: ClassVar[str] = "config.callpickups.interceptors.groups.updated"

    def __init__(self, call_pickup_id: int, group_ids: list[int], **data):
        content = {
            "call_pickup_id": call_pickup_id,
            "group_ids": group_ids,
        }
        super().__init__(content=content, **data)


class CallPickupTargetGroupsAssociatedEvent(CallPickupMemberEvent):
    """Event for when target groups are associated."""

    name: ClassVar[str] = "call_pickup_target_groups_associated"
    routing_key_fmt: ClassVar[str] = "config.callpickups.targets.groups.updated"

    def __init__(self, call_pickup_id: int, group_ids: list[int], **data):
        content = {
            "call_pickup_id": call_pickup_id,
            "group_ids": group_ids,
        }
        super().__init__(content=content, **data)
