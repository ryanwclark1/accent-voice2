# Copyright 2025 Accent Communications

"""Devices command module for the Configuration Daemon API."""

import logging
from typing import Any

from accent_lib_rest_client import RESTCommand

from accent_confd_client.crud import MultiTenantCommand
from accent_confd_client.relations import LineDeviceRelation
from accent_confd_client.util import extract_id, url_join

# Configure standard logging
logger = logging.getLogger(__name__)


class DeviceRelation:
    """Relations for devices."""

    def __init__(self, builder: Any, device_id: str) -> None:
        """Initialize device relations.

        Args:
            builder: Client instance
            device_id: Device ID

        """
        self.device_id = device_id
        self.line_device = LineDeviceRelation(builder)

    @extract_id
    def add_line(self, line_id: str) -> Any:
        """Add a line to the device.

        Args:
            line_id: Line ID

        Returns:
            API response

        """
        return self.line_device.associate(line_id, self.device_id)

    @extract_id
    async def add_line_async(self, line_id: str) -> Any:
        """Add a line to the device asynchronously.

        Args:
            line_id: Line ID

        Returns:
            API response

        """
        return await self.line_device.associate_async(line_id, self.device_id)

    @extract_id
    def remove_line(self, line_id: str) -> Any:
        """Remove a line from the device.

        Args:
            line_id: Line ID

        Returns:
            API response

        """
        return self.line_device.dissociate(line_id, self.device_id)

    @extract_id
    async def remove_line_async(self, line_id: str) -> Any:
        """Remove a line from the device asynchronously.

        Args:
            line_id: Line ID

        Returns:
            API response

        """
        return await self.line_device.dissociate_async(line_id, self.device_id)

    def list_lines(self) -> list[dict[str, Any]]:
        """List lines for the device.

        Returns:
            List of lines

        """
        return self.line_device.list_by_device(self.device_id)

    async def list_lines_async(self) -> list[dict[str, Any]]:
        """List lines for the device asynchronously.

        Returns:
            List of lines

        """
        return await self.line_device.list_by_device_async(self.device_id)


class DevicesCommand(MultiTenantCommand):
    """Command for managing devices."""

    resource = "devices"
    relation_cmd = DeviceRelation

    @extract_id
    def autoprov(self, device_id: str, **kwargs: Any) -> None:
        """Auto-provision a device.

        Args:
            device_id: Device ID
            **kwargs: Additional parameters

        """
        tenant_uuid = kwargs.pop("tenant_uuid", self._client.config.tenant_uuid)
        headers = dict(kwargs.get("headers", self.session.READ_HEADERS))
        if tenant_uuid:
            headers["Accent-Tenant"] = tenant_uuid
        url = url_join(self.resource, device_id, "autoprov")
        self.session.get(url, headers=headers)

    @extract_id
    async def autoprov_async(self, device_id: str, **kwargs: Any) -> None:
        """Auto-provision a device asynchronously.

        Args:
            device_id: Device ID
            **kwargs: Additional parameters

        """
        tenant_uuid = kwargs.pop("tenant_uuid", self._client.config.tenant_uuid)
        headers = dict(kwargs.get("headers", self.session.READ_HEADERS))
        if tenant_uuid:
            headers["Accent-Tenant"] = tenant_uuid
        url = url_join(self.resource, device_id, "autoprov")
        await self.session.get_async(url, headers=headers)

    @extract_id
    def synchronize(self, device_id: str, **kwargs: Any) -> None:
        """Synchronize a device.

        Args:
            device_id: Device ID
            **kwargs: Additional parameters

        """
        tenant_uuid = kwargs.pop("tenant_uuid", self._client.config.tenant_uuid)
        headers = dict(kwargs.get("headers", self.session.READ_HEADERS))
        if tenant_uuid:
            headers["Accent-Tenant"] = tenant_uuid
        url = url_join(self.resource, device_id, "synchronize")
        self.session.get(url, headers=headers)

    @extract_id
    async def synchronize_async(self, device_id: str, **kwargs: Any) -> None:
        """Synchronize a device asynchronously.

        Args:
            device_id: Device ID
            **kwargs: Additional parameters

        """
        tenant_uuid = kwargs.pop("tenant_uuid", self._client.config.tenant_uuid)
        headers = dict(kwargs.get("headers", self.session.READ_HEADERS))
        if tenant_uuid:
            headers["Accent-Tenant"] = tenant_uuid
        url = url_join(self.resource, device_id, "synchronize")
        await self.session.get_async(url, headers=headers)


class UnallocatedDevicesCommand(RESTCommand):
    """Command for managing unallocated devices."""

    resource = "devices/unallocated"

    def list(self, **kwargs: Any) -> dict[str, Any]:
        """List unallocated devices.

        Args:
            **kwargs: Query parameters

        Returns:
            List of unallocated devices

        """
        url = url_join(self.resource)
        response = self.session.get(url, params=kwargs)
        return response.json()

    async def list_async(self, **kwargs: Any) -> dict[str, Any]:
        """List unallocated devices asynchronously.

        Args:
            **kwargs: Query parameters

        Returns:
            List of unallocated devices

        """
        url = url_join(self.resource)
        response = await self.session.get_async(url, params=kwargs)
        return response.json()

    def assign_tenant(self, device_id: str, **kwargs: Any) -> None:
        """Assign a device to a tenant.

        Args:
            device_id: Device ID
            **kwargs: Additional parameters

        """
        tenant_uuid = kwargs.pop("tenant_uuid", self._client.config.tenant_uuid)
        headers = dict(kwargs.get("headers", self.session.WRITE_HEADERS))
        if tenant_uuid:
            headers["Accent-Tenant"] = tenant_uuid
        url = url_join(self.resource, device_id)
        self.session.put(url, headers=headers)

    async def assign_tenant_async(self, device_id: str, **kwargs: Any) -> None:
        """Assign a device to a tenant asynchronously.

        Args:
            device_id: Device ID
            **kwargs: Additional parameters

        """
        tenant_uuid = kwargs.pop("tenant_uuid", self._client.config.tenant_uuid)
        headers = dict(kwargs.get("headers", self.session.WRITE_HEADERS))
        if tenant_uuid:
            headers["Accent-Tenant"] = tenant_uuid
        url = url_join(self.resource, device_id)
        await self.session.put_async(url, headers=headers)
