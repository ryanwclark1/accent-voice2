# Copyright 2023 Accent Communications

from __future__ import annotations

import logging
from typing import TypeVar

from accent_auth_client import Client as AuthClient
from flask import current_app, g
from werkzeug.local import LocalProxy

from accent.tenant_helpers import Token, User

from . import tenant_helpers

logger = logging.getLogger(__name__)


def get_auth_client() -> AuthClient:
    # NOTE: It's possible to inject its own client (ex: accent-auth)
    auth_client = g.get("auth_client")
    if not auth_client:
        auth_config = dict(current_app.config["auth"])
        auth_config.pop("username", None)
        auth_config.pop("password", None)
        auth_config.pop("key_file", None)
        auth_client = g.auth_client = AuthClient(**auth_config)
    return auth_client


auth_client: AuthClient = LocalProxy(get_auth_client)


def get_token() -> Token:
    token = g.get("token")
    if not token:
        if g.get("token_extractor"):
            _token = Token(g.token_extractor(), auth_client)
        else:
            _token = Token.from_headers(auth_client)
        token = g.token = _token
        auth_client.set_token(token.uuid)
    return token


token: Token = LocalProxy(get_token)  # type: ignore[assignment]


def get_user() -> User:
    user = g.get("user")
    if not user:
        user = g.user = User(token.user_uuid)
    return user


user: User = LocalProxy(get_user)  # type: ignore[assignment]

Self = TypeVar("Self", bound="Tenant")


class Tenant(tenant_helpers.Tenant):
    @classmethod
    def autodetect(cls: type[Self], include_query: bool = False) -> Self:
        tenant = None
        if include_query:
            try:
                tenant = cls.from_query()
            except tenant_helpers.InvalidTenant:
                logger.debug("Invalid tenant from query, using header...")
            else:
                logger.debug('Found tenant "%s" from query', tenant.uuid)

        if not tenant:
            try:
                tenant = cls.from_headers()
            except tenant_helpers.InvalidTenant:
                logger.debug("Invalid tenant from header, using token...")
            else:
                logger.debug('Found tenant "%s" from header', tenant.uuid)

        verified_tenant_uuid = g.get("verified_tenant_uuid")
        if verified_tenant_uuid and tenant and verified_tenant_uuid == tenant.uuid:
            logger.debug("Tenant already validated by Flask verify_token")
            return cls(uuid=tenant.uuid)

        if not tenant:
            tenant = cls.from_token(token)
            logger.debug('Found tenant "%s" from token', tenant.uuid)
            return tenant

        try:
            return tenant.check_against_token(token)
        except tenant_helpers.InvalidTenant:
            logger.debug("Tenant invalid against token")
            raise tenant_helpers.UnauthorizedTenant(tenant.uuid)
