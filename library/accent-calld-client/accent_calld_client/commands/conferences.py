# Copyright 2025 Accent Communications

"""Commands for conference management in the Calld API.

This module provides commands for listing, creating, and manipulating
conference participants.
"""

from __future__ import annotations

import logging
from typing import Any

from ..command import CalldCommand

logger = logging.getLogger(__name__)


class ConferencesCommand(CalldCommand):
    """Command for managing conferences.

    This command provides methods for listing, creating, and managing
    conferences and their participants.
    """

    resource = "conferences"

    async def list_participants_async(self, conference_id: str) -> dict[str, Any]:
        """List participants in a conference asynchronously.

        Args:
            conference_id: ID of the conference

        Returns:
            Dictionary containing participant information

        Raises:
            CalldError: If the API returns an error

        """
        headers = self._get_headers()
        url = self._client.url(self.resource, conference_id, "participants")
        r = await self.async_client.get(url, headers=headers)
        if r.status_code != 200:
            self.raise_from_response(r)

        return r.json()

    def list_participants(self, conference_id: str) -> dict[str, Any]:
        """List participants in a conference.

        Args:
            conference_id: ID of the conference

        Returns:
            Dictionary containing participant information

        Raises:
            CalldError: If the API returns an error

        """
        headers = self._get_headers()
        url = self._client.url(self.resource, conference_id, "participants")
        r = self.sync_client.get(url, headers=headers)
        if r.status_code != 200:
            self.raise_from_response(r)

        return r.json()

    async def user_list_participants_async(self, conference_id: str) -> dict[str, Any]:
        """List participants in a user's conference asynchronously.

        Args:
            conference_id: ID of the conference

        Returns:
            Dictionary containing participant information

        Raises:
            CalldError: If the API returns an error

        """
        headers = self._get_headers()
        url = self._client.url(
            "users", "me", self.resource, conference_id, "participants"
        )
        r = await self.async_client.get(url, headers=headers)
        if r.status_code != 200:
            self.raise_from_response(r)

        return r.json()

    def user_list_participants(self, conference_id: str) -> dict[str, Any]:
        """List participants in a user's conference.

        Args:
            conference_id: ID of the conference

        Returns:
            Dictionary containing participant information

        Raises:
            CalldError: If the API returns an error

        """
        headers = self._get_headers()
        url = self._client.url(
            "users", "me", self.resource, conference_id, "participants"
        )
        r = self.sync_client.get(url, headers=headers)
        if r.status_code != 200:
            self.raise_from_response(r)

        return r.json()

    async def kick_participant_async(
        self, conference_id: str, participant_id: str
    ) -> None:
        """Kick a participant from a conference asynchronously.

        Args:
            conference_id: ID of the conference
            participant_id: ID of the participant to kick

        Raises:
            CalldError: If the API returns an error

        """
        headers = self._get_headers()
        url = self._client.url(
            self.resource, conference_id, "participants", participant_id
        )
        r = await self.async_client.delete(url, headers=headers)
        if r.status_code != 204:
            self.raise_from_response(r)

    def kick_participant(self, conference_id: str, participant_id: str) -> None:
        """Kick a participant from a conference.

        Args:
            conference_id: ID of the conference
            participant_id: ID of the participant to kick

        Raises:
            CalldError: If the API returns an error

        """
        headers = self._get_headers()
        url = self._client.url(
            self.resource, conference_id, "participants", participant_id
        )
        r = self.sync_client.delete(url, headers=headers)
        if r.status_code != 204:
            self.raise_from_response(r)

    async def mute_participant_async(
        self, conference_id: str, participant_id: str
    ) -> None:
        """Mute a participant in a conference asynchronously.

        Args:
            conference_id: ID of the conference
            participant_id: ID of the participant to mute

        Raises:
            CalldError: If the API returns an error

        """
        headers = self._get_headers()
        url = self._client.url(
            self.resource, conference_id, "participants", participant_id, "mute"
        )
        r = await self.async_client.put(url, headers=headers)
        if r.status_code != 204:
            self.raise_from_response(r)

    def mute_participant(self, conference_id: str, participant_id: str) -> None:
        """Mute a participant in a conference.

        Args:
            conference_id: ID of the conference
            participant_id: ID of the participant to mute

        Raises:
            CalldError: If the API returns an error

        """
        headers = self._get_headers()
        url = self._client.url(
            self.resource, conference_id, "participants", participant_id, "mute"
        )
        r = self.sync_client.put(url, headers=headers)
        if r.status_code != 204:
            self.raise_from_response(r)

    async def unmute_participant_async(
        self, conference_id: str, participant_id: str
    ) -> None:
        """Unmute a participant in a conference asynchronously.

        Args:
            conference_id: ID of the conference
            participant_id: ID of the participant to unmute

        Raises:
            CalldError: If the API returns an error

        """
        headers = self._get_headers()
        url = self._client.url(
            self.resource, conference_id, "participants", participant_id, "unmute"
        )
        r = await self.async_client.put(url, headers=headers)
        if r.status_code != 204:
            self.raise_from_response(r)

    def unmute_participant(self, conference_id: str, participant_id: str) -> None:
        """Unmute a participant in a conference.

        Args:
            conference_id: ID of the conference
            participant_id: ID of the participant to unmute

        Raises:
            CalldError: If the API returns an error

        """
        headers = self._get_headers()
        url = self._client.url(
            self.resource, conference_id, "participants", participant_id, "unmute"
        )
        r = self.sync_client.put(url, headers=headers)
        if r.status_code != 204:
            self.raise_from_response(r)

    async def record_async(self, conference_id: str) -> None:
        """Start recording a conference asynchronously.

        Args:
            conference_id: ID of the conference to record

        Raises:
            CalldError: If the API returns an error

        """
        headers = self._get_headers()
        url = self._client.url(self.resource, conference_id, "record")
        r = await self.async_client.post(url, headers=headers)
        if r.status_code != 204:
            self.raise_from_response(r)

    def record(self, conference_id: str) -> None:
        """Start recording a conference.

        Args:
            conference_id: ID of the conference to record

        Raises:
            CalldError: If the API returns an error

        """
        headers = self._get_headers()
        url = self._client.url(self.resource, conference_id, "record")
        r = self.sync_client.post(url, headers=headers)
        if r.status_code != 204:
            self.raise_from_response(r)

    async def stop_record_async(self, conference_id: str) -> None:
        """Stop recording a conference asynchronously.

        Args:
            conference_id: ID of the conference to stop recording

        Raises:
            CalldError: If the API returns an error

        """
        headers = self._get_headers()
        url = self._client.url(self.resource, conference_id, "record")
        r = await self.async_client.delete(url, headers=headers)
        if r.status_code != 204:
            self.raise_from_response(r)

    def stop_record(self, conference_id: str) -> None:
        """Stop recording a conference.

        Args:
            conference_id: ID of the conference to stop recording

        Raises:
            CalldError: If the API returns an error

        """
        headers = self._get_headers()
        url = self._client.url(self.resource, conference_id, "record")
        r = self.sync_client.delete(url, headers=headers)
        if r.status_code != 204:
            self.raise_from_response(r)
