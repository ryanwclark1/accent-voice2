# Copyright 2023 Accent Communications

from __future__ import annotations

from typing import Any

import requests
import requests.auth
from accent_lib_rest_client.client import BaseClient

from accent_auth_client.commands import (
    AdminCommand,
    BackendsCommand,
    ConfigCommand,
    EmailsCommand,
    ExternalAuthCommand,
    GroupsCommand,
    LDAPBackendConfigCommand,
    PoliciesCommand,
    RefreshTokenCommand,
    SAMLCommand,
    SAMLConfigCommand,
    SessionsCommand,
    StatusCommand,
    TenantsCommand,
    TokenCommand,
    UsersCommand,
)


class AuthClient(BaseClient):
    namespace = 'accent_auth_client.commands'

    admin: AdminCommand
    backends: BackendsCommand
    config: ConfigCommand
    emails: EmailsCommand
    external: ExternalAuthCommand
    groups: GroupsCommand
    ldap_config: LDAPBackendConfigCommand
    policies: PoliciesCommand
    refresh_tokens: RefreshTokenCommand
    saml: SAMLCommand
    saml_config: SAMLConfigCommand
    sessions: SessionsCommand
    status: StatusCommand
    tenants: TenantsCommand
    token: TokenCommand
    users: UsersCommand

    def __init__(
        self,
        host: str,
        port: int = 443,
        prefix: str | None = '/api/auth',
        version: str = '0.1',
        username: str | None = None,
        password: str | None = None,
        **kwargs: Any,
    ):
        kwargs.pop('key_file', None)
        kwargs.pop('master_tenant_uuid', None)
        super().__init__(host=host, port=port, prefix=prefix, version=version, **kwargs)
        self.username = username
        self.password = password

    def session(self) -> requests.Session:
        session = super().session()
        if self.username and self.password:
            session.auth = requests.auth.HTTPBasicAuth(
                self.username.encode("utf-8"), self.password.encode("utf-8")
            )
        return session
