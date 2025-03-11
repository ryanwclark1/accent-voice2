# Copyright 2025 Accent Communications

"""Commands for ad-hoc conference management in the Calld API.

This module provides commands for creating and managing ad-hoc conferences.
"""

from __future__ import annotations

import logging
from typing import Any

from accent_calld_client.command import CalldCommand

logger = logging.getLogger(__name__)


class AdhocConferencesCommand(CalldCommand):
    """Command for managing ad-hoc conferences.

    This command provides methods for creating, deleting, and managing
    participants in ad-hoc conferences.
    """

    resource = "adhoc_conferences"

    async def create_from_user_async(
        self, host_call_id: str, *participant_call_ids: str
    ) -> dict[str, Any]:
        """Create an ad-hoc conference from user asynchronously.

        Args:
            host_call_id: Call ID of the conference host
            *participant_call_ids: Call IDs of the participants

        Returns:
            Conference data as a dictionary

        Raises:
            CalldError: If the API returns an error

        """
        body = {
            "host_call_id": host_call_id,
            "participant_call_ids": participant_call_ids,
        }
        headers = self._get_headers()
        url = self._client.url("users", "me", "conferences", "adhoc")
        r = await self.async_client.post(url, json=body, headers=headers)

        if r.status_code != 201:
            self.raise_from_response(r)

        return r.json()

    def create_from_user(
        self, host_call_id: str, *participant_call_ids: str
    ) -> dict[str, Any]:
        """Create an ad-hoc conference from user.

        Args:
            host_call_id: Call ID of the conference host
            *participant_call_ids: Call IDs of the participants

        Returns:
            Conference data as a dictionary

        Raises:
            CalldError: If the API returns an error

        """
        body = {
            "host_call_id": host_call_id,
            "participant_call_ids": participant_call_ids,
        }
        headers = self._get_headers()
        url = self._client.url("users", "me", "conferences", "adhoc")
        r = self.sync_client.post(url, json=body, headers=headers)

        if r.status_code != 201:
            self.raise_from_response(r)

        return r.json()

    async def delete_from_user_async(self, adhoc_conference_id: str) -> None:
        """Delete an ad-hoc conference from user asynchronously.

        Args:
            adhoc_conference_id: ID of the ad-hoc conference to delete

        Raises:
            CalldError: If the API returns an error

        """
        headers = self._get_headers()
        url = self._client.url(
            "users",
            "me",
            "conferences",
            "adhoc",
            adhoc_conference_id,
        )
        r = await self.async_client.delete(url, headers=headers)

        if r.status_code != 204:
            self.raise_from_response(r)

    def delete_from_user(self, adhoc_conference_id: str) -> None:
        """Delete an ad-hoc conference from user.

        Args:
            adhoc_conference_id: ID of the ad-hoc conference to delete

        Raises:
            CalldError: If the API returns an error

        """
        headers = self._get_headers()
        url = self._client.url(
            "users",
            "me",
            "conferences",
            "adhoc",
            adhoc_conference_id,
        )
        r = self.sync_client.delete(url, headers=headers)

        if r.status_code != 204:
            self.raise_from_response(r)

    async def add_participant_from_user_async(
        self, adhoc_conference_id: str, call_id: str
    ) -> None:
        """Add a participant to an ad-hoc conference asynchronously.

        Args:
            adhoc_conference_id: ID of the ad-hoc conference
            call_id: Call ID of the participant to add

        Raises:
            CalldError: If the API returns an error

        """
        headers = self._get_headers()
        url = self._client.url(
            "users",
            "me",
            "conferences",
            "adhoc",
            adhoc_conference_id,
            "participants",
            call_id,
        )
        r = await self.async_client.put(url, headers=headers)

        if r.status_code != 204:
            self.raise_from_response(r)

    def add_participant_from_user(self, adhoc_conference_id: str, call_id: str) -> None:
        """Add a participant to an ad-hoc conference.

        Args:
            adhoc_conference_id: ID of the ad-hoc conference
            call_id: Call ID of the participant to add

        Raises:
            CalldError: If the API returns an error

        """
        headers = self._get_headers()
        url = self._client.url(
            "users",
            "me",
            "conferences",
            "adhoc",
            adhoc_conference_id,
            "participants",
            call_id,
        )
        r = self.sync_client.put(url, headers=headers)

        if r.status_code != 204:
            self.raise_from_response(r)

    async def remove_participant_from_user_async(
        self, adhoc_conference_id: str, call_id: str
    ) -> None:
        """Remove a participant from an ad-hoc conference asynchronously.

        Args:
            adhoc_conference_id: ID of the ad-hoc conference
            call_id: Call ID of the participant to remove

        Raises:
            CalldError: If the API returns an error

        """
        headers = self._get_headers()
        url = self._client.url(
            "users",
            "me",
            "conferences",
            "adhoc",
            adhoc_conference_id,
            "participants",
            call_id,
        )
        r = await self.async_client.delete(url, headers=headers)

        if r.status_code != 204:
            self.raise_from_response(r)

    def remove_participant_from_user(
        self, adhoc_conference_id: str, call_id: str
    ) -> None:
        """Remove a participant from an ad-hoc conference.

        Args:
            adhoc_conference_id: ID of the ad-hoc conference
            call_id: Call ID of the participant to remove

        Raises:
            CalldError: If the API returns an error

        """
        headers = self._get_headers()
        url = self._client.url(
            "users",
            "me",
            "conferences",
            "adhoc",
            adhoc_conference_id,
            "participants",
            call_id,
        )
        r = self.sync_client.delete(url, headers=headers)

        if r.status_code != 204:
            self.raise_from_response(r)
