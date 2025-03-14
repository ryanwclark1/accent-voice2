# accent_bus/resources/user/event.py
# Copyright 2025 Accent Communications

"""User events."""

from __future__ import annotations

from typing import TYPE_CHECKING

from accent_bus.resources.common.event import TenantEvent, UserEvent

if TYPE_CHECKING:
    from accent_bus.resources.common.types import UUIDStr


class _BaseUserEvent(TenantEvent):
    """Base class for user events."""

    def __init__(
        self,
        user_id: int,
        user_uuid: UUIDStr,
        subscription_type: str,
        created_at: str | None,
        tenant_uuid: UUIDStr,
    ) -> None:
        """Initialize BaseUserEvent.

        Args:
            user_id: User ID
            user_uuid: User UUID
            subscription_type: Subscription Type
            created_at: Creation timestamp
            tenant_uuid: tenant UUID

        """
        content = {
            "id": int(user_id),
            "uuid": str(user_uuid),
            "subscription_type": subscription_type,
            "created_at": str(created_at) if created_at is not None else None,
            "tenant_uuid": str(tenant_uuid),
        }
        super().__init__(content, tenant_uuid)


class UserCreatedEvent(_BaseUserEvent):
    """Event for when a user is created."""

    service = "confd"
    name = "user_created"
    routing_key_fmt = "config.user.created"


class UserDeletedEvent(_BaseUserEvent):
    """Event for when a user is deleted."""

    service = "confd"
    name = "user_deleted"
    routing_key_fmt = "config.user.deleted"


class UserEditedEvent(_BaseUserEvent):
    """Event for when a user is edited."""

    service = "confd"
    name = "user_edited"
    routing_key_fmt = "config.user.edited"


class UserFallbackEditedEvent(UserEvent):
    """Event for when a user fallback is edited."""

    service = "confd"
    name = "user_fallback_edited"
    routing_key_fmt = "config.users.fallbacks.edited"

    def __init__(
        self,
        user_id: int,
        tenant_uuid: UUIDStr,
        user_uuid: UUIDStr,
    ) -> None:
        """Initialize event.

        Args:
          user_id: User ID
          tenant_uuid: tenant UUID
          user_uuid: user UUID

        """
        content = {
            "id": int(user_id),
            "uuid": str(user_uuid),
            "subscription_type": None,
            "created_at": None,
            "tenant_uuid": str(tenant_uuid),
        }
        super().__init__(content, tenant_uuid, user_uuid)


class UserServiceEditedEvent(UserEvent):
    """Event for when a user service is edited."""

    service = "confd"
    name = "users_services_{service_name}_updated"
    routing_key_fmt = "config.users.{user_uuid}.services.{service_name}.updated"

    def __init__(
        self,
        user_id: int,
        service_name: str,
        service_enabled: bool,
        tenant_uuid: UUIDStr,
        user_uuid: UUIDStr,
    ) -> None:
        """Initialize event.

        Args:
            user_id: User ID
            service_name: Service Name
            service_enabled: service enabled
            tenant_uuid: tenant UUID
            user_uuid: user UUID

        """
        self.name = type(self).name.format(service_name=service_name)
        content = {
            "user_id": int(user_id),
            "user_uuid": str(user_uuid),
            "tenant_uuid": str(tenant_uuid),
            "enabled": service_enabled,
        }
        super().__init__(content, tenant_uuid, user_uuid)
        self.service_name = service_name


class UserForwardEditedEvent(UserEvent):
    """Event for when a user forward is edited."""

    service = "confd"
    name = "users_forwards_{forward_name}_updated"
    routing_key_fmt = "config.users.{user_uuid}.forwards.{forward_name}.updated"

    def __init__(
        self,
        user_id: int,
        forward_name: str,
        forward_enabled: bool,
        forward_dest: str,
        tenant_uuid: UUIDStr,
        user_uuid: UUIDStr,
    ) -> None:
        """Initialize event.

        Args:
          user_id: User ID
          forward_name: Forward Name
          forward_enabled:  forward enabled
          forward_dest:  forward destination
          tenant_uuid: tenant UUID
          user_uuid: user UUID

        """
        self.name = type(self).name.format(forward_name=forward_name)
        content = {
            "user_id": int(user_id),
            "user_uuid": str(user_uuid),
            "tenant_uuid": str(tenant_uuid),
            "enabled": forward_enabled,
            "destination": forward_dest,
        }
        super().__init__(content, tenant_uuid, user_uuid)
        self.forward_name = forward_name
