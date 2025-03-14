# Copyright 2023 Accent Communications

from ..common.event import TenantEvent, UserEvent
from ..common.types import UUIDStr
from .types import TenantDict


class TenantCreatedEvent(TenantEvent):
    service = 'auth'
    name = 'auth_tenant_added'
    routing_key_fmt = 'auth.tenants.{tenant_uuid}.created'

    def __init__(self, tenant_data: TenantDict, tenant_uuid: UUIDStr):
        super().__init__(tenant_data, tenant_uuid)


class TenantUpdatedEvent(TenantEvent):
    service = 'auth'
    name = 'auth_tenant_updated'
    routing_key_fmt = 'auth.tenants.{tenant_uuid}.updated'

    def __init__(self, name: str, tenant_uuid: UUIDStr):
        content = {'uuid': tenant_uuid, 'name': name}
        super().__init__(content, tenant_uuid)


class TenantDeletedEvent(TenantEvent):
    service = 'auth'
    name = 'auth_tenant_deleted'
    routing_key_fmt = 'auth.tenants.{tenant_uuid}.deleted'

    def __init__(self, tenant_uuid: UUIDStr):
        content = {'uuid': tenant_uuid}
        super().__init__(content, tenant_uuid)


class UserExternalAuthAddedEvent(UserEvent):
    service = 'auth'
    name = 'auth_user_external_auth_added'
    routing_key_fmt = 'auth.users.{user_uuid}.external.{external_auth_name}.created'

    def __init__(
        self,
        external_auth_name: str,
        tenant_uuid: UUIDStr,
        user_uuid: UUIDStr,
    ):
        content = {'user_uuid': user_uuid, 'external_auth_name': external_auth_name}
        super().__init__(content, tenant_uuid, user_uuid)


class UserExternalAuthAuthorizedEvent(UserEvent):
    service = 'auth'
    name = 'auth_user_external_auth_authorized'
    routing_key_fmt = 'auth.users.{user_uuid}.external.{external_auth_name}.authorized'

    def __init__(
        self,
        external_auth_name: str,
        tenant_uuid: UUIDStr,
        user_uuid: UUIDStr,
    ):
        content = {'user_uuid': user_uuid, 'external_auth_name': external_auth_name}
        super().__init__(content, tenant_uuid, user_uuid)


class UserExternalAuthDeletedEvent(UserEvent):
    service = 'auth'
    name = 'auth_user_external_auth_deleted'
    routing_key_fmt = 'auth.users.{user_uuid}.external.{external_auth_name}.deleted'

    def __init__(
        self,
        external_auth_name: str,
        tenant_uuid: UUIDStr,
        user_uuid: UUIDStr,
    ):
        content = {'user_uuid': user_uuid, 'external_auth_name': external_auth_name}
        super().__init__(content, tenant_uuid, user_uuid)


class RefreshTokenCreatedEvent(UserEvent):
    service = 'auth'
    name = 'auth_refresh_token_created'
    routing_key_fmt = 'auth.users.{user_uuid}.tokens.{client_id}.created'

    def __init__(
        self,
        client_id: str,
        is_mobile: bool,
        tenant_uuid: UUIDStr,
        user_uuid: UUIDStr,
    ):
        content = {
            'client_id': client_id,
            'mobile': bool(is_mobile),
            'user_uuid': user_uuid,
            'tenant_uuid': tenant_uuid,
        }
        super().__init__(content, tenant_uuid, user_uuid)


class RefreshTokenDeletedEvent(UserEvent):
    service = 'auth'
    name = 'auth_refresh_token_deleted'
    routing_key_fmt = 'auth.users.{user_uuid}.tokens.{client_id}.deleted'

    def __init__(
        self,
        client_id: str,
        is_mobile: bool,
        tenant_uuid: UUIDStr,
        user_uuid: UUIDStr,
    ):
        content = {
            'client_id': client_id,
            'mobile': bool(is_mobile),
            'user_uuid': user_uuid,
            'tenant_uuid': tenant_uuid,
        }
        super().__init__(content, tenant_uuid, user_uuid)


class SessionCreatedEvent(UserEvent):
    service = 'auth'
    name = 'auth_session_created'
    routing_key_fmt = 'auth.sessions.{session_uuid}.created'

    def __init__(
        self,
        session_uuid: UUIDStr,
        is_mobile: bool,
        tenant_uuid: UUIDStr,
        user_uuid: UUIDStr,
    ):
        content = {
            'uuid': session_uuid,
            'tenant_uuid': tenant_uuid,
            'user_uuid': user_uuid,
            'mobile': bool(is_mobile),
        }
        super().__init__(content, tenant_uuid, user_uuid)
        self.session_uuid = str(session_uuid)


class SessionDeletedEvent(UserEvent):
    service = 'auth'
    name = 'auth_session_deleted'
    routing_key_fmt = 'auth.sessions.{session_uuid}.deleted'

    def __init__(
        self,
        session_uuid: UUIDStr,
        tenant_uuid: UUIDStr,
        user_uuid: UUIDStr,
    ):
        content = {
            'uuid': session_uuid,
            'user_uuid': user_uuid,
            'tenant_uuid': tenant_uuid,
        }
        super().__init__(content, tenant_uuid, user_uuid)
        self.session_uuid = str(session_uuid)


class SessionExpireSoonEvent(UserEvent):
    service = 'auth'
    name = 'auth_session_expire_soon'
    routing_key_fmt = 'auth.users.{user_uuid}.sessions.{session_uuid}.expire_soon'

    def __init__(
        self,
        session_uuid: UUIDStr,
        tenant_uuid: UUIDStr,
        user_uuid: UUIDStr,
    ):
        content = {
            'uuid': session_uuid,
            'user_uuid': user_uuid,
            'tenant_uuid': tenant_uuid,
        }
        super().__init__(content, tenant_uuid, user_uuid)
        self.session_uuid = str(session_uuid)
