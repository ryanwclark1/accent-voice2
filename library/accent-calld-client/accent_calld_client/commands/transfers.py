# Copyright 2025 Accent Communications

"""Commands for call transfer management in the Calld API.

This module provides commands for creating and managing call transfers.
"""

from __future__ import annotations

import logging
from typing import Any

from accent_calld_client.command import CalldCommand

logger = logging.getLogger(__name__)


class TransfersCommand(CalldCommand):
    """Command for managing call transfers.

    This command provides methods for listing, creating, and managing
    call transfers.
    """

    resource = "transfers"

    async def list_transfers_from_user_async(self) -> dict[str, Any]:
        """List transfers for the current user asynchronously.

        Returns:
            Dictionary containing transfer information

        Raises:
            CalldError: If the API returns an error

        """
        headers = self._get_headers()
        url = self._client.url("users", "me", self.resource)
        r = await self.async_client.get(url, headers=headers)
        if r.status_code != 200:
            self.raise_from_response(r)

        return r.json()

    def list_transfers_from_user(self) -> dict[str, Any]:
        """List transfers for the current user.

        Returns:
            Dictionary containing transfer information

        Raises:
            CalldError: If the API returns an error

        """
        headers = self._get_headers()
        url = self._client.url("users", "me", self.resource)
        r = self.sync_client.get(url, headers=headers)
        if r.status_code != 200:
            self.raise_from_response(r)

        return r.json()

    async def get_transfer_async(self, transfer_id: str) -> dict[str, Any]:
        """Get information about a specific transfer asynchronously.

        Args:
            transfer_id: ID of the transfer

        Returns:
            Transfer data as a dictionary

        Raises:
            CalldError: If the API returns an error

        """
        headers = self._get_headers()
        url = self._client.url(self.resource, transfer_id)
        r = await self.async_client.get(url, headers=headers)
        if r.status_code != 200:
            self.raise_from_response(r)

        return r.json()

    def get_transfer(self, transfer_id: str) -> dict[str, Any]:
        """Get information about a specific transfer.

        Args:
            transfer_id: ID of the transfer

        Returns:
            Transfer data as a dictionary

        Raises:
            CalldError: If the API returns an error

        """
        headers = self._get_headers()
        url = self._client.url(self.resource, transfer_id)
        r = self.sync_client.get(url, headers=headers)
        if r.status_code != 200:
            self.raise_from_response(r)

        return r.json()

    async def make_transfer_async(
        self,
        transferred: str,
        initiator: str,
        context: str,
        exten: str,
        flow: str = "attended",
        variables: dict[str, str] | None = None,
        timeout: int | None = None,
    ) -> dict[str, Any]:
        """Create a new transfer asynchronously.

        Args:
            transferred: Call ID being transferred
            initiator: Call ID initiating the transfer
            context: Call context
            exten: Target extension
            flow: Transfer flow type (default: 'attended')
            variables: Optional variables for the transfer
            timeout: Optional timeout in seconds

        Returns:
            Transfer data as a dictionary

        Raises:
            CalldError: If the API returns an error

        """
        variables = variables or {}
        body = {
            "transferred_call": transferred,
            "initiator_call": initiator,
            "context": context,
            "exten": exten,
            "flow": flow,
            "variables": variables,
            "timeout": timeout,
        }
        headers = self._get_headers()
        url = self.base_url
        r = await self.async_client.post(url, json=body, headers=headers)

        if r.status_code != 201:
            self.raise_from_response(r)

        return r.json()

    def make_transfer(
        self,
        transferred: str,
        initiator: str,
        context: str,
        exten: str,
        flow: str = "attended",
        variables: dict[str, str] | None = None,
        timeout: int | None = None,
    ) -> dict[str, Any]:
        """Create a new transfer.

        Args:
            transferred: Call ID being transferred
            initiator: Call ID initiating the transfer
            context: Call context
            exten: Target extension
            flow: Transfer flow type (default: 'attended')
            variables: Optional variables for the transfer
            timeout: Optional timeout in seconds

        Returns:
            Transfer data as a dictionary

        Raises:
            CalldError: If the API returns an error

        """
        variables = variables or {}
        body = {
            "transferred_call": transferred,
            "initiator_call": initiator,
            "context": context,
            "exten": exten,
            "flow": flow,
            "variables": variables,
            "timeout": timeout,
        }
        headers = self._get_headers()
        url = self.base_url
        r = self.sync_client.post(url, json=body, headers=headers)

        if r.status_code != 201:
            self.raise_from_response(r)

        return r.json()

    async def make_transfer_from_user_async(
        self, exten: str, initiator: str, flow: str, timeout: int | None = None
    ) -> dict[str, Any]:
        """Create a new transfer as the current user asynchronously.

        Args:
            exten: Target extension
            initiator: Call ID initiating the transfer
            flow: Transfer flow type
            timeout: Optional timeout in seconds

        Returns:
            Transfer data as a dictionary

        Raises:
            CalldError: If the API returns an error

        """
        body = {
            "exten": exten,
            "initiator_call": initiator,
            "flow": flow,
            "timeout": timeout,
        }
        headers = self._get_headers()
        url = self._client.url("users", "me", self.resource)
        r = await self.async_client.post(url, json=body, headers=headers)
        if r.status_code != 201:
            self.raise_from_response(r)

        return r.json()

    def make_transfer_from_user(
        self, exten: str, initiator: str, flow: str, timeout: int | None = None
    ) -> dict[str, Any]:
        """Create a new transfer as the current user.

        Args:
            exten: Target extension
            initiator: Call ID initiating the transfer
            flow: Transfer flow type
            timeout: Optional timeout in seconds

        Returns:
            Transfer data as a dictionary

        Raises:
            CalldError: If the API returns an error

        """
        body = {
            "exten": exten,
            "initiator_call": initiator,
            "flow": flow,
            "timeout": timeout,
        }
        headers = self._get_headers()
        url = self._client.url("users", "me", self.resource)
        r = self.sync_client.post(url, json=body, headers=headers)
        if r.status_code != 201:
            self.raise_from_response(r)

        return r.json()

    async def complete_transfer_async(self, transfer_id: str) -> None:
        """Complete a transfer asynchronously.

        Args:
            transfer_id: ID of the transfer to complete

        Raises:
            CalldError: If the API returns an error

        """
        headers = self._get_headers()
        url = self._client.url(self.resource, transfer_id, "complete")
        r = await self.async_client.put(url, headers=headers)
        if r.status_code != 204:
            self.raise_from_response(r)

    def complete_transfer(self, transfer_id: str) -> None:
        """Complete a transfer.

        Args:
            transfer_id: ID of the transfer to complete

        Raises:
            CalldError: If the API returns an error

        """
        headers = self._get_headers()
        url = self._client.url(self.resource, transfer_id, "complete")
        r = self.sync_client.put(url, headers=headers)
        if r.status_code != 204:
            self.raise_from_response(r)

    async def complete_transfer_from_user_async(self, transfer_id: str) -> None:
        """Complete a transfer as the current user asynchronously.

        Args:
            transfer_id: ID of the transfer to complete

        Raises:
            CalldError: If the API returns an error

        """
        headers = self._get_headers()
        url = self._client.url("users", "me", self.resource, transfer_id, "complete")
        r = await self.async_client.put(url, headers=headers)
        if r.status_code != 204:
            self.raise_from_response(r)

    def complete_transfer_from_user(self, transfer_id: str) -> None:
        """Complete a transfer as the current user.

        Args:
            transfer_id: ID of the transfer to complete

        Raises:
            CalldError: If the API returns an error

        """
        headers = self._get_headers()
        url = self._client.url("users", "me", self.resource, transfer_id, "complete")
        r = self.sync_client.put(url, headers=headers)
        if r.status_code != 204:
            self.raise_from_response(r)

    async def cancel_transfer_async(self, transfer_id: str) -> None:
        """Cancel a transfer asynchronously.

        Args:
            transfer_id: ID of the transfer to cancel

        Raises:
            CalldError: If the API returns an error

        """
        headers = self._get_headers()
        url = self._client.url(self.resource, transfer_id)
        r = await self.async_client.delete(url, headers=headers)
        if r.status_code != 204:
            self.raise_from_response(r)

    def cancel_transfer(self, transfer_id: str) -> None:
        """Cancel a transfer.

        Args:
            transfer_id: ID of the transfer to cancel

        Raises:
            CalldError: If the API returns an error

        """
        headers = self._get_headers()
        url = self._client.url(self.resource, transfer_id)
        r = self.sync_client.delete(url, headers=headers)
        if r.status_code != 204:
            self.raise_from_response(r)

    async def cancel_transfer_from_user_async(self, transfer_id: str) -> None:
        """Cancel a transfer as the current user asynchronously.

        Args:
            transfer_id: ID of the transfer to cancel

        Raises:
            CalldError: If the API returns an error

        """
        headers = self._get_headers()
        url = self._client.url("users", "me", self.resource, transfer_id)
        r = await self.async_client.delete(url, headers=headers)
        if r.status_code != 204:
            self.raise_from_response(r)

    def cancel_transfer_from_user(self, transfer_id: str) -> None:
        """Cancel a transfer as the current user.

        Args:
            transfer_id: ID of the transfer to cancel

        Raises:
            CalldError: If the API returns an error

        """
        headers = self._get_headers()
        url = self._client.url("users", "me", self.resource, transfer_id)
        r = self.sync_client.delete(url, headers=headers)
        if r.status_code != 204:
            self.raise_from_response(r)
