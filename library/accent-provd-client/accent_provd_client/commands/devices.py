# Copyright 2025 Accent Communications

"""Commands for device management."""

from __future__ import annotations

import logging
from typing import Any

from accent_provd_client.command import ProvdCommand
from accent_provd_client.operation import OperationInProgress

logger = logging.getLogger(__name__)


class DevicesCommand(ProvdCommand):
    """Commands for device management.

    Provides methods for managing devices.
    """

    resource = "dev_mgr"
    _headers = {"Content-Type": "application/vnd.accent.provd+json"}

    def _build_headers(self, kwargs: dict[str, Any]) -> dict[str, str]:
        """Build headers for device commands.

        Args:
            kwargs: Keyword arguments

        Returns:
            Headers dictionary

        """
        headers: dict[str, str] = {}
        # The requests session will use self.tenant_uuid by default
        tenant_uuid = kwargs.pop("tenant_uuid", None)
        if tenant_uuid:
            headers["Accent-Tenant"] = str(tenant_uuid)
        return headers

    def _build_headers_with_global_headers(
        self, kwargs: dict[str, Any]
    ) -> dict[str, str]:
        """Build headers with global headers included.

        Args:
            kwargs: Keyword arguments

        Returns:
            Headers dictionary

        """
        headers = dict(self._headers)
        headers.update(self._build_headers(kwargs))
        return headers

    async def get_async(self, device_id: str, **kwargs: Any) -> dict[str, Any]:
        """Get a device by ID asynchronously.

        Args:
            device_id: Device ID
            **kwargs: Additional parameters

        Returns:
            Device data

        Raises:
            ProvdError: If the request fails

        """
        url = f"{self.base_url}/devices/{device_id}"
        r = await self.async_client.get(
            url, headers=self._build_headers(kwargs), params=kwargs
        )
        self.raise_from_response(r)
        return r.json()["device"]

    def get(self, device_id: str, **kwargs: Any) -> dict[str, Any]:
        """Get a device by ID.

        Args:
            device_id: Device ID
            **kwargs: Additional parameters

        Returns:
            Device data

        Raises:
            ProvdError: If the request fails

        """
        url = f"{self.base_url}/devices/{device_id}"
        r = self.sync_client.get(
            url, headers=self._build_headers(kwargs), params=kwargs
        )
        self.raise_from_response(r)
        return r.json()["device"]

    async def list_async(self, *args: Any, **kwargs: Any) -> dict[str, Any]:
        """List devices asynchronously.

        Args:
            *args: Positional arguments for backward compatibility
            **kwargs: Additional filtering parameters

        Returns:
            List of devices

        Raises:
            ProvdError: If the request fails

        """
        url = f"{self.base_url}/devices"
        r = await self.async_client.get(
            url,
            headers=self._build_headers(kwargs),
            params=self._build_list_params(*args, **kwargs),
        )
        self.raise_from_response(r)
        return r.json()

    def list(self, *args: Any, **kwargs: Any) -> dict[str, Any]:
        """List devices.

        Args:
            *args: Positional arguments for backward compatibility
            **kwargs: Additional filtering parameters

        Returns:
            List of devices

        Raises:
            ProvdError: If the request fails

        """
        url = f"{self.base_url}/devices"
        r = self.sync_client.get(
            url,
            headers=self._build_headers(kwargs),
            params=self._build_list_params(*args, **kwargs),
        )
        self.raise_from_response(r)
        return r.json()

    async def update_async(self, data: dict[str, Any], **kwargs: Any) -> None:
        """Update a device asynchronously.

        Args:
            data: Device data with ID
            **kwargs: Additional parameters

        Raises:
            ProvdError: If the request fails

        """
        device_id = data.get("id")
        url = f"{self.base_url}/devices/{device_id}"
        r = await self.async_client.put(
            url,
            json={"device": data},
            headers=self._build_headers_with_global_headers(kwargs),
            params=kwargs,
        )
        self.raise_from_response(r)

    def update(self, data: dict[str, Any], **kwargs: Any) -> None:
        """Update a device.

        Args:
            data: Device data with ID
            **kwargs: Additional parameters

        Raises:
            ProvdError: If the request fails

        """
        device_id = data.get("id")
        url = f"{self.base_url}/devices/{device_id}"
        r = self.sync_client.put(
            url,
            json={"device": data},
            headers=self._build_headers_with_global_headers(kwargs),
            params=kwargs,
        )
        self.raise_from_response(r)

    async def create_async(self, data: dict[str, Any], **kwargs: Any) -> dict[str, Any]:
        """Create a device asynchronously.

        Args:
            data: Device data
            **kwargs: Additional parameters

        Returns:
            Created device data

        Raises:
            ProvdError: If the request fails

        """
        url = f"{self.base_url}/devices"
        r = await self.async_client.post(
            url,
            json={"device": data},
            headers=self._build_headers_with_global_headers(kwargs),
            params=kwargs,
        )
        self.raise_from_response(r)
        return r.json()

    def create(self, data: dict[str, Any], **kwargs: Any) -> dict[str, Any]:
        """Create a device.

        Args:
            data: Device data
            **kwargs: Additional parameters

        Returns:
            Created device data

        Raises:
            ProvdError: If the request fails

        """
        url = f"{self.base_url}/devices"
        r = self.sync_client.post(
            url,
            json={"device": data},
            headers=self._build_headers_with_global_headers(kwargs),
            params=kwargs,
        )
        self.raise_from_response(r)
        return r.json()

    async def delete_async(self, id_: str, **kwargs: Any) -> None:
        """Delete a device asynchronously.

        Args:
            id_: Device ID
            **kwargs: Additional parameters

        Raises:
            ProvdError: If the request fails

        """
        url = f"{self.base_url}/devices/{id_}"
        r = await self.async_client.delete(
            url, headers=self._build_headers_with_global_headers(kwargs), params=kwargs
        )
        self.raise_from_response(r)

    def delete(self, id_: str, **kwargs: Any) -> None:
        """Delete a device.

        Args:
            id_: Device ID
            **kwargs: Additional parameters

        Raises:
            ProvdError: If the request fails

        """
        url = f"{self.base_url}/devices/{id_}"
        r = self.sync_client.delete(
            url, headers=self._build_headers_with_global_headers(kwargs), params=kwargs
        )
        self.raise_from_response(r)

    async def synchronize_async(self, id_: str, **kwargs: Any) -> OperationInProgress:
        """Synchronize a device asynchronously.

        Args:
            id_: Device ID
            **kwargs: Additional parameters

        Returns:
            Operation tracking object

        Raises:
            ProvdError: If the request fails

        """
        url = f"{self.base_url}/synchronize"
        r = await self.async_client.post(
            url,
            json={"id": id_},
            headers=self._build_headers_with_global_headers(kwargs),
            params=kwargs,
        )
        self.raise_from_response(r)
        return OperationInProgress(self, r.headers["Location"])

    def synchronize(self, id_: str, **kwargs: Any) -> OperationInProgress:
        """Synchronize a device.

        Args:
            id_: Device ID
            **kwargs: Additional parameters

        Returns:
            Operation tracking object

        Raises:
            ProvdError: If the request fails

        """
        url = f"{self.base_url}/synchronize"
        r = self.sync_client.post(
            url,
            json={"id": id_},
            headers=self._build_headers_with_global_headers(kwargs),
            params=kwargs,
        )
        self.raise_from_response(r)
        return OperationInProgress(self, r.headers["Location"])

    async def reconfigure_async(self, id_: str, **kwargs: Any) -> None:
        """Reconfigure a device asynchronously.

        Args:
            id_: Device ID
            **kwargs: Additional parameters

        Raises:
            ProvdError: If the request fails

        """
        url = f"{self.base_url}/reconfigure"
        r = await self.async_client.post(
            url,
            json={"id": id_},
            headers=self._build_headers_with_global_headers(kwargs),
            params=kwargs,
        )
        self.raise_from_response(r)

    def reconfigure(self, id_: str, **kwargs: Any) -> None:
        """Reconfigure a device.

        Args:
            id_: Device ID
            **kwargs: Additional parameters

        Raises:
            ProvdError: If the request fails

        """
        url = f"{self.base_url}/reconfigure"
        r = self.sync_client.post(
            url,
            json={"id": id_},
            headers=self._build_headers_with_global_headers(kwargs),
            params=kwargs,
        )
        self.raise_from_response(r)

    async def create_from_dhcp_async(self, data: dict[str, Any], **kwargs: Any) -> None:
        """Create a device from DHCP information asynchronously.

        Args:
            data: DHCP information
            **kwargs: Additional parameters

        Raises:
            ProvdError: If the request fails

        """
        url = f"{self.base_url}/dhcpinfo"
        r = await self.async_client.post(
            url,
            json={"dhcp_info": data},
            headers=self._build_headers_with_global_headers(kwargs),
            params=kwargs,
        )
        self.raise_from_response(r)

    def create_from_dhcp(self, data: dict[str, Any], **kwargs: Any) -> None:
        """Create a device from DHCP information.

        Args:
            data: DHCP information
            **kwargs: Additional parameters

        Raises:
            ProvdError: If the request fails

        """
        url = f"{self.base_url}/dhcpinfo"
        r = self.sync_client.post(
            url,
            json={"dhcp_info": data},
            headers=self._build_headers_with_global_headers(kwargs),
            params=kwargs,
        )
        self.raise_from_response(r)
