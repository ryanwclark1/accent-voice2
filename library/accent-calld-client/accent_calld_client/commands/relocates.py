# Copyright 2025 Accent Communications

"""Commands for call relocation management in the Calld API.

This module provides commands for creating and managing call relocations.
"""

from __future__ import annotations

import logging
from typing import Any

from accent_calld_client.command import CalldCommand

logger = logging.getLogger(__name__)


class RelocatesCommand(CalldCommand):
    """Command for managing call relocations.

    This command provides methods for listing, creating, and managing
    call relocations.
    """

    resource = "relocates"

    async def list_from_user_async(self) -> dict[str, Any]:
        """List relocations for the current user asynchronously.

        Returns:
            Dictionary containing relocation information

        Raises:
            CalldError: If the API returns an error

        """
        headers = self._get_headers()
        url = self._client.url("users", "me", self.resource)
        r = await self.async_client.get(url, headers=headers)
        if r.status_code != 200:
            self.raise_from_response(r)

        return r.json()

    def list_from_user(self) -> dict[str, Any]:
        """List relocations for the current user.

        Returns:
            Dictionary containing relocation information

        Raises:
            CalldError: If the API returns an error

        """
        headers = self._get_headers()
        url = self._client.url("users", "me", self.resource)
        r = self.sync_client.get(url, headers=headers)
        if r.status_code != 200:
            self.raise_from_response(r)

        return r.json()

    async def get_from_user_async(self, relocate_uuid: str) -> dict[str, Any]:
        """Get information about a specific relocation asynchronously.

        Args:
            relocate_uuid: UUID of the relocation

        Returns:
            Relocation data as a dictionary

        Raises:
            CalldError: If the API returns an error

        """
        headers = self._get_headers()
        url = self._client.url("users", "me", self.resource, relocate_uuid)
        r = await self.async_client.get(url, headers=headers)
        if r.status_code != 200:
            self.raise_from_response(r)

        return r.json()

    def get_from_user(self, relocate_uuid: str) -> dict[str, Any]:
        """Get information about a specific relocation.

        Args:
            relocate_uuid: UUID of the relocation

        Returns:
            Relocation data as a dictionary

        Raises:
            CalldError: If the API returns an error

        """
        headers = self._get_headers()
        url = self._client.url("users", "me", self.resource, relocate_uuid)
        r = self.sync_client.get(url, headers=headers)
        if r.status_code != 200:
            self.raise_from_response(r)

        return r.json()

    async def create_from_user_async(
        self,
        initiator: str,
        destination: str,
        location: str | None = None,
        completions: list[str] | None = None,
        timeout: int | None = None,
        auto_answer: bool | None = None,
    ) -> dict[str, Any]:
        """Create a new relocation asynchronously.

        Args:
            initiator: Call ID of the initiator
            destination: Destination for the relocation
            location: Optional location information
            completions: Optional completion data
            timeout: Optional timeout in seconds
            auto_answer: Whether to auto-answer

        Returns:
            Relocation data as a dictionary

        Raises:
            CalldError: If the API returns an error

        """
        body = {"initiator_call": initiator, "destination": destination}
        if location:
            body["location"] = location
        if completions:
            body["completions"] = completions
        if timeout:
            body["timeout"] = timeout
        if auto_answer:
            body["auto_answer"] = auto_answer

        headers = self._get_headers()
        url = self._client.url("users", "me", self.resource)
        r = await self.async_client.post(url, json=body, headers=headers)

        if r.status_code != 201:
            self.raise_from_response(r)

        return r.json()

    def create_from_user(
        self,
        initiator: str,
        destination: str,
        location: str | None = None,
        completions: list[str] | None = None,
        timeout: int | None = None,
        auto_answer: bool | None = None,
    ) -> dict[str, Any]:
        """Create a new relocation.

        Args:
            initiator: Call ID of the initiator
            destination: Destination for the relocation
            location: Optional location information
            completions: Optional completion data
            timeout: Optional timeout in seconds
            auto_answer: Whether to auto-answer

        Returns:
            Relocation data as a dictionary

        Raises:
            CalldError: If the API returns an error

        """
        body = {"initiator_call": initiator, "destination": destination}
        if location:
            body["location"] = location
        if completions:
            body["completions"] = completions
        if timeout:
            body["timeout"] = timeout
        if auto_answer:
            body["auto_answer"] = auto_answer

        headers = self._get_headers()
        url = self._client.url("users", "me", self.resource)
        r = self.sync_client.post(url, json=body, headers=headers)

        if r.status_code != 201:
            self.raise_from_response(r)

        return r.json()

    async def complete_from_user_async(self, relocate_uuid: str) -> None:
        """Complete a relocation asynchronously.

        Args:
            relocate_uuid: UUID of the relocation to complete

        Raises:
            CalldError: If the API returns an error

        """
        headers = self._get_headers()
        url = self._client.url("users", "me", self.resource, relocate_uuid, "complete")
        r = await self.async_client.put(url, headers=headers)
        if r.status_code != 204:
            self.raise_from_response(r)

    def complete_from_user(self, relocate_uuid: str) -> None:
        """Complete a relocation.

        Args:
            relocate_uuid: UUID of the relocation to complete

        Raises:
            CalldError: If the API returns an error

        """
        headers = self._get_headers()
        url = self._client.url("users", "me", self.resource, relocate_uuid, "complete")
        r = self.sync_client.put(url, headers=headers)
        if r.status_code != 204:
            self.raise_from_response(r)

    async def cancel_from_user_async(self, relocate_uuid: str) -> None:
        """Cancel a relocation asynchronously.

        Args:
            relocate_uuid: UUID of the relocation to cancel

        Raises:
            CalldError: If the API returns an error

        """
        headers = self._get_headers()
        url = self._client.url("users", "me", self.resource, relocate_uuid, "cancel")
        r = await self.async_client.put(url, headers=headers)
        if r.status_code != 204:
            self.raise_from_response(r)

    def cancel_from_user(self, relocate_uuid: str) -> None:
        """Cancel a relocation.

        Args:
            relocate_uuid: UUID of the relocation to cancel

        Raises:
            CalldError: If the API returns an error

        """
        headers = self._get_headers()
        url = self._client.url("users", "me", self.resource, relocate_uuid, "cancel")
        r = self.sync_client.put(url, headers=headers)
        if r.status_code != 204:
            self.raise_from_response(r)
