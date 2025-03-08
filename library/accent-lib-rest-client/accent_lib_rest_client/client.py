# Copyright 2024 Accent Communications

from __future__ import annotations

import logging
import os
import sys
from typing import Any, TypeVar
from uuid import UUID

import httpx
from stevedore import extension
from urllib3 import disable_warnings

from .models import ClientConfig, RequestParameters, TenantConfig, TokenConfig, URLConfig


logger = logging.getLogger(__name__)

T = TypeVar("T", bound="BaseClient")

global PLUGINS_CACHE
PLUGINS_CACHE: dict[str, list[extension.Extension]] = {}


class BaseClient:
    """Base REST client with modern features."""

    namespace: str | None = None

    def __init__(
        self,
        host: str,
        https: bool = True,
        port: int = 443,
        prefix: str | None = None,
        tenant_uuid: UUID | str | None = None,
        timeout: int = 10,
        token: str | None = None,
        user_agent: str = "",
        verify_certificate: bool = True,
        version: str = "",
        **kwargs: Any,
    ) -> None:
        """Initialize the REST client with validation."""
        # Convert string UUID to UUID object if necessary
        if isinstance(tenant_uuid, str):
            tenant_uuid = UUID(tenant_uuid)

        # Create and validate configuration
        self.config = ClientConfig(
            host=host,
            https=https,
            port=port,
            prefix=prefix,
            tenant_uuid=tenant_uuid,
            timeout=timeout,
            token=token,
            user_agent=user_agent or os.path.basename(sys.argv[0]),
            verify_certificate=verify_certificate,
            version=version,
        )

        # Initialize URL configuration
        self._url_config = URLConfig(
            scheme="https" if self.config.https else "http",
            host=self.config.host,
            port=self.config.port,
            prefix=self.config.prefix,
            version=self.config.version
        )

        # Initialize tenant and token configurations
        self._tenant_config = TenantConfig(tenant_uuid=tenant_uuid)
        self._token_config = TokenConfig(token=token) if token else None

        # Set internal state from validated config
        for key, value in self.config.model_dump().items():
            setattr(self, f"_{key}", value)

        if kwargs:
            logger.debug(
                "%s received unexpected arguments: %s",
                self.__class__.__name__,
                list(kwargs.keys()),
            )

        self._load_plugins()

    @property
    def tenant_uuid(self) -> UUID | None:
        """Get the current tenant UUID."""
        return self._tenant_config.tenant_uuid if self._tenant_config else None

    @tenant_uuid.setter
    def tenant_uuid(self, value: UUID | str | None) -> None:
        """Set the tenant UUID for subsequent requests."""
        if isinstance(value, str):
            value = UUID(value)

        if self._tenant_config is None:
            self._tenant_config = TenantConfig(tenant_uuid=value)
        else:
            self._tenant_config.tenant_uuid = value

    def set_token(self, token: str) -> None:
        """Set the authentication token for subsequent requests."""
        self._token_config = TokenConfig(token=token)
        self._token = token

    def session(self, parameters: RequestParameters | None = None) -> httpx.Client:
        """Create an HTTP client session with the current configuration."""
        headers = {"Connection": "close"}

        if self._token_config and self._token_config.token:
            headers["X-Auth-Token"] = self._token_config.token

        if self._tenant_config and self._tenant_config.tenant_uuid:
            headers["Accent-Tenant"] = str(self._tenant_config.tenant_uuid)

        if self._user_agent:
            headers["User-agent"] = self._user_agent

        verify = self._verify_certificate if self._https else False
        if not verify:
            disable_warnings()

        return httpx.Client(
            timeout=self._timeout,
            headers=headers,
            verify=verify,
            follow_redirects=True
        )

    def url(self, *fragments: str) -> str:
        """Build a complete URL for the API endpoint."""
        return self._url_config.build_url(*fragments)

    def is_server_reachable(self) -> bool:
        """Check if the server is reachable."""
        try:
            with self.session() as client:
                client.head(self.url())
            return True
        except httpx.HTTPStatusError:
            return True
        except httpx.RequestError as e:
            logger.debug("Server unreachable: %s", e)
            return False
