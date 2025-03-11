# Copyright 2025 Accent Communications

"""Command implementations for the Accent Plugin Daemon client.

This module provides REST command classes for various Plugin Daemon
API operations.
"""

from __future__ import annotations

import builtins
import logging
import time
from functools import lru_cache
from typing import Any

import httpx
from accent_lib_rest_client import RESTCommand
from accent_lib_rest_client.exceptions import handle_http_error

from .models import ConfigData, MarketData, PluginData, StatusData

# Configure logging
logger = logging.getLogger(__name__)


class MarketCommand(RESTCommand):
    """Command for interacting with the plugin marketplace.

    Provides methods to get plugin information and list available plugins.
    """

    resource = "market"

    async def get_async(self, namespace: str, name: str) -> MarketData:
        """Get information about a plugin in the marketplace (async).

        Args:
            namespace: Plugin namespace
            name: Plugin name

        Returns:
            Market data for the requested plugin

        Raises:
            AccentAPIError: If the request fails

        """
        headers = self._get_headers()
        url = f"{self.base_url}/{namespace}/{name}"
        start_time = time.time()

        try:
            response = await self.async_client.get(url, headers=headers)
            response.raise_for_status()
            data = response.json()
            logger.debug("Retrieved market data for %s/%s", namespace, name)
            return MarketData.model_validate(data)
        except httpx.HTTPStatusError as e:
            logger.error("Failed to get market data: %s", e)
            handle_http_error(e)
        finally:
            logger.debug(
                "Market get request completed in %.2fs", time.time() - start_time
            )

    def get(self, namespace: str, name: str) -> MarketData:
        """Get information about a plugin in the marketplace.

        Args:
            namespace: Plugin namespace
            name: Plugin name

        Returns:
            Market data for the requested plugin

        Raises:
            AccentAPIError: If the request fails

        """
        headers = self._get_headers()
        url = f"{self.base_url}/{namespace}/{name}"
        start_time = time.time()

        try:
            response = self.sync_client.get(url, headers=headers)
            response.raise_for_status()
            data = response.json()
            logger.debug("Retrieved market data for %s/%s", namespace, name)
            return MarketData.model_validate(data)
        except httpx.HTTPStatusError as e:
            logger.error("Failed to get market data: %s", e)
            handle_http_error(e)
        finally:
            logger.debug(
                "Market get request completed in %.2fs", time.time() - start_time
            )

    async def list_async(
        self, search: str | None = None, **kwargs: Any
    ) -> builtins.list[MarketData]:
        """List plugins in the marketplace (async).

        Args:
            search: Optional search term
            **kwargs: Additional filter parameters

        Returns:
            List of available plugins

        Raises:
            AccentAPIError: If the request fails

        """
        params: dict[str, Any] = dict(kwargs)
        if search:
            params["search"] = search

        headers = self._get_headers()
        start_time = time.time()

        try:
            response = await self.async_client.get(
                self.base_url, params=params, headers=headers
            )
            response.raise_for_status()
            data = response.json()
            logger.debug("Listed market plugins with params: %s", params)
            return [MarketData.model_validate(item) for item in data]
        except httpx.HTTPStatusError as e:
            logger.error("Failed to list market data: %s", e)
            handle_http_error(e)
        finally:
            logger.debug(
                "Market list request completed in %.2fs", time.time() - start_time
            )

    def list(self, *args: str, **kwargs: Any) -> builtins.list[MarketData]:
        """List plugins in the marketplace.

        Args:
            *args: Optional search term as first positional argument
            **kwargs: Additional filter parameters

        Returns:
            List of available plugins

        Raises:
            AccentAPIError: If the request fails

        """
        params: dict[str, Any] = dict(kwargs)
        if args:
            params["search"] = args[0]

        headers = self._get_headers()
        start_time = time.time()

        try:
            response = self.sync_client.get(
                self.base_url, params=params, headers=headers
            )
            response.raise_for_status()
            data = response.json()
            logger.debug("Listed market plugins with params: %s", params)
            return [MarketData.model_validate(item) for item in data]
        except httpx.HTTPStatusError as e:
            logger.error("Failed to list market data: %s", e)
            handle_http_error(e)
        finally:
            logger.debug(
                "Market list request completed in %.2fs", time.time() - start_time
            )


class PluginCommand(RESTCommand):
    """Command for managing plugins.

    Provides methods to get, install, list, and uninstall plugins.
    """

    resource = "plugins"

    async def get_async(self, namespace: str, name: str) -> PluginData:
        """Get information about an installed plugin (async).

        Args:
            namespace: Plugin namespace
            name: Plugin name

        Returns:
            Data for the requested plugin

        Raises:
            AccentAPIError: If the request fails

        """
        headers = self._get_headers()
        url = f"{self.base_url}/{namespace}/{name}"
        start_time = time.time()

        try:
            response = await self.async_client.get(url, headers=headers)
            response.raise_for_status()
            data = response.json()
            logger.debug("Retrieved plugin data for %s/%s", namespace, name)
            return PluginData.model_validate(data)
        except httpx.HTTPStatusError as e:
            logger.error("Failed to get plugin data: %s", e)
            handle_http_error(e)
        finally:
            logger.debug(
                "Plugin get request completed in %.2fs", time.time() - start_time
            )

    def get(self, namespace: str, name: str) -> PluginData:
        """Get information about an installed plugin.

        Args:
            namespace: Plugin namespace
            name: Plugin name

        Returns:
            Data for the requested plugin

        Raises:
            AccentAPIError: If the request fails

        """
        headers = self._get_headers()
        url = f"{self.base_url}/{namespace}/{name}"
        start_time = time.time()

        try:
            response = self.sync_client.get(url, headers=headers)
            response.raise_for_status()
            data = response.json()
            logger.debug("Retrieved plugin data for %s/%s", namespace, name)
            return PluginData.model_validate(data)
        except httpx.HTTPStatusError as e:
            logger.error("Failed to get plugin data: %s", e)
            handle_http_error(e)
        finally:
            logger.debug(
                "Plugin get request completed in %.2fs", time.time() - start_time
            )

    async def install_async(
        self,
        url: str | None = None,
        method: str | None = None,
        options: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> PluginData:
        """Install a plugin (async).

        Args:
            url: URL to install the plugin from
            method: Installation method
            options: Additional installation options
            **kwargs: Additional parameters

        Returns:
            Data for the installed plugin

        Raises:
            AccentAPIError: If the installation fails

        """
        data: dict[str, Any] = {"method": method, "options": options or {}}

        query_string: dict[str, bool] = {}
        if kwargs.get("reinstall"):
            query_string["reinstall"] = True

        if url:
            data["options"]["url"] = url

        headers = self._get_headers()
        start_time = time.time()

        try:
            response = await self.async_client.post(
                self.base_url,
                headers=headers,
                params=query_string,
                json=data,
            )
            response.raise_for_status()
            result = response.json()
            logger.info(
                "Installed plugin with method: %s, url: %s", method, url or "N/A"
            )
            return PluginData.model_validate(result)
        except httpx.HTTPStatusError as e:
            logger.error("Failed to install plugin: %s", e)
            handle_http_error(e)
        finally:
            logger.debug(
                "Plugin install request completed in %.2fs", time.time() - start_time
            )

    def install(
        self,
        url: str | None = None,
        method: str | None = None,
        options: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> PluginData:
        """Install a plugin.

        Args:
            url: URL to install the plugin from
            method: Installation method
            options: Additional installation options
            **kwargs: Additional parameters

        Returns:
            Data for the installed plugin

        Raises:
            AccentAPIError: If the installation fails

        """
        data: dict[str, Any] = {"method": method, "options": options or {}}

        query_string: dict[str, bool] = {}
        if kwargs.get("reinstall"):
            query_string["reinstall"] = True

        if url:
            data["options"]["url"] = url

        headers = self._get_headers()
        start_time = time.time()

        try:
            response = self.sync_client.post(
                self.base_url,
                headers=headers,
                params=query_string,
                json=data,
            )
            response.raise_for_status()
            result = response.json()
            logger.info(
                "Installed plugin with method: %s, url: %s", method, url or "N/A"
            )
            return PluginData.model_validate(result)
        except httpx.HTTPStatusError as e:
            logger.error("Failed to install plugin: %s", e)
            handle_http_error(e)
        finally:
            logger.debug(
                "Plugin install request completed in %.2fs", time.time() - start_time
            )

    @lru_cache(maxsize=32)
    async def list_async(self) -> builtins.list[PluginData]:
        """List installed plugins (async).

        Returns:
            List of installed plugins

        Raises:
            AccentAPIError: If the request fails

        """
        headers = self._get_headers()
        start_time = time.time()

        try:
            response = await self.async_client.get(self.base_url, headers=headers)
            response.raise_for_status()
            data = response.json()
            logger.debug("Listed installed plugins")
            return [PluginData.model_validate(item) for item in data]
        except httpx.HTTPStatusError as e:
            logger.error("Failed to list plugins: %s", e)
            handle_http_error(e)
        finally:
            logger.debug(
                "Plugin list request completed in %.2fs", time.time() - start_time
            )

    @lru_cache(maxsize=32)
    def list(self) -> builtins.list[PluginData]:
        """List installed plugins.

        Returns:
            List of installed plugins

        Raises:
            AccentAPIError: If the request fails

        """
        headers = self._get_headers()
        start_time = time.time()

        try:
            response = self.sync_client.get(self.base_url, headers=headers)
            response.raise_for_status()
            data = response.json()
            logger.debug("Listed installed plugins")
            return [PluginData.model_validate(item) for item in data]
        except httpx.HTTPStatusError as e:
            logger.error("Failed to list plugins: %s", e)
            handle_http_error(e)
        finally:
            logger.debug(
                "Plugin list request completed in %.2fs", time.time() - start_time
            )

    async def uninstall_async(self, namespace: str, name: str) -> None:
        """Uninstall a plugin (async).

        Args:
            namespace: Plugin namespace
            name: Plugin name

        Raises:
            AccentAPIError: If the uninstallation fails

        """
        headers = self._get_headers()
        url = f"{self.base_url}/{namespace}/{name}"
        start_time = time.time()

        try:
            response = await self.async_client.delete(url, headers=headers)
            response.raise_for_status()
            logger.info("Uninstalled plugin %s/%s", namespace, name)
        except httpx.HTTPStatusError as e:
            logger.error("Failed to uninstall plugin: %s", e)
            handle_http_error(e)
        finally:
            logger.debug(
                "Plugin uninstall request completed in %.2fs", time.time() - start_time
            )

    def uninstall(self, namespace: str, name: str) -> None:
        """Uninstall a plugin.

        Args:
            namespace: Plugin namespace
            name: Plugin name

        Raises:
            AccentAPIError: If the uninstallation fails

        """
        headers = self._get_headers()
        url = f"{self.base_url}/{namespace}/{name}"
        start_time = time.time()

        try:
            response = self.sync_client.delete(url, headers=headers)
            # Original had a status check for 204
            if response.status_code != 204:
                response.raise_for_status()
            logger.info("Uninstalled plugin %s/%s", namespace, name)
        except httpx.HTTPStatusError as e:
            logger.error("Failed to uninstall plugin: %s", e)
            handle_http_error(e)
        finally:
            logger.debug(
                "Plugin uninstall request completed in %.2fs", time.time() - start_time
            )


class ConfigCommand(RESTCommand):
    """Command for managing plugin daemon configuration.

    Provides methods to get and update configuration.
    """

    resource = "config"

    @lru_cache(maxsize=8)
    async def get_async(self) -> ConfigData:
        """Get the current plugin daemon configuration (async).

        Returns:
            Current configuration

        Raises:
            AccentAPIError: If the request fails

        """
        headers = self._get_headers()
        start_time = time.time()

        try:
            response = await self.async_client.get(self.base_url, headers=headers)
            response.raise_for_status()
            data = response.json()
            logger.debug("Retrieved plugin daemon configuration")
            return ConfigData.model_validate(data)
        except httpx.HTTPStatusError as e:
            logger.error("Failed to get configuration: %s", e)
            handle_http_error(e)
        finally:
            logger.debug(
                "Config get request completed in %.2fs", time.time() - start_time
            )

    @lru_cache(maxsize=8)
    def get(self) -> ConfigData:
        """Get the current plugin daemon configuration.

        Returns:
            Current configuration

        Raises:
            AccentAPIError: If the request fails

        """
        headers = self._get_headers()
        start_time = time.time()

        try:
            response = self.sync_client.get(self.base_url, headers=headers)
            response.raise_for_status()
            data = response.json()
            logger.debug("Retrieved plugin daemon configuration")
            return ConfigData.model_validate(data)
        except httpx.HTTPStatusError as e:
            logger.error("Failed to get configuration: %s", e)
            handle_http_error(e)
        finally:
            logger.debug(
                "Config get request completed in %.2fs", time.time() - start_time
            )


class StatusCheckerCommand(RESTCommand):
    """Command for checking the plugin daemon status.

    Provides methods to get the current status.
    """

    resource = "status"

    async def get_async(self) -> StatusData:
        """Get the current plugin daemon status (async).

        Returns:
            Current status

        Raises:
            AccentAPIError: If the request fails

        """
        headers = self._get_headers()
        start_time = time.time()

        try:
            response = await self.async_client.get(self.base_url, headers=headers)
            response.raise_for_status()
            data = response.json()
            logger.debug("Retrieved plugin daemon status")
            return StatusData.model_validate(data)
        except httpx.HTTPStatusError as e:
            logger.error("Failed to get status: %s", e)
            handle_http_error(e)
        finally:
            logger.debug(
                "Status get request completed in %.2fs", time.time() - start_time
            )

    def get(self) -> StatusData:
        """Get the current plugin daemon status.

        Returns:
            Current status

        Raises:
            AccentAPIError: If the request fails

        """
        headers = self._get_headers()
        start_time = time.time()

        try:
            response = self.sync_client.get(self.base_url, headers=headers)
            response.raise_for_status()
            data = response.json()
            logger.debug("Retrieved plugin daemon status")
            return StatusData.model_validate(data)
        except httpx.HTTPStatusError as e:
            logger.error("Failed to get status: %s", e)
            handle_http_error(e)
        finally:
            logger.debug(
                "Status get request completed in %.2fs", time.time() - start_time
            )
