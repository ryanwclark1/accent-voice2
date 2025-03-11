# Copyright 2025 Accent Communications

from __future__ import annotations

import logging
import sys
from functools import lru_cache
from pathlib import Path
from typing import (
    Any,
    ClassVar,
    TypeVar,
)

import httpx
from stevedore import extension

from accent_lib_rest_client.exceptions import InvalidArgumentError
from accent_lib_rest_client.models import ClientConfig

# Configure standard logging
logger = logging.getLogger(__name__)
# T = TypeVar("T")
T = TypeVar("T", httpx.Client, httpx.AsyncClient)

# Global cache for plugins
PLUGINS_CACHE: dict[str, list[extension.Extension]] = {}


class BaseClient:
    """Base client for API interactions.

    This class handles connection configuration, session management,
    and command loading from plugins.
    """

    namespace: ClassVar[str | None] = None
    _url_fmt = "{scheme}://{host}{port}{prefix}{version}"

    def __init__(
        self,
        host: str,
        port: int | None = None,
        version: str = "",
        token: str | None = None,
        tenant_uuid: str | None = None,
        https: bool = True,
        timeout: float = 10.0,
        verify_certificate: bool | str = True,
        prefix: str | None = None,
        user_agent: str = "",
        max_retries: int = 3,
        retry_delay: float = 1.0,
        **kwargs: Any,
    ) -> None:
        """Initialize a new API client.

        Args:
            host: Hostname or IP of the server
            port: Port number for the server
            version: API version string
            token: Authentication token
            tenant_uuid: Tenant identifier
            https: Whether to use HTTPS
            timeout: Request timeout in seconds
            verify_certificate: Whether to verify SSL certificates or path to a CA bundle
            prefix: URL prefix path
            user_agent: User agent string for requests
            max_retries: Maximum number of retries for requests
            retry_delay: Delay between retries in seconds
            **kwargs: Additional arguments (will be logged but not used)

        Raises:
            InvalidArgumentError: If host is empty

        """
        if not host:
            raise InvalidArgumentError("host")

        if not user_agent:
            user_agent = Path(sys.argv[0]).name

        self.config = ClientConfig(
            host=host,
            port=port,
            version=version,
            token=token,
            tenant_uuid=tenant_uuid,
            https=https,
            timeout=timeout,
            verify_certificate=verify_certificate,
            prefix=self._build_prefix(prefix),
            user_agent=user_agent,
            max_retries=max_retries,
            retry_delay=retry_delay,
        )

        # Create sync and async clients
        self._sync_client: httpx.Client | None = None
        self._async_client: httpx.AsyncClient | None = None

        if kwargs:
            logger.warning(
                "%s received unexpected arguments: %s",
                self.__class__.__name__,
                list(kwargs.keys()),
            )

        self._load_plugins()

    def _build_prefix(self, prefix: str | None) -> str:
        """Build a properly formatted URL prefix.

        Args:
            prefix: Raw prefix string

        Returns:
            Formatted prefix with leading slash

        """
        if not prefix:
            return ""
        if not prefix.startswith("/"):
            prefix = "/" + prefix
        return prefix

    def _load_plugins(self) -> None:
        """Load command plugins for this client.

        Raises:
            ValueError: If namespace is not defined

        """
        global PLUGINS_CACHE

        if not self.namespace:
            error_msg = "You must redefine BaseClient.namespace"
            raise ValueError(error_msg)

        if self.namespace not in PLUGINS_CACHE:
            PLUGINS_CACHE[self.namespace] = list(
                extension.ExtensionManager(self.namespace)
            )

        plugins = PLUGINS_CACHE[self.namespace]
        if not plugins:
            logger.warning("No commands found")
            return

        for ext in plugins:
            setattr(self, ext.name, ext.plugin(self))

    @property
    def sync_client(self) -> httpx.Client:
        """Get or create a synchronous HTTP client.

        Returns:
            Configured httpx.Client instance

        """
        if self._sync_client is None:
            self._sync_client = self._create_client(httpx.Client)
        return self._sync_client

    @property
    def async_client(self) -> httpx.AsyncClient:
        """Get or create an asynchronous HTTP client.

        Returns:
            Configured httpx.AsyncClient instance

        """
        if self._async_client is None:
            self._async_client = self._create_client(httpx.AsyncClient)
        return self._async_client

    def _create_client(self, client_class: type[T]) -> T:
        """Create a new HTTP client with the configured settings.

        Args:
            client_class: The httpx client class to instantiate

        Returns:
            Configured client instance

        """
        headers = {"Connection": "close"}

        if self.config.token:
            headers["X-Auth-Token"] = self.config.token

        if self.config.tenant_uuid:
            headers["Accent-Tenant"] = self.config.tenant_uuid

        if self.config.user_agent:
            headers["User-agent"] = self.config.user_agent

        return client_class(
            timeout=self.config.timeout,
            verify=self.config.verify_certificate if self.config.https else False,
            headers=headers,
        )

    # For backwards compatibility
    def session(self) -> httpx.Client:
        """Get a synchronous HTTP client (compatibility method).

        Returns:
            Configured httpx.Client instance

        """
        logger.warning("Deprecated method 'session()'. Use 'sync_client' instead.")
        return self.sync_client

    def set_tenant(self, tenant_uuid: str) -> None:
        """Set the tenant UUID for subsequent requests (deprecated).

        Args:
            tenant_uuid: Tenant identifier

        """
        logger.warning(
            "Deprecated method 'set_tenant()'. Set 'tenant_uuid' directly instead."
        )
        self.config.tenant_uuid = tenant_uuid

        # Reset clients to recreate with new headers
        if self._sync_client:
            self._sync_client.close()
            self._sync_client = None
        if self._async_client:
            import asyncio

            if asyncio.get_event_loop().is_running():
                asyncio.create_task(self._close_async_client())
            else:
                asyncio.run(self._close_async_client())
            self._async_client = None

    async def _close_async_client(self) -> None:
        """Close the async client safely."""
        if self._async_client:
            await self._async_client.aclose()
            self._async_client = None

    def tenant(self) -> str | None:
        """Get the current tenant UUID (deprecated).

        Returns:
            Current tenant UUID or None

        """
        logger.warning(
            "Deprecated method 'tenant()'. Access 'tenant_uuid' directly instead."
        )
        return self.config.tenant_uuid

    def set_token(self, token: str) -> None:
        """Set the authentication token for subsequent requests.

        Args:
            token: Authentication token

        """
        self.config.token = token

        # Reset clients to recreate with new headers
        if self._sync_client:
            self._sync_client.close()
            self._sync_client = None
        if self._async_client:
            import asyncio

            if asyncio.get_event_loop().is_running():
                asyncio.create_task(self._close_async_client())
            else:
                asyncio.run(self._close_async_client())
            self._async_client = None

    @lru_cache(maxsize=128)
    def url(self, *fragments: str) -> str:
        """Build a URL with the configured base and optional path fragments.

        Args:
            *fragments: URL path fragments to append

        Returns:
            Complete URL string

        """
        base = self._url_fmt.format(
            scheme="https" if self.config.https else "http",
            host=self.config.host,
            port=f":{self.config.port}" if self.config.port else "",
            prefix=self.config.prefix,
            version=f"/{self.config.version}" if self.config.version else "",
        )
        if fragments:
            path = "/".join(str(fragment) for fragment in fragments)
            base = f"{base}/{path}"
        return base

    def is_server_reachable(self) -> bool:
        """Check if the server is reachable.

        Returns:
            True if the server responds, False otherwise

        """
        try:
            self.sync_client.head(self.url())
            return True
        except httpx.HTTPStatusError:
            return True
        except httpx.RequestError as e:
            logger.debug("Server unreachable: %s", e)
            return False

    async def is_server_reachable_async(self) -> bool:
        """Check if the server is reachable (async version).

        Returns:
            True if the server responds, False otherwise

        """
        try:
            await self.async_client.head(self.url())
            return True
        except httpx.HTTPStatusError:
            return True
        except httpx.RequestError as e:
            logger.debug("Server unreachable: %s", e)
            return False

    def __del__(self) -> None:
        """Close HTTP clients when the object is destroyed."""
        if hasattr(self, "_sync_client") and self._sync_client:
            self._sync_client.close()
        # Async client needs to be closed explicitly with await
        # We can't await in __del__, but we can check if it exists
        if hasattr(self, "_async_client") and self._async_client:
            # Can't await in __del__, will rely on garbage collection
            pass
