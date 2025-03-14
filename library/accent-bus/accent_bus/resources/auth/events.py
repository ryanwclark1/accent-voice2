# accent_bus/resources/auth/events.py
# Copyright 2025 Accent Communications

"""Auth events."""

from accent_bus.resources.common.event import TenantEvent, UserEvent
from accent_bus.resources.common.types import UUIDStr

from .types import TenantDict


class TenantCreatedEvent(TenantEvent):
    """Event for when a tenant is created."""

    service = "auth"
    name = "auth_tenant_added"
    routing_key_fmt = "auth.tenants.{tenant_uuid}.created"

    def __init__(self, tenant_data: TenantDict, tenant_uuid: UUIDStr) -> None:
        """Initialize the event.

        Args:
           tenant_data: Tenant data
           tenant_uuid: tenant UUID

        """
        super().__init__(tenant_data, tenant_uuid)


class TenantUpdatedEvent(TenantEvent):
    """Event for when a tenant is updated."""

    service = "auth"
    name = "auth_tenant_updated"
    routing_key_fmt = "auth.tenants.{tenant_uuid}.updated"

    def __init__(self, name: str, tenant_uuid: UUIDStr) -> None:
        """Initialize the event.

        Args:
           name:  tenant name
           tenant_uuid: tenant UUID

        """
        content = {"uuid": tenant_uuid, "name": name}
        super().__init__(content, tenant_uuid)


class TenantDeletedEvent(TenantEvent):
    """Event for when a tenant is deleted."""

    service = "auth"
    name = "auth_tenant_deleted"
    routing_key_fmt = "auth.tenants.{tenant_uuid}.deleted"

    def __init__(self, tenant_uuid: UUIDStr) -> None:
        """Initialize the event.

        Args:
           tenant_uuid (UUIDStr): tenant UUID

        """
        content = {"uuid": tenant_uuid}
        super().__init__(content, tenant_uuid)


class UserExternalAuthAddedEvent(UserEvent):
    """Event for when external auth is added to a user."""

    service = "auth"
    name = "auth_user_external_auth_added"
    routing_key_fmt = "auth.users.{user_uuid}.external.{external_auth_name}.created"

    def __init__(
        self,
        external_auth_name: str,
        tenant_uuid: UUIDStr,
        user_uuid: UUIDStr,
    ) -> None:
        """Initialize the event.

        Args:
            external_auth_name (str): The name of the external auth provider.
            tenant_uuid (UUIDStr): The tenant UUID.
            user_uuid (UUIDStr): The user UUID.

        """
        content = {"user_uuid": user_uuid, "external_auth_name": external_auth_name}
        super().__init__(content, tenant_uuid, user_uuid)


class UserExternalAuthAuthorizedEvent(UserEvent):
    """Event for when a user is authorized via external auth."""

    service = "auth"
    name = "auth_user_external_auth_authorized"
    routing_key_fmt = "auth.users.{user_uuid}.external.{external_auth_name}.authorized"

    def __init__(
        self,
        external_auth_name: str,
        tenant_uuid: UUIDStr,
        user_uuid: UUIDStr,
    ) -> None:
        """Initialize event.

        Args:
            external_auth_name: The name of the external auth provider.
            tenant_uuid: The tenant UUID.
            user_uuid: The user UUID.

        """
        content = {"user_uuid": user_uuid, "external_auth_name": external_auth_name}
        super().__init__(content, tenant_uuid, user_uuid)


class UserExternalAuthDeletedEvent(UserEvent):
    """Event for when external auth is deleted for a user."""

    service = "auth"
    name = "auth_user_external_auth_deleted"
    routing_key_fmt = "auth.users.{user_uuid}.external.{external_auth_name}.deleted"

    def __init__(
        self,
        external_auth_name: str,
        tenant_uuid: UUIDStr,
        user_uuid: UUIDStr,
    ) -> None:
        """Initialize the event.

        Args:
            external_auth_name (str): external auth provider
            tenant_uuid (UUIDStr): tenant UUID
            user_uuid (UUIDStr): user UUID

        """
        content = {"user_uuid": user_uuid, "external_auth_name": external_auth_name}
        super().__init__(content, tenant_uuid, user_uuid)


class RefreshTokenCreatedEvent(UserEvent):
    """Event for when a refresh token is created."""

    service = "auth"
    name = "auth_refresh_token_created"
    routing_key_fmt = "auth.users.{user_uuid}.tokens.{client_id}.created"

    def __init__(
        self,
        client_id: str,
        is_mobile: bool,
        tenant_uuid: UUIDStr,
        user_uuid: UUIDStr,
    ) -> None:
        """Initialize the event.

        Args:
           client_id: Client ID
           is_mobile: if it is mobile
           tenant_uuid: tenant UUID
           user_uuid: user UUID

        """
        content = {
            "client_id": client_id,
            "mobile": bool(is_mobile),
            "user_uuid": user_uuid,
            "tenant_uuid": tenant_uuid,
        }
        super().__init__(content, tenant_uuid, user_uuid)


class RefreshTokenDeletedEvent(UserEvent):
    """Event for when a refresh token is deleted."""

    service = "auth"
    name = "auth_refresh_token_deleted"
    routing_key_fmt = "auth.users.{user_uuid}.tokens.{client_id}.deleted"

    def __init__(
        self,
        client_id: str,
        is_mobile: bool,
        tenant_uuid: UUIDStr,
        user_uuid: UUIDStr,
    ) -> None:
        """Initialize event.

        Args:
           client_id: client id
           is_mobile: mobile
            tenant_uuid: tenant UUID
           user_uuid: user UUID

        """
        content = {
            "client_id": client_id,
            "mobile": bool(is_mobile),
            "user_uuid": user_uuid,
            "tenant_uuid": tenant_uuid,
        }
        super().__init__(content, tenant_uuid, user_uuid)


class SessionCreatedEvent(UserEvent):
    """Event for when a session is created."""

    service = "auth"
    name = "auth_session_created"
    routing_key_fmt = "auth.sessions.{session_uuid}.created"

    def __init__(
        self,
        session_uuid: UUIDStr,
        is_mobile: bool,
        tenant_uuid: UUIDStr,
        user_uuid: UUIDStr,
    ) -> None:
        """Initialize Event.

        Args:
            session_uuid (UUIDStr): Session UUID.
            is_mobile (bool):  mobile
            tenant_uuid (UUIDStr): tenant UUID
            user_uuid (UUIDStr): user UUID

        """
        content = {
            "uuid": session_uuid,
            "tenant_uuid": tenant_uuid,
            "user_uuid": user_uuid,
            "mobile": bool(is_mobile),
        }
        super().__init__(content, tenant_uuid, user_uuid)
        self.session_uuid = str(session_uuid)


class SessionDeletedEvent(UserEvent):
    """Event for when a session is deleted."""

    service = "auth"
    name = "auth_session_deleted"
    routing_key_fmt = "auth.sessions.{session_uuid}.deleted"

    def __init__(
        self,
        session_uuid: UUIDStr,
        tenant_uuid: UUIDStr,
        user_uuid: UUIDStr,
    ) -> None:
        """Initialize the event.

        Args:
            session_uuid (UUIDStr): session UUID
            tenant_uuid (UUIDStr): tenant UUID
            user_uuid (UUIDStr): user UUID

        """
        content = {
            "uuid": session_uuid,
            "user_uuid": user_uuid,
            "tenant_uuid": tenant_uuid,
        }
        super().__init__(content, tenant_uuid, user_uuid)
        self.session_uuid = str(session_uuid)


class SessionExpireSoonEvent(UserEvent):
    """Event for when a session is about to expire."""

    service = "auth"
    name = "auth_session_expire_soon"
    routing_key_fmt = "auth.users.{user_uuid}.sessions.{session_uuid}.expire_soon"

    def __init__(
        self,
        session_uuid: UUIDStr,
        tenant_uuid: UUIDStr,
        user_uuid: UUIDStr,
    ) -> None:
        """Initialize the event.

        Args:
           session_uuid (UUIDStr): session UUID
           tenant_uuid (UUIDStr): tenant UUID
           user_uuid (UUIDStr): user UUID

        """
        content = {
            "uuid": session_uuid,
            "user_uuid": user_uuid,
            "tenant_uuid": tenant_uuid,
        }
        super().__init__(content, tenant_uuid, user_uuid)
        self.session_uuid = str(session_uuid)
