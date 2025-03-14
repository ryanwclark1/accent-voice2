# resources/user/event.py
from typing import ClassVar

from pydantic import Field

from accent_bus.resources.common.event import TenantEvent, UserEvent


class _BaseUserEvent(TenantEvent):
    """Base class for user-related events."""

    service: ClassVar[str] = "confd"
    content: dict


class UserCreatedEvent(_BaseUserEvent):
    """Event for when a user is created."""

    name: ClassVar[str] = "user_created"
    routing_key_fmt: ClassVar[str] = "config.user.created"
    user_id: int = Field(..., alias="id")  # Keep original "id" field name
    user_uuid: str = Field(..., alias="uuid")  # Keep original "uuid"
    subscription_type: str
    created_at: str | None = None  # Optional, use explicit None

    def __init__(
        self,
        user_id: int,
        user_uuid: str,
        subscription_type: str,
        created_at: str | None,
        **data,
    ):
        content = {
            "id": int(user_id),
            "uuid": str(user_uuid),
            "subscription_type": subscription_type,
            "created_at": str(created_at) if created_at is not None else None,
            "tenant_uuid": str(data["tenant_uuid"]),
        }

        super().__init__(content=content, **data)


class UserDeletedEvent(_BaseUserEvent):
    """Event for when a user is deleted."""

    name: ClassVar[str] = "user_deleted"
    routing_key_fmt: ClassVar[str] = "config.user.deleted"
    user_id: int = Field(..., alias="id")  # Keep original "id" field name
    user_uuid: str = Field(..., alias="uuid")  # Keep original "uuid"
    subscription_type: str
    created_at: str | None = None  # Optional

    def __init__(
        self,
        user_id: int,
        user_uuid: str,
        subscription_type: str,
        created_at: str | None,
        **data,
    ):
        content = {
            "id": int(user_id),
            "uuid": str(user_uuid),
            "subscription_type": subscription_type,
            "created_at": str(created_at) if created_at is not None else None,
            "tenant_uuid": str(data["tenant_uuid"]),
        }
        super().__init__(content=content, **data)


class UserEditedEvent(_BaseUserEvent):
    """Event for when a user is edited."""

    name: ClassVar[str] = "user_edited"
    routing_key_fmt: ClassVar[str] = "config.user.edited"
    user_id: int = Field(..., alias="id")  # Keep original "id" field name
    user_uuid: str = Field(..., alias="uuid")  # Keep original "uuid"
    subscription_type: str
    created_at: str | None = None

    def __init__(
        self,
        user_id: int,
        user_uuid: str,
        subscription_type: str,
        created_at: str | None,
        **data,
    ):
        content = {
            "id": int(user_id),
            "uuid": str(user_uuid),
            "subscription_type": subscription_type,
            "created_at": str(created_at) if created_at is not None else None,
            "tenant_uuid": str(data["tenant_uuid"]),
        }

        super().__init__(content=content, **data)


class UserFallbackEditedEvent(UserEvent):
    """Event for user fallback is edited."""

    name: ClassVar[str] = "user_fallback_edited"
    routing_key_fmt: ClassVar[str] = "config.users.fallbacks.edited"
    service: ClassVar[str] = "confd"
    content: dict

    def __init__(
        self,
        user_id: int,
        **data,
    ):
        content = {
            "id": int(user_id),
            "uuid": str(data["user_uuid"]),
            "subscription_type": None,
            "created_at": None,
            "tenant_uuid": str(data["tenant_uuid"]),
        }
        super().__init__(content=content, **data)


class UserServiceEditedEvent(UserEvent):
    service: ClassVar[str] = "confd"
    name: ClassVar[str] = "users_services_{service_name}_updated"
    routing_key_fmt: ClassVar[str] = (
        "config.users.{user_uuid}.services.{service_name}.updated"
    )
    content: dict
    service_name: str

    def __init__(self, user_id: int, service_name: str, service_enabled: bool, **data):
        self.name = type(self).name.format(service_name=service_name)
        content = {
            "user_id": int(user_id),
            "user_uuid": str(data["user_uuid"]),
            "tenant_uuid": str(data["tenant_uuid"]),
            "enabled": service_enabled,
        }
        super().__init__(content=content, **data)
        self.service_name = service_name


class UserForwardEditedEvent(UserEvent):
    service: ClassVar[str] = "confd"
    name: ClassVar[str] = "users_forwards_{forward_name}_updated"
    routing_key_fmt: ClassVar[str] = (
        "config.users.{user_uuid}.forwards.{forward_name}.updated"
    )
    content: dict
    forward_name: str

    def __init__(
        self,
        user_id: int,
        forward_name: str,
        forward_enabled: bool,
        forward_dest: str,
        **data,
    ):
        self.name = type(self).name.format(forward_name=forward_name)
        content = {
            "user_id": int(user_id),
            "user_uuid": str(data["user_uuid"]),
            "tenant_uuid": str(data["tenant_uuid"]),
            "enabled": forward_enabled,
            "destination": forward_dest,
        }
        super().__init__(content=content, **data)
        self.forward_name = forward_name
