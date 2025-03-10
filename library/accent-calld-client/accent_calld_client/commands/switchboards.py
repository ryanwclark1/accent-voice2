# Copyright 2025 Accent Communications

"""Commands for switchboard management in the Calld API.

This module provides commands for managing call switchboards.
"""

from __future__ import annotations

import logging
from typing import Any

from ..command import CalldCommand

logger = logging.getLogger(__name__)


class SwitchboardsCommand(CalldCommand):
    """Command for managing call switchboards.

    This command provides methods for listing and managing calls in switchboards.
    """

    resource = "switchboards"

    async def list_queued_calls_async(
        self, switchboard_uuid: str, tenant_uuid: str | None = None
    ) -> dict[str, Any]:
        """List queued calls for a switchboard asynchronously.

        Args:
            switchboard_uuid: UUID of the switchboard
            tenant_uuid: Optional tenant UUID

        Returns:
            Dictionary containing queued call information

        Raises:
            CalldError: If the API returns an error

        """
        headers = self._get_headers(tenant_uuid=tenant_uuid)
        url = self._client.url(self.resource, switchboard_uuid, "calls", "queued")
        r = await self.async_client.get(url, headers=headers)
        if r.status_code != 200:
            self.raise_from_response(r)

        return r.json()

    def list_queued_calls(
        self, switchboard_uuid: str, tenant_uuid: str | None = None
    ) -> dict[str, Any]:
        """List queued calls for a switchboard.

        Args:
            switchboard_uuid: UUID of the switchboard
            tenant_uuid: Optional tenant UUID

        Returns:
            Dictionary containing queued call information

        Raises:
            CalldError: If the API returns an error

        """
        headers = self._get_headers(tenant_uuid=tenant_uuid)
        url = self._client.url(self.resource, switchboard_uuid, "calls", "queued")
        r = self.sync_client.get(url, headers=headers)
        if r.status_code != 200:
            self.raise_from_response(r)

        return r.json()

    async def answer_queued_call_from_user_async(
        self, switchboard_uuid: str, call_id: str, line_id: str | None = None
    ) -> dict[str, Any]:
        """Answer a queued call as the current user asynchronously.

        Args:
            switchboard_uuid: UUID of the switchboard
            call_id: ID of the call to answer
            line_id: Optional line ID to use

        Returns:
            Answer data as a dictionary

        Raises:
            CalldError: If the API returns an error

        """
        headers = self._get_headers()
        url = self._client.url(
            self.resource, switchboard_uuid, "calls", "queued", call_id, "answer"
        )
        params = {"line_id": line_id} if line_id else None
        r = await self.async_client.put(url, params=params, headers=headers)
        if r.status_code != 200:
            self.raise_from_response(r)

        return r.json()

    def answer_queued_call_from_user(
        self, switchboard_uuid: str, call_id: str, line_id: str | None = None
    ) -> dict[str, Any]:
        """Answer a queued call as the current user.

        Args:
            switchboard_uuid: UUID of the switchboard
            call_id: ID of the call to answer
            line_id: Optional line ID to use

        Returns:
            Answer data as a dictionary

        Raises:
            CalldError: If the API returns an error

        """
        headers = self._get_headers()
        url = self._client.url(
            self.resource, switchboard_uuid, "calls", "queued", call_id, "answer"
        )
        params = {"line_id": line_id} if line_id else None
        r = self.sync_client.put(url, params=params, headers=headers)
        if r.status_code != 200:
            self.raise_from_response(r)

        return r.json()

    async def hold_call_async(
        self, switchboard_uuid: str, call_id: str, tenant_uuid: str | None = None
    ) -> None:
        """Put a call on hold in a switchboard asynchronously.

        Args:
            switchboard_uuid: UUID of the switchboard
            call_id: ID of the call to put on hold
            tenant_uuid: Optional tenant UUID

        Raises:
            CalldError: If the API returns an error

        """
        headers = self._get_headers(tenant_uuid=tenant_uuid)
        url = self._client.url(
            self.resource, switchboard_uuid, "calls", "held", call_id
        )
        r = await self.async_client.put(url, headers=headers)
        if r.status_code != 204:
            self.raise_from_response(r)

    def hold_call(
        self, switchboard_uuid: str, call_id: str, tenant_uuid: str | None = None
    ) -> None:
        """Put a call on hold in a switchboard.

        Args:
            switchboard_uuid: UUID of the switchboard
            call_id: ID of the call to put on hold
            tenant_uuid: Optional tenant UUID

        Raises:
            CalldError: If the API returns an error

        """
        headers = self._get_headers(tenant_uuid=tenant_uuid)
        url = self._client.url(
            self.resource, switchboard_uuid, "calls", "held", call_id
        )
        r = self.sync_client.put(url, headers=headers)
        if r.status_code != 204:
            self.raise_from_response(r)

    async def list_held_calls_async(
        self, switchboard_uuid: str, tenant_uuid: str | None = None
    ) -> dict[str, Any]:
        """List held calls for a switchboard asynchronously.

        Args:
            switchboard_uuid: UUID of the switchboard
            tenant_uuid: Optional tenant UUID

        Returns:
            Dictionary containing held call information

        Raises:
            CalldError: If the API returns an error

        """
        headers = self._get_headers(tenant_uuid=tenant_uuid)
        url = self._client.url(self.resource, switchboard_uuid, "calls", "held")
        r = await self.async_client.get(url, headers=headers)
        if r.status_code != 200:
            self.raise_from_response(r)

        return r.json()

    def list_held_calls(
        self, switchboard_uuid: str, tenant_uuid: str | None = None
    ) -> dict[str, Any]:
        """List held calls for a switchboard.

        Args:
            switchboard_uuid: UUID of the switchboard
            tenant_uuid: Optional tenant UUID

        Returns:
            Dictionary containing held call information

        Raises:
            CalldError: If the API returns an error

        """
        headers = self._get_headers(tenant_uuid=tenant_uuid)
        url = self._client.url(self.resource, switchboard_uuid, "calls", "held")
        r = self.sync_client.get(url, headers=headers)
        if r.status_code != 200:
            self.raise_from_response(r)

        return r.json()

    async def answer_held_call_from_user_async(
        self, switchboard_uuid: str, call_id: str, line_id: str | None = None
    ) -> dict[str, Any]:
        """Answer a held call as the current user asynchronously.

        Args:
            switchboard_uuid: UUID of the switchboard
            call_id: ID of the call to answer
            line_id: Optional line ID to use

        Returns:
            Answer data as a dictionary

        Raises:
            CalldError: If the API returns an error

        """
        headers = self._get_headers()
        url = self._client.url(
            self.resource, switchboard_uuid, "calls", "held", call_id, "answer"
        )
        params = {"line_id": line_id} if line_id else None
        r = await self.async_client.put(url, params=params, headers=headers)
        if r.status_code != 200:
            self.raise_from_response(r)

        return r.json()

    def answer_held_call_from_user(
        self, switchboard_uuid: str, call_id: str, line_id: str | None = None
    ) -> dict[str, Any]:
        """Answer a held call as the current user.

        Args:
            switchboard_uuid: UUID of the switchboard
            call_id: ID of the call to answer
            line_id: Optional line ID to use

        Returns:
            Answer data as a dictionary

        Raises:
            CalldError: If the API returns an error

        """
        headers = self._get_headers()
        url = self._client.url(
            self.resource, switchboard_uuid, "calls", "held", call_id, "answer"
        )
        params = {"line_id": line_id} if line_id else None
        r = self.sync_client.put(url, params=params, headers=headers)
        if r.status_code != 200:
            self.raise_from_response(r)

        return r.json()
