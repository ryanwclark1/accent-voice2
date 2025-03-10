# Copyright 2025 Accent Communications

"""Commands for parameter management."""

from __future__ import annotations

import logging
from typing import Any

from accent_provd_client.command import ProvdCommand

logger = logging.getLogger(__name__)


class ParamsCommand(ProvdCommand):
    """Commands for parameter management.

    Provides methods for managing system parameters.
    """

    resource = "configure"
    _headers = {"Content-Type": "application/vnd.accent.provd+json"}

    async def list_async(self) -> dict[str, Any]:
        """List parameters asynchronously.

        Returns:
            List of parameters

        Raises:
            ProvdError: If the request fails

        """
        url = f"{self.base_url}"
        r = await self.async_client.get(url)
        self.raise_from_response(r)
        return r.json()

    def list(self) -> dict[str, Any]:
        """List parameters.

        Returns:
            List of parameters

        Raises:
            ProvdError: If the request fails

        """
        url = f"{self.base_url}"
        r = self.sync_client.get(url)
        self.raise_from_response(r)
        return r.json()

    async def get_async(
        self, param: str, tenant_uuid: str | None = None, **kwargs: Any
    ) -> Any:
        """Get a parameter value asynchronously.

        Args:
            param: Parameter name
            tenant_uuid: Optional tenant UUID
            **kwargs: Additional parameters

        Returns:
            Parameter value

        Raises:
            ProvdError: If the request fails

        """
        url = f"{self.base_url}/{param}"
        headers = self._get_headers(tenant_uuid=tenant_uuid)
        r = await self.async_client.get(url, headers=headers)
        self.raise_from_response(r)
        return r.json()["param"]

    def get(self, param: str, tenant_uuid: str | None = None, **kwargs: Any) -> Any:
        """Get a parameter value.

        Args:
            param: Parameter name
            tenant_uuid: Optional tenant UUID
            **kwargs: Additional parameters

        Returns:
            Parameter value

        Raises:
            ProvdError: If the request fails

        """
        url = f"{self.base_url}/{param}"
        headers = self._get_headers(tenant_uuid=tenant_uuid)
        r = self.sync_client.get(url, headers=headers)
        self.raise_from_response(r)
        return r.json()["param"]

    async def update_async(
        self, param: str, value: Any, tenant_uuid: str | None = None, **kwargs: Any
    ) -> None:
        """Update a parameter value asynchronously.

        Args:
            param: Parameter name
            value: New parameter value
            tenant_uuid: Optional tenant UUID
            **kwargs: Additional parameters

        Raises:
            ProvdError: If the request fails

        """
        url = f"{self.base_url}/{param}"
        data = {"param": {"value": value}}
        headers = self._get_headers(tenant_uuid=tenant_uuid)
        r = await self.async_client.put(url, json=data, headers=headers)
        self.raise_from_response(r)

    def update(
        self, param: str, value: Any, tenant_uuid: str | None = None, **kwargs: Any
    ) -> None:
        """Update a parameter value.

        Args:
            param: Parameter name
            value: New parameter value
            tenant_uuid: Optional tenant UUID
            **kwargs: Additional parameters

        Raises:
            ProvdError: If the request fails

        """
        url = f"{self.base_url}/{param}"
        data = {"param": {"value": value}}
        headers = self._get_headers(tenant_uuid=tenant_uuid)
        r = self.sync_client.put(url, json=data, headers=headers)
        self.raise_from_response(r)

    async def delete_async(self, param: str) -> None:
        """Delete a parameter asynchronously.

        Args:
            param: Parameter name

        Raises:
            ProvdError: If the request fails

        """
        await self.update_async(param, None)

    def delete(self, param: str) -> None:
        """Delete a parameter.

        Args:
            param: Parameter name

        Raises:
            ProvdError: If the request fails

        """
        self.update(param, None)
