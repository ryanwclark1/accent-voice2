# Copyright 2025 Accent Communications

"""Commands for configuration management."""

from __future__ import annotations

import base64
import json
import logging
from typing import Any

from accent_provd_client.command import ProvdCommand

logger = logging.getLogger(__name__)


class ConfigsCommand(ProvdCommand):
    """Commands for configuration management.

    Provides methods for managing device and registrar configurations.
    """

    resource = "cfg_mgr"
    _headers = {"Content-Type": "application/vnd.accent.provd+json"}

    async def list_registrar_async(self, **params: Any) -> dict[str, Any]:
        """List registrar configurations asynchronously.

        Args:
            **params: Additional filtering parameters

        Returns:
            List of registrar configurations

        Raises:
            ProvdError: If the request fails

        """
        url = f"{self.base_url}/configs"
        params.update(self._prepare_query({"X_type": "registrar"}))

        r = await self.async_client.get(url, params=params)
        self.raise_from_response(r)
        return r.json()

    def list_registrar(self, **params: Any) -> dict[str, Any]:
        """List registrar configurations.

        Args:
            **params: Additional filtering parameters

        Returns:
            List of registrar configurations

        Raises:
            ProvdError: If the request fails

        """
        url = f"{self.base_url}/configs"
        params.update(self._prepare_query({"X_type": "registrar"}))

        r = self.sync_client.get(url, params=params)
        self.raise_from_response(r)
        return r.json()

    async def list_device_async(self, **params: Any) -> dict[str, Any]:
        """List device configurations asynchronously.

        Args:
            **params: Additional filtering parameters

        Returns:
            List of device configurations

        Raises:
            ProvdError: If the request fails

        """
        url = f"{self.base_url}/configs"
        params.update(self._prepare_query({"X_type": "device"}))

        r = await self.async_client.get(url, params=params)
        self.raise_from_response(r)
        return r.json()

    def list_device(self, **params: Any) -> dict[str, Any]:
        """List device configurations.

        Args:
            **params: Additional filtering parameters

        Returns:
            List of device configurations

        Raises:
            ProvdError: If the request fails

        """
        url = f"{self.base_url}/configs"
        params.update(self._prepare_query({"X_type": "device"}))

        r = self.sync_client.get(url, params=params)
        self.raise_from_response(r)
        return r.json()

    async def list_async(self, *args: Any, **kwargs: Any) -> dict[str, Any]:
        """List configurations asynchronously.

        Args:
            *args: Positional arguments for backward compatibility
            **kwargs: Additional filtering parameters

        Returns:
            List of configurations

        Raises:
            ProvdError: If the request fails

        """
        url = f"{self.base_url}/configs"
        r = await self.async_client.get(
            url, params=self._build_list_params(*args, **kwargs)
        )
        self.raise_from_response(r)
        return r.json()

    def list(self, *args: Any, **kwargs: Any) -> dict[str, Any]:
        """List configurations.

        Args:
            *args: Positional arguments for backward compatibility
            **kwargs: Additional filtering parameters

        Returns:
            List of configurations

        Raises:
            ProvdError: If the request fails

        """
        url = f"{self.base_url}/configs"
        r = self.sync_client.get(url, params=self._build_list_params(*args, **kwargs))
        self.raise_from_response(r)
        return r.json()

    async def get_all_async(self) -> dict[str, Any]:
        """Get all configurations asynchronously.

        Returns:
            All configurations

        Raises:
            ProvdError: If the request fails

        """
        url = f"{self.base_url}/configs"
        r = await self.async_client.get(url)
        self.raise_from_response(r)
        return r.json()

    def get_all(self) -> dict[str, Any]:
        """Get all configurations.

        Returns:
            All configurations

        Raises:
            ProvdError: If the request fails

        """
        url = f"{self.base_url}/configs"
        r = self.sync_client.get(url)
        self.raise_from_response(r)
        return r.json()

    async def get_async(self, id_: str) -> dict[str, Any]:
        """Get a configuration by ID asynchronously.

        Args:
            id_: Configuration ID

        Returns:
            Configuration data

        Raises:
            ProvdError: If the request fails

        """
        url = f"{self.base_url}/configs/{id_}"
        r = await self.async_client.get(url, headers=self._headers)
        self.raise_from_response(r)
        return r.json()["config"]

    def get(self, id_: str) -> dict[str, Any]:
        """Get a configuration by ID.

        Args:
            id_: Configuration ID

        Returns:
            Configuration data

        Raises:
            ProvdError: If the request fails

        """
        url = f"{self.base_url}/configs/{id_}"
        r = self.sync_client.get(url, headers=self._headers)
        self.raise_from_response(r)
        return r.json()["config"]

    async def get_raw_async(self, id_: str) -> dict[str, Any]:
        """Get raw configuration by ID asynchronously.

        Args:
            id_: Configuration ID

        Returns:
            Raw configuration data

        Raises:
            ProvdError: If the request fails

        """
        url = f"{self.base_url}/configs/{id_}/raw"
        r = await self.async_client.get(url, headers=self._headers)
        self.raise_from_response(r)
        return r.json()["raw_config"]

    def get_raw(self, id_: str) -> dict[str, Any]:
        """Get raw configuration by ID.

        Args:
            id_: Configuration ID

        Returns:
            Raw configuration data

        Raises:
            ProvdError: If the request fails

        """
        url = f"{self.base_url}/configs/{id_}/raw"
        r = self.sync_client.get(url, headers=self._headers)
        self.raise_from_response(r)
        return r.json()["raw_config"]

    async def create_async(self, data: dict[str, Any]) -> dict[str, Any]:
        """Create a configuration asynchronously.

        Args:
            data: Configuration data

        Returns:
            Created configuration

        Raises:
            ProvdError: If the request fails

        """
        url = f"{self.base_url}/configs"
        r = await self.async_client.post(
            url, json={"config": data}, headers=self._headers
        )
        self.raise_from_response(r)
        return r.json()

    def create(self, data: dict[str, Any]) -> dict[str, Any]:
        """Create a configuration.

        Args:
            data: Configuration data

        Returns:
            Created configuration

        Raises:
            ProvdError: If the request fails

        """
        url = f"{self.base_url}/configs"
        r = self.sync_client.post(url, json={"config": data}, headers=self._headers)
        self.raise_from_response(r)
        return r.json()

    async def update_async(self, data: dict[str, Any]) -> None:
        """Update a configuration asynchronously.

        Args:
            data: Configuration data with ID

        Raises:
            ProvdError: If the request fails

        """
        id_ = data["id"]
        url = f"{self.base_url}/configs/{id_}"
        r = await self.async_client.put(
            url, json={"config": data}, headers=self._headers
        )
        self.raise_from_response(r)

    def update(self, data: dict[str, Any]) -> None:
        """Update a configuration.

        Args:
            data: Configuration data with ID

        Raises:
            ProvdError: If the request fails

        """
        id_ = data["id"]
        url = f"{self.base_url}/configs/{id_}"
        r = self.sync_client.put(url, json={"config": data}, headers=self._headers)
        self.raise_from_response(r)

    async def delete_async(self, id_: str) -> None:
        """Delete a configuration asynchronously.

        Args:
            id_: Configuration ID

        Raises:
            ProvdError: If the request fails

        """
        url = f"{self.base_url}/configs/{id_}"
        r = await self.async_client.delete(url)
        self.raise_from_response(r)

    def delete(self, id_: str) -> None:
        """Delete a configuration.

        Args:
            id_: Configuration ID

        Raises:
            ProvdError: If the request fails

        """
        url = f"{self.base_url}/configs/{id_}"
        r = self.sync_client.delete(url)
        self.raise_from_response(r)

    async def autocreate_async(self) -> dict[str, Any]:
        """Auto-create configurations asynchronously.

        Returns:
            Created configurations

        Raises:
            ProvdError: If the request fails

        """
        url = f"{self.base_url}/autocreate"
        r = await self.async_client.post(url, json={}, headers=self._headers)
        self.raise_from_response(r)
        return r.json()

    def autocreate(self) -> dict[str, Any]:
        """Auto-create configurations.

        Returns:
            Created configurations

        Raises:
            ProvdError: If the request fails

        """
        url = f"{self.base_url}/autocreate"
        r = self.sync_client.post(url, json={}, headers=self._headers)
        self.raise_from_response(r)
        return r.json()

    def _prepare_query(self, query: dict[str, Any]) -> dict[str, str]:
        """Prepare a query for the API.

        Args:
            query: Query parameters

        Returns:
            Encoded query parameters

        """
        query_json = json.dumps(query).encode("utf-8")
        query_b64 = base64.b64encode(query_json).decode("utf-8")
        return {"q64": query_b64}
