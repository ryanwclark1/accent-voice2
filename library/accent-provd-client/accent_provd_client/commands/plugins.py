# Copyright 2025 Accent Communications

"""Commands for plugin management."""

from __future__ import annotations

import logging
from typing import Any

from accent_provd_client.command import ProvdCommand
from accent_provd_client.operation import OperationInProgress

logger = logging.getLogger(__name__)

class PluginsCommand(ProvdCommand):
    """Commands for plugin management.

    Provides methods for managing provisioning plugins.
    """

    resource = "pg_mgr"
    _headers = {"Content-Type": "application/vnd.accent.provd+json"}

    async def update_async(self) -> OperationInProgress:
        """Update plugins asynchronously.

        Returns:
            Operation tracking object

        Raises:
            ProvdError: If the request fails

        """
        url = f"{self.base_url}/install/update"
        r = await self.async_client.post(url, json={}, headers=self._headers)
        self.raise_from_response(r)
        return OperationInProgress(self, r.headers["Location"])

    def update(self) -> OperationInProgress:
        """Update plugins.

        Returns:
            Operation tracking object

        Raises:
            ProvdError: If the request fails

        """
        url = f"{self.base_url}/install/update"
        r = self.sync_client.post(url, json={}, headers=self._headers)
        self.raise_from_response(r)
        return OperationInProgress(self, r.headers["Location"])

    async def get_async(self, id_: str) -> dict[str, Any]:
        """Get plugin information asynchronously.

        Args:
            id_: Plugin ID

        Returns:
            Plugin information

        Raises:
            ProvdError: If the request fails

        """
        url = f"{self.base_url}/plugins/{id_}/info"
        r = await self.async_client.get(url)
        self.raise_from_response(r)
        return r.json()["plugin_info"]

    def get(self, id_: str) -> dict[str, Any]:
        """Get plugin information.

        Args:
            id_: Plugin ID

        Returns:
            Plugin information

        Raises:
            ProvdError: If the request fails

        """
        url = f"{self.base_url}/plugins/{id_}/info"
        r = self.sync_client.get(url)
        self.raise_from_response(r)
        return r.json()["plugin_info"]

    async def upgrade_async(self, id_: str) -> OperationInProgress:
        """Upgrade a plugin asynchronously.

        Args:
            id_: Plugin ID

        Returns:
            Operation tracking object

        Raises:
            ProvdError: If the request fails

        """
        url = f"{self.base_url}/install/upgrade"
        r = await self.async_client.post(url, json={"id": id_}, headers=self._headers)
        self.raise_from_response(r)
        return OperationInProgress(self, r.headers["Location"])

    def upgrade(self, id_: str) -> OperationInProgress:
        """Upgrade a plugin.

        Args:
            id_: Plugin ID

        Returns:
            Operation tracking object

        Raises:
            ProvdError: If the request fails

        """
        url = f"{self.base_url}/install/upgrade"
        r = self.sync_client.post(url, json={"id": id_}, headers=self._headers)
        self.raise_from_response(r)
        return OperationInProgress(self, r.headers["Location"])

    async def install_async(self, id_: str) -> OperationInProgress:
        """Install a plugin asynchronously.

        Args:
            id_: Plugin ID

        Returns:
            Operation tracking object

        Raises:
            ProvdError: If the request fails

        """
        url = f"{self.base_url}/install/install"
        r = await self.async_client.post(url, json={"id": id_}, headers=self._headers)
        self.raise_from_response(r)
        return OperationInProgress(self, r.headers["Location"])

    def install(self, id_: str) -> OperationInProgress:
        """Install a plugin.

        Args:
            id_: Plugin ID

        Returns:
            Operation tracking object

        Raises:
            ProvdError: If the request fails

        """
        url = f"{self.base_url}/install/install"
        r = self.sync_client.post(url, json={"id": id_}, headers=self._headers)
        self.raise_from_response(r)
        return OperationInProgress(self, r.headers["Location"])

    async def uninstall_async(self, id_: str) -> None:
        """Uninstall a plugin asynchronously.

        Args:
            id_: Plugin ID

        Raises:
            ProvdError: If the request fails

        """
        url = f"{self.base_url}/install/uninstall"
        r = await self.async_client.post(url, json={"id": id_}, headers=self._headers)
        self.raise_from_response(r)

    def uninstall(self, id_: str) -> None:
        """Uninstall a plugin.

        Args:
            id_: Plugin ID

        Raises:
            ProvdError: If the request fails

        """
        url = f"{self.base_url}/install/uninstall"
        r = self.sync_client.post(url, json={"id": id_}, headers=self._headers)
        self.raise_from_response(r)

    async def list_async(self, **params: Any) -> dict[str, Any]:
        """List plugins asynchronously.

        Args:
            **params: Filter parameters

        Returns:
            List of plugins

        Raises:
            ProvdError: If the request fails

        """
        url = f"{self.base_url}/plugins"
        r = await self.async_client.get(url, params=params)
        self.raise_from_response(r)
        return r.json()

    def list(self, **params: Any) -> dict[str, Any]:
        """List plugins.

        Args:
            **params: Filter parameters

        Returns:
            List of plugins

        Raises:
            ProvdError: If the request fails

        """
        url = f"{self.base_url}/plugins"
        r = self.sync_client.get(url, params=params)
        self.raise_from_response(r)
        return r.json()

    async def list_installed_async(self, **params: Any) -> dict[str, Any]:
        """List installed plugins asynchronously.

        Args:
            **params: Filter parameters

        Returns:
            List of installed plugins

        Raises:
            ProvdError: If the request fails

        """
        url = f"{self.base_url}/install/installed"
        r = await self.async_client.get(url, params=params)
        self.raise_from_response(r)
        return r.json()

    def list_installed(self, **params: Any) -> dict[str, Any]:
        """List installed plugins.

        Args:
            **params: Filter parameters

        Returns:
            List of installed plugins

        Raises:
            ProvdError: If the request fails

        """
        url = f"{self.base_url}/install/installed"
        r = self.sync_client.get(url, params=params)
        self.raise_from_response(r)
        return r.json()

    async def list_installable_async(self, **params: Any) -> dict[str, Any]:
        """List installable plugins asynchronously.

        Args:
            **params: Filter parameters

        Returns:
            List of installable plugins

        Raises:
            ProvdError: If the request fails

        """
        url = f"{self.base_url}/install/installable"
        r = await self.async_client.get(url, params=params)
        self.raise_from_response(r)
        return r.json()

    def list_installable(self, **params: Any) -> dict[str, Any]:
        """List installable plugins.

        Args:
            **params: Filter parameters

        Returns:
            List of installable plugins

        Raises:
            ProvdError: If the request fails

        """
        url = f"{self.base_url}/install/installable"
        r = self.sync_client.get(url, params=params)
        self.raise_from_response(r)
        return r.json()

    async def get_packages_installed_async(
        self,
        plugin: str,
        **params: Any
    ) -> dict[str, Any]:
        """Get installed packages for a plugin asynchronously.

        Args:
            plugin: Plugin ID
            **params: Filter parameters

        Returns:
            List of installed packages

        Raises:
            ProvdError: If the request fails

        """
        url = f"{self.base_url}/plugins/{plugin}/install/installed"
        r = await self.async_client.get(url, params=params)
        self.raise_from_response(r)
        return r.json()

    def get_packages_installed(self, plugin: str, **params: Any) -> dict[str, Any]:
        """Get installed packages for a plugin.

        Args:
            plugin: Plugin ID
            **params: Filter parameters

        Returns:
            List of installed packages

        Raises:
            ProvdError: If the request fails

        """
        url = f"{self.base_url}/plugins/{plugin}/install/installed"
        r = self.sync_client.get(url, params=params)
        self.raise_from_response(r)
        return r.json()

    async def get_packages_installable_async(
        self,
        plugin: str,
        **params: Any
    ) -> dict[str, Any]:
        """Get installable packages for a plugin asynchronously.

        Args:
            plugin: Plugin ID
            **params: Filter parameters

        Returns:
            List of installable packages

        Raises:
            ProvdError: If the request fails

        """
        url = f"{self.base_url}/plugins/{plugin}/install/installable"
        r = await self.async_client.get(url, params=params)
        self.raise_from_response(r)
        return r.json()

    def get_packages_installable(self, plugin: str, **params: Any) -> dict[str, Any]:
        """Get installable packages for a plugin.

        Args:
            plugin: Plugin ID
            **params: Filter parameters

        Returns:
            List of installable packages

        Raises:
            ProvdError: If the request fails

        """
        url = f"{self.base_url}/plugins/{plugin}/install/installable"
        r = self.sync_client.get(url, params=params)
        self.raise_from_response(r)
        return r.json()

    async def install_package_async(
        self,
        plugin: str,
        package: str
    ) -> OperationInProgress:
        """Install a package asynchronously.

        Args:
            plugin: Plugin ID
            package: Package ID

        Returns:
            Operation tracking object

        Raises:
            ProvdError: If the request fails

        """
        url = f"{self.base_url}/plugins/{plugin}/install/install"
        r = await self.async_client.post(
            url,
            json={"id": package},
            headers=self._headers
        )
        self.raise_from_response(r)
        return OperationInProgress(self, r.headers["Location"])

    def install_package(self, plugin: str, package: str) -> OperationInProgress:
        """Install a package.

        Args:
            plugin: Plugin ID
            package: Package ID

        Returns:
            Operation tracking object

        Raises:
            ProvdError: If the request fails

        """
        url = f"{self.base_url}/plugins/{plugin}/install/install"
        r = self.sync_client.post(
            url,
            json={"id": package},
            headers=self._headers
        )
        self.raise_from_response(r)
        return OperationInProgress(self, r.headers["Location"])

    async def uninstall_package_async(self, plugin: str, package: str) -> None:
        """Uninstall a package asynchronously.

        Args:
            plugin: Plugin ID
            package: Package ID

        Raises:
            ProvdError: If the request fails

        """
        url = f"{self.base_url}/plugins/{plugin}/install/uninstall"
        r = await self.async_client.post(
            url,
            json={"id": package},
            headers=self._headers
        )
        self.raise_from_response(r)

    def uninstall_package(self, plugin: str, package: str) -> None:
        """Uninstall a package.

        Args:
            plugin: Plugin ID
            package: Package ID

        Raises:
            ProvdError: If the request fails

        """
        url = f"{self.base_url}/plugins/{plugin}/install/uninstall"
        r = self.sync_client.post(
            url,
            json={"id": package},
            headers=self._headers
        )
        self.raise_from_response(r)

    async def upgrade_package_async(
        self,
        plugin: str,
        package: str
    ) -> OperationInProgress:
        """Upgrade a package asynchronously.

        Args:
            plugin: Plugin ID
            package: Package ID

        Returns:
            Operation tracking object

        Raises:
            ProvdError: If the request fails

        """
        url = f"{self.base_url}/plugins/{plugin}/install/upgrade"
        r = await self.async_client.post(
            url,
            json={"id": package},
            headers=self._headers
        )
        self.raise_from_response(r)
        return OperationInProgress(self, r.headers["Location"])

    def upgrade_package(self, plugin: str, package: str) -> OperationInProgress:
        """Upgrade a package.

        Args:
            plugin: Plugin ID
            package: Package ID

        Returns:
            Operation tracking object

        Raises:
            ProvdError: If the request fails

        """
        url = f"{self.base_url}/plugins/{plugin}/install/upgrade"
        r = self.sync_client.post(url, json={"id": package}, headers=self._headers)
        self.raise_from_response(r)
        return OperationInProgress(self, r.headers["Location"])
