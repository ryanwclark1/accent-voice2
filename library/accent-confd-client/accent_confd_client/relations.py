# Copyright 2025 Accent Communications

"""Relation commands for the Configuration Daemon API."""

import logging
from typing import Any

from accent_lib_rest_client import HTTPCommand

from accent_confd_client.util import url_join

# Configure standard logging
logger = logging.getLogger(__name__)


class UserLineRelation(HTTPCommand):
    """Relation between users and lines."""

    def associate(self, user_id: str, line_id: str) -> None:
        """Associate a user with a line.

        Args:
            user_id: User ID
            line_id: Line ID

        """
        url = url_join("users", user_id, "lines", line_id)
        self.sync_client.put(url)

    async def associate_async(self, user_id: str, line_id: str) -> None:
        """Associate a user with a line asynchronously.

        Args:
            user_id: User ID
            line_id: Line ID

        """
        url = url_join("users", user_id, "lines", line_id)
        await self.async_client.put(url)

    def dissociate(self, user_id: str, line_id: str) -> None:
        """Dissociate a user from a line.

        Args:
            user_id: User ID
            line_id: Line ID

        """
        url = url_join("users", user_id, "lines", line_id)
        self.sync_client.delete(url)

    async def dissociate_async(self, user_id: str, line_id: str) -> None:
        """Dissociate a user from a line asynchronously.

        Args:
            user_id: User ID
            line_id: Line ID

        """
        url = url_join("users", user_id, "lines", line_id)
        await self.async_client.delete(url)

    def update_lines(self, user_id: str, lines: list[dict[str, Any]]) -> None:
        """Update lines for a user.

        Args:
            user_id: User ID
            lines: List of line data

        """
        url = url_join("users", user_id, "lines")
        body = {"lines": [{"id": line["id"]} for line in lines]}
        self.sync_client.put(url, json=body)

    async def update_lines_async(
        self, user_id: str, lines: list[dict[str, Any]]
    ) -> None:
        """Update lines for a user asynchronously.

        Args:
            user_id: User ID
            lines: List of line data

        """
        url = url_join("users", user_id, "lines")
        body = {"lines": [{"id": line["id"]} for line in lines]}
        await self.async_client.put(url, json=body)


class UserEndpointSipRelation(HTTPCommand):
    """Relation between users and SIP endpoints."""

    def get_by_user_line(
        self, user_uuid: str, line_id: str, view: str | None = None
    ) -> dict[str, Any]:
        """Get SIP endpoint for a user's line.

        Args:
            user_uuid: User UUID
            line_id: Line ID
            view: View type

        Returns:
            SIP endpoint data

        """
        url = url_join(
            "users", user_uuid, "lines", line_id, "associated", "endpoints", "sip"
        )
        params = {}
        if view:
            params["view"] = view
        response = self.sync_client.get(url, params=params)
        response.raise_for_status()
        return response.json()

    async def get_by_user_line_async(
        self, user_uuid: str, line_id: str, view: str | None = None
    ) -> dict[str, Any]:
        """Get SIP endpoint for a user's line asynchronously.

        Args:
            user_uuid: User UUID
            line_id: Line ID
            view: View type

        Returns:
            SIP endpoint data

        """
        url = url_join(
            "users", user_uuid, "lines", line_id, "associated", "endpoints", "sip"
        )
        params = {}
        if view:
            params["view"] = view
        response = await self.async_client.get(url, params=params)
        response.raise_for_status()
        return response.json()


class LineDeviceRelation(HTTPCommand):
    """Relation between lines and devices."""

    def associate(self, line_id: str, device_id: str) -> None:
        """Associate a line with a device.

        Args:
            line_id: Line ID
            device_id: Device ID

        """
        url = url_join("lines", line_id, "devices", device_id)
        self.sync_client.put(url)

    async def associate_async(self, line_id: str, device_id: str) -> None:
        """Associate a line with a device asynchronously.

        Args:
            line_id: Line ID
            device_id: Device ID

        """
        url = url_join("lines", line_id, "devices", device_id)
        await self.async_client.put(url)

    def dissociate(self, line_id: str, device_id: str) -> None:
        """Dissociate a line from a device.

        Args:
            line_id: Line ID
            device_id: Device ID

        """
        url = url_join("lines", line_id, "devices", device_id)
        self.sync_client.delete(url)

    async def dissociate_async(self, line_id: str, device_id: str) -> None:
        """Dissociate a line from a device asynchronously.

        Args:
            line_id: Line ID
            device_id: Device ID

        """
        url = url_join("lines", line_id, "devices", device_id)
        await self.async_client.delete(url)

    def get_by_line(self, line_id: str) -> dict[str, Any]:
        """Get devices for a line.

        Args:
            line_id: Line ID

        Returns:
            Devices data

        """
        url = url_join("lines", line_id, "devices")
        response = self.sync_client.get(url)
        response.raise_for_status()
        return response.json()

    async def get_by_line_async(self, line_id: str) -> dict[str, Any]:
        """Get devices for a line asynchronously.

        Args:
            line_id: Line ID

        Returns:
            Devices data

        """
        url = url_join("lines", line_id, "devices")
        response = await self.async_client.get(url)
        response.raise_for_status()
        return response.json()

    def list_by_device(self, device_id: str) -> dict[str, Any]:
        """List lines for a device.

        Args:
            device_id: Device ID

        Returns:
            Lines data

        """
        url = url_join("devices", device_id, "lines")
        response = self.sync_client.get(url)
        response.raise_for_status()
        return response.json()

    async def list_by_device_async(self, device_id: str) -> dict[str, Any]:
        """List lines for a device asynchronously.

        Args:
            device_id: Device ID

        Returns:
            Lines data

        """
        url = url_join("devices", device_id, "lines")
        response = await self.async_client.get(url)
        response.raise_for_status()
        return response.json()


class UserFuncKeyRelation(HTTPCommand):
    """Relation between users and function keys."""

    def update_funckey(
        self, user_id: str, position: str, funckey: dict[str, Any]
    ) -> None:
        """Update a function key for a user.

        Args:
            user_id: User ID
            position: Function key position
            funckey: Function key data

        """
        url = url_join("users", user_id, "funckeys", position)
        self.sync_client.put(url, json=funckey)

    async def update_funckey_async(
        self, user_id: str, position: str, funckey: dict[str, Any]
    ) -> None:
        """Update a function key for a user asynchronously.

        Args:
            user_id: User ID
            position: Function key position
            funckey: Function key data

        """
        url = url_join("users", user_id, "funckeys", position)
        await self.async_client.put(url, json=funckey)

    def remove_funckey(self, user_id: str, position: str) -> None:
        """Remove a function key from a user.

        Args:
            user_id: User ID
            position: Function key position

        """
        url = url_join("users", user_id, "funckeys", position)
        self.sync_client.delete(url)

    async def remove_funckey_async(self, user_id: str, position: str) -> None:
        """Remove a function key from a user asynchronously.

        Args:
            user_id: User ID
            position: Function key position

        """
        url = url_join("users", user_id, "funckeys", position)
        await self.async_client.delete(url)

    def get_funckey(self, user_id: str, position: str) -> dict[str, Any]:
        """Get a function key for a user.

        Args:
            user_id: User ID
            position: Function key position

        Returns:
            Function key data

        """
        url = url_join("users", user_id, "funckeys", position)
        response = self.sync_client.get(url)
        response.raise_for_status()
        return response.json()

    async def get_funckey_async(self, user_id: str, position: str) -> dict[str, Any]:
        """Get a function key for a user asynchronously.

        Args:
            user_id: User ID
            position: Function key position

        Returns:
            Function key data

        """
        url = url_join("users", user_id, "funckeys", position)
        response = await self.async_client.get(url)
        response.raise_for_status()
        return response.json()
