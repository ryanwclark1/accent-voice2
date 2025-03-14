# resources/auth/events.py
from typing import ClassVar

from pydantic import BaseModel, UUID4, Field

from resources.common.event import TenantEvent, UserEvent
from .types import TenantDict


class AuthTenantEvent(TenantEvent):
    """Base class for auth tenant events."""

    service: ClassVar[str] = "auth"
    content: dict  # Will be replaced by specific models in subclasses


class TenantCreatedEvent(AuthTenantEvent):
    """Event for when a tenant is created."""

    name: ClassVar[str] = "auth_tenant_added"
    routing_key_fmt: ClassVar[str] = "auth.tenants.{tenant_uuid}.created"
    content: TenantDict  # Using the Pydantic model

    def __init__(self, tenant_data: TenantDict, **data):
        super().__init__(content=tenant_data.model_dump(), **data)


class TenantContent(BaseModel):
    """
    Content for tenant update.

    Attributes:
        uuid (UUID4): The tenant UUID.
        name (str): The tenant name.
    """

    uuid: UUID4
    name: str


class TenantUpdatedEvent(AuthTenantEvent):
    """Event for when a tenant is updated."""

    name: ClassVar[str] = "auth_tenant_updated"
    routing_key_fmt: ClassVar[str] = "auth.tenants.{tenant_uuid}.updated"
    content: TenantContent

    def __init__(self, name: str, **data):
        content = TenantContent(uuid=data["tenant_uuid"], name=name)
        super().__init__(content=content.model_dump(), **data)


class TenantDeletedContent(BaseModel):
    """
    Content for tenant deletion.
    Attributes:
        uuid (UUID4): The tenant UUID.
    """

    uuid: UUID4


class TenantDeletedEvent(AuthTenantEvent):
    """Event for when a tenant is deleted."""

    name: ClassVar[str] = "auth_tenant_deleted"
    routing_key_fmt: ClassVar[str] = "auth.tenants.{tenant_uuid}.deleted"
    content: TenantDeletedContent

    def __init__(self, **data):
        content = TenantDeletedContent(uuid=data["tenant_uuid"])
        super().__init__(content=content.model_dump(), **data)


class AuthUserEvent(UserEvent):
    """Base class for Auth User Events."""

    service: ClassVar[str] = "auth"
    content: dict  # Will be replaced in subclasses


class ExternalAuthContent(BaseModel):
    """
    Content for external auth events.
    Attributes:
        user_uuid (str): UUID of the user.
        external_auth_name (str): External auth provider name.
    """

    user_uuid: str
    external_auth_name: str


class UserExternalAuthAddedEvent(AuthUserEvent):
    """Event for when an external auth is added to a user."""

    name: ClassVar[str] = "auth_user_external_auth_added"
    routing_key_fmt: ClassVar[str] = (
        "auth.users.{user_uuid}.external.{external_auth_name}.created"
    )
    content: ExternalAuthContent

    def __init__(self, external_auth_name: str, **data):
        content = ExternalAuthContent(
            user_uuid=str(data["user_uuid"]), external_auth_name=external_auth_name
        )
        super().__init__(content=content.model_dump(), **data)


class UserExternalAuthAuthorizedEvent(AuthUserEvent):
    """Event for when a user is authorized by an external auth."""

    name: ClassVar[str] = "auth_user_external_auth_authorized"
    routing_key_fmt: ClassVar[str] = (
        "auth.users.{user_uuid}.external.{external_auth_name}.authorized"
    )
    content: ExternalAuthContent

    def __init__(self, external_auth_name: str, **data):
        content = ExternalAuthContent(
            user_uuid=str(data["user_uuid"]), external_auth_name=external_auth_name
        )
        super().__init__(content=content.model_dump(), **data)


class UserExternalAuthDeletedEvent(AuthUserEvent):
    """Event for when an external auth is deleted for a user."""

    name: ClassVar[str] = "auth_user_external_auth_deleted"
    routing_key_fmt: ClassVar[str] = (
        "auth.users.{user_uuid}.external.{external_auth_name}.deleted"
    )
    content: ExternalAuthContent

    def __init__(self, external_auth_name: str, **data):
        content = ExternalAuthContent(
            user_uuid=str(data["user_uuid"]), external_auth_name=external_auth_name
        )
        super().__init__(content=content.model_dump(), **data)


class RefreshTokenContent(BaseModel):
    """
    Content for refresh token events.
    Attributes:
        client_id (str): Client id.
        mobile (bool): If mobile.
        user_uuid (str): User UUID.
        tenant_uuid (str): Tenant UUID.
    """

    client_id: str
    mobile: bool
    user_uuid: str
    tenant_uuid: str


class RefreshTokenCreatedEvent(AuthUserEvent):
    """Event for when a refresh token is created."""

    name: ClassVar[str] = "auth_refresh_token_created"
    routing_key_fmt: ClassVar[str] = "auth.users.{user_uuid}.tokens.{client_id}.created"
    content: RefreshTokenContent

    def __init__(self, client_id: str, is_mobile: bool, **data):
        content = RefreshTokenContent(
            client_id=client_id,
            mobile=bool(is_mobile),
            user_uuid=str(data["user_uuid"]),
            tenant_uuid=str(data["tenant_uuid"]),
        )
        super().__init__(content=content.model_dump(), **data)


class RefreshTokenDeletedEvent(AuthUserEvent):
    """Event for when a refresh token is deleted."""

    name: ClassVar[str] = "auth_refresh_token_deleted"
    routing_key_fmt: ClassVar[str] = "auth.users.{user_uuid}.tokens.{client_id}.deleted"
    content: RefreshTokenContent

    def __init__(self, client_id: str, is_mobile: bool, **data):
        content = RefreshTokenContent(
            client_id=client_id,
            mobile=bool(is_mobile),
            user_uuid=str(data["user_uuid"]),
            tenant_uuid=str(data["tenant_uuid"]),
        )
        super().__init__(content=content.model_dump(), **data)


class SessionContent(BaseModel):
    """
    Content for Session events.
    Attributes:
        uuid (str): The session UUID.
        tenant_uuid (str): Tenant UUID.
        user_uuid (str): User UUID.
        mobile (bool): If mobile.
    """

    uuid: str
    tenant_uuid: str
    user_uuid: str
    mobile: bool


class SessionCreatedEvent(AuthUserEvent):
    """Event for when a session is created."""

    name: ClassVar[str] = "auth_session_created"
    routing_key_fmt: ClassVar[str] = "auth.sessions.{session_uuid}.created"
    content: SessionContent
    session_uuid: str  # Required by routing_key_fmt

    def __init__(self, session_uuid: UUID4, is_mobile: bool, **data):
        content = SessionContent(
            uuid=str(session_uuid),
            tenant_uuid=str(data["tenant_uuid"]),
            user_uuid=str(data["user_uuid"]),
            mobile=bool(is_mobile),
        )
        super().__init__(content=content.model_dump(), **data)
        self.session_uuid = str(session_uuid)


class SessionDeletedEvent(AuthUserEvent):
    """Event for when a session is deleted."""

    name: ClassVar[str] = "auth_session_deleted"
    routing_key_fmt: ClassVar[str] = "auth.sessions.{session_uuid}.deleted"
    content: SessionContent
    session_uuid: str  # Required by routing_key_fmt

    def __init__(self, session_uuid: UUID4, **data):
        content = SessionContent(
            uuid=str(session_uuid),
            user_uuid=str(data["user_uuid"]),
            tenant_uuid=str(data["tenant_uuid"]),
            mobile=False,  # Not on this event, avoid key error
        )
        super().__init__(content=content.model_dump(), **data)
        self.session_uuid = str(session_uuid)


class SessionExpireSoonContent(BaseModel):
    """
    Content for Session Expiration Events.

    Attributes:
        uuid (str): Session UUID.
        user_uuid (str): User UUID.
        tenant_uuid (str): Tenant UUID.
    """

    uuid: str
    user_uuid: str
    tenant_uuid: str


class SessionExpireSoonEvent(AuthUserEvent):
    """Event for when a session is about to expire."""

    name: ClassVar[str] = "auth_session_expire_soon"
    routing_key_fmt: ClassVar[str] = (
        "auth.users.{user_uuid}.sessions.{session_uuid}.expire_soon"
    )
    content: SessionExpireSoonContent
    session_uuid: str  # Required by routing_key_fmt

    def __init__(self, session_uuid: UUID4, **data):
        content = SessionExpireSoonContent(
            uuid=str(session_uuid),
            user_uuid=str(data["user_uuid"]),
            tenant_uuid=str(data["tenant_uuid"]),
        )
        super().__init__(content=content.model_dump(), **data)
        self.session_uuid = str(session_uuid)
