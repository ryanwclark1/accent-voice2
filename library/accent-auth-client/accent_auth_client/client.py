# Copyright 2025 Accent Communications

from __future__ import annotations

import logging
from typing import Any, ClassVar

import httpx
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

logger = logging.getLogger(__name__)


class AuthClient(BaseClient):
    """Authentication client for Accent API interactions.

    Provides access to various authentication-related commands.
    """

    namespace: ClassVar[str] = "accent_auth_client.commands"

    # Command attributes for type hints
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
        prefix: str | None = "/api/auth",
        version: str = "0.1",
        username: str | None = None,
        password: str | None = None,
        **kwargs: Any,
    ) -> None:
        """Initialize the authentication client.

        Args:
            host: Hostname or IP of the server
            port: Port number for the server (default: 443)
            prefix: URL prefix path (default: '/api/auth')
            version: API version string (default: '0.1')
            username: Username for basic authentication
            password: Password for basic authentication
            **kwargs: Additional arguments passed to the base client

        """
        # Remove deprecated arguments
        kwargs.pop("key_file", None)
        kwargs.pop("master_tenant_uuid", None)

        super().__init__(host=host, port=port, prefix=prefix, version=version, **kwargs)
        self.username = username
        self.password = password

        logger.info("Initialized Auth client for host: %s, port: %s", host, port)

    @property
    def sync_client(self) -> httpx.Client:
        """Get or create a synchronized HTTP client with authentication.

        Returns:
            Configured httpx.Client instance with authentication if credentials provided

        """
        client = super().sync_client

        # Add basic auth if credentials are provided
        if self.username and self.password:
            auth = httpx.BasicAuth(username=self.username, password=self.password)
            client.auth = auth

        return client

    @property
    def async_client(self) -> httpx.AsyncClient:
        """Get or create an asynchronous HTTP client with authentication.

        Returns:
            Configured httpx.AsyncClient instance with authentication if credentials provided

        """
        client = super().async_client

        # Add basic auth if credentials are provided
        if self.username and self.password:
            auth = httpx.BasicAuth(username=self.username, password=self.password)
            client.auth = auth

        return client

    # For backwards compatibility
    def session(self) -> httpx.Client:
        """Get a synchronized HTTP client (compatibility method).

        Returns:
            Configured httpx.Client instance

        Deprecated:
            Use sync_client property instead

        """
        logger.warning(
            "Deprecated method 'session()' called. Use 'sync_client' instead"
        )
        return self.sync_client
