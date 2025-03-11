# Copyright 2025 Accent Communications

"""Commands for meeting management in the Calld API.

This module provides commands for creating and managing meetings.
"""

from __future__ import annotations

import logging
from typing import Any

from accent_calld_client.command import CalldCommand

logger = logging.getLogger(__name__)


class MeetingsCommand(CalldCommand):
    """Command for managing meetings.

    This command provides methods for listing, creating, and managing
    meetings and their participants.
    """

    resource = "meetings"

    async def guest_status_async(self, meeting_uuid: str) -> dict[str, Any]:
        """Get guest status for a meeting asynchronously.

        Args:
            meeting_uuid: UUID of the meeting

        Returns:
            Dictionary containing guest status information

        Raises:
            CalldError: If the API returns an error

        """
        headers = self._get_headers()
        url = self._client.url(
            "guests",
            "me",
            self.resource,
            meeting_uuid,
            "status",
        )
        r = await self.async_client.get(url, headers=headers)
        if r.status_code != 200:
            self.raise_from_response(r)

        return r.json()

    def guest_status(self, meeting_uuid: str) -> dict[str, Any]:
        """Get guest status for a meeting.

        Args:
            meeting_uuid: UUID of the meeting

        Returns:
            Dictionary containing guest status information

        Raises:
            CalldError: If the API returns an error

        """
        headers = self._get_headers()
        url = self._client.url(
            "guests",
            "me",
            self.resource,
            meeting_uuid,
            "status",
        )
        r = self.sync_client.get(url, headers=headers)
        if r.status_code != 200:
            self.raise_from_response(r)

        return r.json()

    async def list_participants_async(self, meeting_uuid: str) -> dict[str, Any]:
        """List participants in a meeting asynchronously.

        Args:
            meeting_uuid: UUID of the meeting

        Returns:
            Dictionary containing participant information

        Raises:
            CalldError: If the API returns an error

        """
        headers = self._get_headers()
        url = self._client.url(self.resource, meeting_uuid, "participants")
        r = await self.async_client.get(url, headers=headers)
        if r.status_code != 200:
            self.raise_from_response(r)

        return r.json()

    def list_participants(self, meeting_uuid: str) -> dict[str, Any]:
        """List participants in a meeting.

        Args:
            meeting_uuid: UUID of the meeting

        Returns:
            Dictionary containing participant information

        Raises:
            CalldError: If the API returns an error

        """
        headers = self._get_headers()
        url = self._client.url(self.resource, meeting_uuid, "participants")
        r = self.sync_client.get(url, headers=headers)
        if r.status_code != 200:
            self.raise_from_response(r)

        return r.json()

    async def user_list_participants_async(self, meeting_uuid: str) -> dict[str, Any]:
        """List participants in a user's meeting asynchronously.

        Args:
            meeting_uuid: UUID of the meeting

        Returns:
            Dictionary containing participant information

        Raises:
            CalldError: If the API returns an error

        """
        headers = self._get_headers()
        url = self._client.url(
            "users", "me", self.resource, meeting_uuid, "participants"
        )
        r = await self.async_client.get(url, headers=headers)
        if r.status_code != 200:
            self.raise_from_response(r)

        return r.json()

    def user_list_participants(self, meeting_uuid: str) -> dict[str, Any]:
        """List participants in a user's meeting.

        Args:
            meeting_uuid: UUID of the meeting

        Returns:
            Dictionary containing participant information

        Raises:
            CalldError: If the API returns an error

        """
        headers = self._get_headers()
        url = self._client.url(
            "users", "me", self.resource, meeting_uuid, "participants"
        )
        r = self.sync_client.get(url, headers=headers)
        if r.status_code != 200:
            self.raise_from_response(r)

        return r.json()

    async def kick_participant_async(
        self, meeting_uuid: str, participant_id: str
    ) -> None:
        """Kick a participant from a meeting asynchronously.

        Args:
            meeting_uuid: UUID of the meeting
            participant_id: ID of the participant to kick

        Raises:
            CalldError: If the API returns an error

        """
        headers = self._get_headers()
        url = self._client.url(
            self.resource, meeting_uuid, "participants", participant_id
        )
        r = await self.async_client.delete(url, headers=headers)
        if r.status_code != 200:
            self.raise_from_response(r)

    def kick_participant(self, meeting_uuid: str, participant_id: str) -> None:
        """Kick a participant from a meeting.

        Args:
            meeting_uuid: UUID of the meeting
            participant_id: ID of the participant to kick

        Raises:
            CalldError: If the API returns an error

        """
        headers = self._get_headers()
        url = self._client.url(
            self.resource, meeting_uuid, "participants", participant_id
        )
        r = self.sync_client.delete(url, headers=headers)
        if r.status_code != 200:
            self.raise_from_response(r)

    async def user_kick_participant_async(
        self, meeting_uuid: str, participant_id: str
    ) -> None:
        """Kick a participant from a user's meeting asynchronously.

        Args:
            meeting_uuid: UUID of the meeting
            participant_id: ID of the participant to kick

        Raises:
            CalldError: If the API returns an error

        """
        headers = self._get_headers()
        url = self._client.url(
            "users", "me", self.resource, meeting_uuid, "participants", participant_id
        )
        r = await self.async_client.delete(url, headers=headers)
        if r.status_code != 200:
            self.raise_from_response(r)

    def user_kick_participant(self, meeting_uuid: str, participant_id: str) -> None:
        """Kick a participant from a user's meeting.

        Args:
            meeting_uuid: UUID of the meeting
            participant_id: ID of the participant to kick

        Raises:
            CalldError: If the API returns an error

        """
        headers = self._get_headers()
        url = self._client.url(
            "users", "me", self.resource, meeting_uuid, "participants", participant_id
        )
        r = self.sync_client.delete(url, headers=headers)
        if r.status_code != 200:
            self.raise_from_response(r)
