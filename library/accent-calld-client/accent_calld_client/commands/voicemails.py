# Copyright 2025 Accent Communications

"""Commands for voicemail management in the Calld API.

This module provides commands for accessing and managing voicemails.
"""

from __future__ import annotations

import logging
from typing import Any

import httpx

from accent_calld_client.command import CalldCommand

logger = logging.getLogger(__name__)


class VoicemailsCommand(CalldCommand):
    """Command for managing voicemails.

    This command provides methods for accessing, creating, and managing
    voicemails, messages, and greetings.
    """

    resource = "voicemails"
    headers = {"Accept": "application/json", "Content-Type": "application/json"}

    async def get_voicemail_async(self, voicemail_id: str) -> dict[str, Any]:
        """Get information about a specific voicemail asynchronously.

        Args:
            voicemail_id: ID of the voicemail

        Returns:
            Voicemail data as a dictionary

        Raises:
            CalldError: If the API returns an error

        """
        url = self._client.url(self.resource, voicemail_id)
        return await self._get_async(url)

    def get_voicemail(self, voicemail_id: str) -> dict[str, Any]:
        """Get information about a specific voicemail.

        Args:
            voicemail_id: ID of the voicemail

        Returns:
            Voicemail data as a dictionary

        Raises:
            CalldError: If the API returns an error

        """
        url = self._client.url(self.resource, voicemail_id)
        return self._get(url)

    async def get_voicemail_from_user_async(self) -> dict[str, Any]:
        """Get information about the current user's voicemail asynchronously.

        Returns:
            Voicemail data as a dictionary

        Raises:
            CalldError: If the API returns an error

        """
        url = self._client.url("users", "me", "voicemails")
        return await self._get_async(url)

    def get_voicemail_from_user(self) -> dict[str, Any]:
        """Get information about the current user's voicemail.

        Returns:
            Voicemail data as a dictionary

        Raises:
            CalldError: If the API returns an error

        """
        url = self._client.url("users", "me", "voicemails")
        return self._get(url)

    async def get_voicemail_folder_async(self, voicemail_id: str, folder_id: str) -> dict[str, Any]:
        """Get information about a specific voicemail folder asynchronously.

        Args:
            voicemail_id: ID of the voicemail
            folder_id: ID of the folder

        Returns:
            Folder data as a dictionary

        Raises:
            CalldError: If the API returns an error

        """
        url = self._client.url(self.resource, voicemail_id, "folders", folder_id)
        return await self._get_async(url)

    def get_voicemail_folder(self, voicemail_id: str, folder_id: str) -> dict[str, Any]:
        """Get information about a specific voicemail folder.

        Args:
            voicemail_id: ID of the voicemail
            folder_id: ID of the folder

        Returns:
            Folder data as a dictionary

        Raises:
            CalldError: If the API returns an error

        """
        url = self._client.url(self.resource, voicemail_id, "folders", folder_id)
        return self._get(url)

    async def get_voicemail_folder_from_user_async(self, folder_id: str) -> dict[str, Any]:
        """Get information about a specific user voicemail folder asynchronously.

        Args:
            folder_id: ID of the folder

        Returns:
            Folder data as a dictionary

        Raises:
            CalldError: If the API returns an error

        """
        url = self._client.url("users", "me", "voicemails", "folders", folder_id)
        return await self._get_async(url)

    def get_voicemail_folder_from_user(self, folder_id: str) -> dict[str, Any]:
        """Get information about a specific user voicemail folder.

        Args:
            folder_id: ID of the folder

        Returns:
            Folder data as a dictionary

        Raises:
            CalldError: If the API returns an error

        """
        url = self._client.url("users", "me", "voicemails", "folders", folder_id)
        return self._get(url)

    async def get_voicemail_message_async(self, voicemail_id: str, message_id: str) -> dict[str, Any]:
        """Get information about a specific voicemail message asynchronously.

        Args:
            voicemail_id: ID of the voicemail
            message_id: ID of the message

        Returns:
            Message data as a dictionary

        Raises:
            CalldError: If the API returns an error

        """
        url = self._client.url(self.resource, voicemail_id, "messages", message_id)
        return await self._get_async(url)

    def get_voicemail_message(self, voicemail_id: str, message_id: str) -> dict[str, Any]:
        """Get information about a specific voicemail message.

        Args:
            voicemail_id: ID of the voicemail
            message_id: ID of the message

        Returns:
            Message data as a dictionary

        Raises:
            CalldError: If the API returns an error

        """
        url = self._client.url(self.resource, voicemail_id, "messages", message_id)
        return self._get(url)

    async def get_voicemail_message_from_user_async(self, message_id: str) -> dict[str, Any]:
        """Get information about a specific user voicemail message asynchronously.

        Args:
            message_id: ID of the message

        Returns:
            Message data as a dictionary

        Raises:
            CalldError: If the API returns an error

        """
        url = self._client.url("users", "me", "voicemails", "messages", message_id)
        return await self._get_async(url)

    def get_voicemail_message_from_user(self, message_id: str) -> dict[str, Any]:
        """Get information about a specific user voicemail message.

        Args:
            message_id: ID of the message

        Returns:
            Message data as a dictionary

        Raises:
            CalldError: If the API returns an error

        """
        url = self._client.url("users", "me", "voicemails", "messages", message_id)
        return self._get(url)

    async def delete_voicemail_message_async(
        self, voicemail_id: str, message_id: str
    ) -> None:
        """Delete a voicemail message asynchronously.

        Args:
            voicemail_id: ID of the voicemail
            message_id: ID of the message to delete

        Raises:
            CalldError: If the API returns an error

        """
        headers = self._get_headers()
        url = self._client.url(self.resource, voicemail_id, "messages", message_id)
        r = await self.async_client.delete(url, headers=headers)
        if r.status_code != 204:
            self.raise_from_response(r)

    def delete_voicemail_message(self, voicemail_id: str, message_id: str) -> None:
        """Delete a voicemail message.

        Args:
            voicemail_id: ID of the voicemail
            message_id: ID of the message to delete

        Raises:
            CalldError: If the API returns an error

        """
        headers = self._get_headers()
        url = self._client.url(self.resource, voicemail_id, "messages", message_id)
        r = self.sync_client.delete(url, headers=headers)
        if r.status_code != 204:
            self.raise_from_response(r)

    async def delete_voicemail_message_from_user_async(self, message_id: str) -> None:
        """Delete a voicemail message as the current user asynchronously.

        Args:
            message_id: ID of the message to delete

        Raises:
            CalldError: If the API returns an error

        """
        headers = self._get_headers()
        url = self._client.url("users", "me", "voicemails", "messages", message_id)
        r = await self.async_client.delete(url, headers=headers)
        if r.status_code != 204:
            self.raise_from_response(r)

    def delete_voicemail_message_from_user(self, message_id: str) -> None:
        """Delete a voicemail message as the current user.

        Args:
            message_id: ID of the message to delete

        Raises:
            CalldError: If the API returns an error

        """
        headers = self._get_headers()
        url = self._client.url("users", "me", "voicemails", "messages", message_id)
        r = self.sync_client.delete(url, headers=headers)
        if r.status_code != 204:
            self.raise_from_response(r)

    async def move_voicemail_message_async(
        self, voicemail_id: str, message_id: str, dest_folder_id: str
    ) -> None:
        """Move a voicemail message to another folder asynchronously.

        Args:
            voicemail_id: ID of the voicemail
            message_id: ID of the message to move
            dest_folder_id: ID of the destination folder

        Raises:
            CalldError: If the API returns an error

        """
        url = self._client.url(self.resource, voicemail_id, "messages", message_id)
        await self._move_message_async(url, dest_folder_id)

    def move_voicemail_message(
        self, voicemail_id: str, message_id: str, dest_folder_id: str
    ) -> None:
        """Move a voicemail message to another folder.

        Args:
            voicemail_id: ID of the voicemail
            message_id: ID of the message to move
            dest_folder_id: ID of the destination folder

        Raises:
            CalldError: If the API returns an error

        """
        url = self._client.url(self.resource, voicemail_id, "messages", message_id)
        self._move_message(url, dest_folder_id)

    async def move_voicemail_message_from_user_async(
        self, message_id: str, dest_folder_id: str
    ) -> None:
        """Move a voicemail message as the current user asynchronously.

        Args:
            message_id: ID of the message to move
            dest_folder_id: ID of the destination folder

        Raises:
            CalldError: If the API returns an error

        """
        url = self._client.url("users", "me", "voicemails", "messages", message_id)
        await self._move_message_async(url, dest_folder_id)

    def move_voicemail_message_from_user(
        self, message_id: str, dest_folder_id: str
    ) -> None:
        """Move a voicemail message as the current user.

        Args:
            message_id: ID of the message to move
            dest_folder_id: ID of the destination folder

        Raises:
            CalldError: If the API returns an error

        """
        url = self._client.url("users", "me", "voicemails", "messages", message_id)
        self._move_message(url, dest_folder_id)

    async def _move_message_async(self, url: str, dest_folder_id: str) -> None:
        """Move a voicemail message to another folder asynchronously (helper method).

        Args:
            url: API URL for the message
            dest_folder_id: ID of the destination folder

        Raises:
            CalldError: If the API returns an error

        """
        headers = self._get_headers()
        body = {"folder_id": dest_folder_id}
        r = await self.async_client.put(url, json=body, headers=headers)
        if r.status_code != 204:
            self.raise_from_response(r)

    def _move_message(self, url: str, dest_folder_id: str) -> None:
        """Move a voicemail message to another folder (helper method).

        Args:
            url: API URL for the message
            dest_folder_id: ID of the destination folder

        Raises:
            CalldError: If the API returns an error

        """
        headers = self._get_headers()
        body = {"folder_id": dest_folder_id}
        r = self.sync_client.put(url, json=body, headers=headers)
        if r.status_code != 204:
            self.raise_from_response(r)

    async def get_voicemail_recording_async(
        self, voicemail_id: str, message_id: str
    ) -> bytes:
        """Get the recording of a voicemail message asynchronously.

        Args:
            voicemail_id: ID of the voicemail
            message_id: ID of the message

        Returns:
            Audio content as bytes

        Raises:
            CalldError: If the API returns an error

        """
        url = self._client.url(
            self.resource,
            voicemail_id,
            "messages",
            message_id,
            "recording",
        )
        return await self._get_recording_async(url)

    def get_voicemail_recording(self, voicemail_id: str, message_id: str) -> bytes:
        """Get the recording of a voicemail message.

        Args:
            voicemail_id: ID of the voicemail
            message_id: ID of the message

        Returns:
            Audio content as bytes

        Raises:
            CalldError: If the API returns an error

        """
        url = self._client.url(
            self.resource,
            voicemail_id,
            "messages",
            message_id,
            "recording",
        )
        return self._get_recording(url)

    async def get_voicemail_recording_from_user_async(self, message_id: str) -> bytes:
        """Get the recording of a user's voicemail message asynchronously.

        Args:
            message_id: ID of the message

        Returns:
            Audio content as bytes

        Raises:
            CalldError: If the API returns an error

        """
        url = self._client.url(
            "users", "me", "voicemails", "messages", message_id, "recording"
        )
        return await self._get_recording_async(url)

    def get_voicemail_recording_from_user(self, message_id: str) -> bytes:
        """Get the recording of a user's voicemail message.

        Args:
            message_id: ID of the message

        Returns:
            Audio content as bytes

        Raises:
            CalldError: If the API returns an error

        """
        url = self._client.url(
            "users", "me", "voicemails", "messages", message_id, "recording"
        )
        return self._get_recording(url)

    async def voicemail_greeting_exists_async(
        self, voicemail_id: str, greeting: str
    ) -> bool:
        """Check if a voicemail greeting exists asynchronously.

        Args:
            voicemail_id: ID of the voicemail
            greeting: Name of the greeting

        Returns:
            True if the greeting exists, False otherwise

        Raises:
            CalldError: If the API returns an error other than 404

        """
        headers = self._get_headers()
        url = self._client.url(self.resource, voicemail_id, "greetings", greeting)
        try:
            response = await self.async_client.head(url, headers=headers)
            # FIXME: invalid voicemail_id returns 400 instead of 404
            if response.status_code in (404, 400):
                return False
            if response.status_code != 200:
                self.raise_from_response(response)
            return True
        except httpx.HTTPStatusError as e:
            if e.response.status_code in (404, 400):
                return False
            raise

    def voicemail_greeting_exists(self, voicemail_id: str, greeting: str) -> bool:
        """Check if a voicemail greeting exists.

        Args:
            voicemail_id: ID of the voicemail
            greeting: Name of the greeting

        Returns:
            True if the greeting exists, False otherwise

        Raises:
            CalldError: If the API returns an error other than 404

        """
        headers = self._get_headers()
        url = self._client.url(self.resource, voicemail_id, "greetings", greeting)
        try:
            response = self.sync_client.head(url, headers=headers)
            # FIXME: invalid voicemail_id returns 400 instead of 404
            if response.status_code in (404, 400):
                return False
            if response.status_code != 200:
                self.raise_from_response(response)
            return True
        except httpx.HTTPStatusError as e:
            if e.response.status_code in (404, 400):
                return False
            raise

    async def get_voicemail_greeting_async(
        self, voicemail_id: str, greeting: str
    ) -> bytes:
        """Get a voicemail greeting asynchronously.

        Args:
            voicemail_id: ID of the voicemail
            greeting: Name of the greeting

        Returns:
            Audio content as bytes

        Raises:
            CalldError: If the API returns an error

        """
        url = self._client.url(self.resource, voicemail_id, "greetings", greeting)
        return await self._get_recording_async(url)

    def get_voicemail_greeting(self, voicemail_id: str, greeting: str) -> bytes:
        """Get a voicemail greeting.

        Args:
            voicemail_id: ID of the voicemail
            greeting: Name of the greeting

        Returns:
            Audio content as bytes

        Raises:
            CalldError: If the API returns an error

        """
        url = self._client.url(self.resource, voicemail_id, "greetings", greeting)
        return self._get_recording(url)

    async def voicemail_greeting_from_user_exists_async(self, greeting: str) -> bool:
        """Check if a user's voicemail greeting exists asynchronously.

        Args:
            greeting: Name of the greeting

        Returns:
            True if the greeting exists, False otherwise

        Raises:
            CalldError: If the API returns an error other than 404

        """
        headers = self._get_headers()
        url = self._client.url("users", "me", "voicemails", "greetings", greeting)
        try:
            response = await self.async_client.head(url, headers=headers)
            if response.status_code == 404:
                return False
            if response.status_code != 200:
                self.raise_from_response(response)
            return True
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                return False
            raise

    def voicemail_greeting_from_user_exists(self, greeting: str) -> bool:
        """Check if a user's voicemail greeting exists.

        Args:
            greeting: Name of the greeting

        Returns:
            True if the greeting exists, False otherwise

        Raises:
            CalldError: If the API returns an error other than 404

        """
        headers = self._get_headers()
        url = self._client.url("users", "me", "voicemails", "greetings", greeting)
        try:
            response = self.sync_client.head(url, headers=headers)
            if response.status_code == 404:
                return False
            if response.status_code != 200:
                self.raise_from_response(response)
            return True
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                return False
            raise

    async def get_voicemail_greeting_from_user_async(self, greeting: str) -> bytes:
        """Get a user's voicemail greeting asynchronously.

        Args:
            greeting: Name of the greeting

        Returns:
            Audio content as bytes

        Raises:
            CalldError: If the API returns an error

        """
        url = self._client.url("users", "me", "voicemails", "greetings", greeting)
        return await self._get_recording_async(url)

    def get_voicemail_greeting_from_user(self, greeting: str) -> bytes:
        """Get a user's voicemail greeting.

        Args:
            greeting: Name of the greeting

        Returns:
            Audio content as bytes

        Raises:
            CalldError: If the API returns an error

        """
        url = self._client.url("users", "me", "voicemails", "greetings", greeting)
        return self._get_recording(url)

    async def create_voicemail_greeting_async(
        self, voicemail_id: str, greeting: str, data: bytes
    ) -> None:
        """Create a voicemail greeting asynchronously.

        Args:
            voicemail_id: ID of the voicemail
            greeting: Name of the greeting
            data: Audio content as bytes

        Raises:
            CalldError: If the API returns an error

        """
        url = self._client.url(self.resource, voicemail_id, "greetings", greeting)
        await self._create_recording_async(url, data)

    def create_voicemail_greeting(
        self, voicemail_id: str, greeting: str, data: bytes
    ) -> None:
        """Create a voicemail greeting.

        Args:
            voicemail_id: ID of the voicemail
            greeting: Name of the greeting
            data: Audio content as bytes

        Raises:
            CalldError: If the API returns an error

        """
        url = self._client.url(self.resource, voicemail_id, "greetings", greeting)
        self._create_recording(url, data)

    async def create_voicemail_greeting_from_user_async(
        self, greeting: str, data: bytes
    ) -> None:
        """Create a user's voicemail greeting asynchronously.

        Args:
            greeting: Name of the greeting
            data: Audio content as bytes

        Raises:
            CalldError: If the API returns an error

        """
        url = self._client.url("users", "me", "voicemails", "greetings", greeting)
        await self._create_recording_async(url, data)

    def create_voicemail_greeting_from_user(self, greeting: str, data: bytes) -> None:
        """Create a user's voicemail greeting.

        Args:
            greeting: Name of the greeting
            data: Audio content as bytes

        Raises:
            CalldError: If the API returns an error

        """
        url = self._client.url("users", "me", "voicemails", "greetings", greeting)
        self._create_recording(url, data)

    async def update_voicemail_greeting_async(
        self, voicemail_id: str, greeting: str, data: bytes
    ) -> None:
        """Update a voicemail greeting asynchronously.

        Args:
            voicemail_id: ID of the voicemail
            greeting: Name of the greeting
            data: Audio content as bytes

        Raises:
            CalldError: If the API returns an error

        """
        url = self._client.url(self.resource, voicemail_id, "greetings", greeting)
        await self._put_recording_async(url, data)

    def update_voicemail_greeting(
        self, voicemail_id: str, greeting: str, data: bytes
    ) -> None:
        """Update a voicemail greeting.

        Args:
            voicemail_id: ID of the voicemail
            greeting: Name of the greeting
            data: Audio content as bytes

        Raises:
            CalldError: If the API returns an error

        """
        url = self._client.url(self.resource, voicemail_id, "greetings", greeting)
        self._put_recording(url, data)

    async def update_voicemail_greeting_from_user_async(
        self, greeting: str, data: bytes
    ) -> None:
        """Update a user's voicemail greeting asynchronously.

        Args:
            greeting: Name of the greeting
            data: Audio content as bytes

        Raises:
            CalldError: If the API returns an error

        """
        url = self._client.url("users", "me", "voicemails", "greetings", greeting)
        await self._put_recording_async(url, data)

    def update_voicemail_greeting_from_user(self, greeting: str, data: bytes) -> None:
        """Update a user's voicemail greeting.

        Args:
            greeting: Name of the greeting
            data: Audio content as bytes

        Raises:
            CalldError: If the API returns an error

        """
        url = self._client.url("users", "me", "voicemails", "greetings", greeting)
        self._put_recording(url, data)

    async def delete_voicemail_greeting_async(
        self, voicemail_id: str, greeting: str
    ) -> None:
        """Delete a voicemail greeting asynchronously.

        Args:
            voicemail_id: ID of the voicemail
            greeting: Name of the greeting to delete

        Raises:
            CalldError: If the API returns an error

        """
        headers = self._get_headers()
        url = self._client.url(self.resource, voicemail_id, "greetings", greeting)
        r = await self.async_client.delete(url, headers=headers)
        if r.status_code != 204:
            self.raise_from_response(r)

    def delete_voicemail_greeting(self, voicemail_id: str, greeting: str) -> None:
        """Delete a voicemail greeting.

        Args:
            voicemail_id: ID of the voicemail
            greeting: Name of the greeting to delete

        Raises:
            CalldError: If the API returns an error

        """
        headers = self._get_headers()
        url = self._client.url(self.resource, voicemail_id, "greetings", greeting)
        r = self.sync_client.delete(url, headers=headers)
        if r.status_code != 204:
            self.raise_from_response(r)

    async def delete_voicemail_greeting_from_user_async(self, greeting: str) -> None:
        """Delete a user's voicemail greeting asynchronously.

        Args:
            greeting: Name of the greeting to delete

        Raises:
            CalldError: If the API returns an error

        """
        headers = self._get_headers()
        url = self._client.url("users", "me", "voicemails", "greetings", greeting)
        r = await self.async_client.delete(url, headers=headers)
        if r.status_code != 204:
            self.raise_from_response(r)

    def delete_voicemail_greeting_from_user(self, greeting: str) -> None:
        """Delete a user's voicemail greeting.

        Args:
            greeting: Name of the greeting to delete

        Raises:
            CalldError: If the API returns an error

        """
        headers = self._get_headers()
        url = self._client.url("users", "me", "voicemails", "greetings", greeting)
        r = self.sync_client.delete(url, headers=headers)
        if r.status_code != 204:
            self.raise_from_response(r)

    async def copy_voicemail_greeting_async(
        self, voicemail_id: str, greeting: str, dest_greeting: str
    ) -> None:
        """Copy a voicemail greeting asynchronously.

        Args:
            voicemail_id: ID of the voicemail
            greeting: Name of the source greeting
            dest_greeting: Name of the destination greeting

        Raises:
            CalldError: If the API returns an error

        """
        headers = self._get_headers()
        url = self._client.url(
            self.resource, voicemail_id, "greetings", greeting, "copy"
        )
        body = {"dest_greeting": dest_greeting}
        r = await self.async_client.post(url, json=body, headers=headers)
        if r.status_code != 204:
            self.raise_from_response(r)

    def copy_voicemail_greeting(
        self, voicemail_id: str, greeting: str, dest_greeting: str
    ) -> None:
        """Copy a voicemail greeting.

        Args:
            voicemail_id: ID of the voicemail
            greeting: Name of the source greeting
            dest_greeting: Name of the destination greeting

        Raises:
            CalldError: If the API returns an error

        """
        headers = self._get_headers()
        url = self._client.url(
            self.resource, voicemail_id, "greetings", greeting, "copy"
        )
        body = {"dest_greeting": dest_greeting}
        r = self.sync_client.post(url, json=body, headers=headers)
        if r.status_code != 204:
            self.raise_from_response(r)

    async def copy_voicemail_greeting_from_user_async(
        self, greeting: str, dest_greeting: str
    ) -> None:
        """Copy a user's voicemail greeting asynchronously.

        Args:
            greeting: Name of the source greeting
            dest_greeting: Name of the destination greeting

        Raises:
            CalldError: If the API returns an error

        """
        headers = self._get_headers()
        url = self._client.url(
            "users", "me", "voicemails", "greetings", greeting, "copy"
        )
        body = {"dest_greeting": dest_greeting}
        r = await self.async_client.post(url, json=body, headers=headers)
        if r.status_code != 204:
            self.raise_from_response(r)

    def copy_voicemail_greeting_from_user(
        self, greeting: str, dest_greeting: str
    ) -> None:
        """Copy a user's voicemail greeting.

        Args:
            greeting: Name of the source greeting
            dest_greeting: Name of the destination greeting

        Raises:
            CalldError: If the API returns an error

        """
        headers = self._get_headers()
        url = self._client.url(
            "users", "me", "voicemails", "greetings", greeting, "copy"
        )
        body = {"dest_greeting": dest_greeting}
        r = self.sync_client.post(url, json=body, headers=headers)
        if r.status_code != 204:
            self.raise_from_response(r)

    async def _create_recording_async(self, url: str, data: bytes) -> None:
        """Create a recording asynchronously.

        Args:
            url: API URL for the recording
            data: Audio content as bytes

        Raises:
            CalldError: If the API returns an error

        """
        headers = self._get_headers()
        headers["Content-type"] = "audio/wav"
        r = await self.async_client.post(url, headers=headers, content=data)
        if r.status_code != 204:
            self.raise_from_response(r)

    def _create_recording(self, url: str, data: bytes) -> None:
        """Create a recording.

        Args:
            url: API URL for the recording
            data: Audio content as bytes

        Raises:
            CalldError: If the API returns an error

        """
        headers = self._get_headers()
        headers["Content-type"] = "audio/wav"
        r = self.sync_client.post(url, headers=headers, content=data)
        if r.status_code != 204:
            self.raise_from_response(r)

    async def _put_recording_async(self, url: str, data: bytes) -> None:
        """Update a recording asynchronously.

        Args:
            url: API URL for the recording
            data: Audio content as bytes

        Raises:
            CalldError: If the API returns an error

        """
        headers = self._get_headers()
        headers["Content-type"] = "audio/wav"
        r = await self.async_client.put(url, headers=headers, content=data)
        if r.status_code != 204:
            self.raise_from_response(r)

    def _put_recording(self, url: str, data: bytes) -> None:
        """Update a recording.

        Args:
            url: API URL for the recording
            data: Audio content as bytes

        Raises:
            CalldError: If the API returns an error

        """
        headers = self._get_headers()
        headers["Content-type"] = "audio/wav"
        r = self.sync_client.put(url, headers=headers, content=data)
        if r.status_code != 204:
            self.raise_from_response(r)

    async def _get_recording_async(self, url: str) -> bytes:
        """Get a recording asynchronously.

        Args:
            url: API URL for the recording

        Returns:
            Audio content as bytes

        Raises:
            CalldError: If the API returns an error

        """
        headers = self._get_headers()
        headers["Accept"] = "audio/wav"
        r = await self.async_client.get(url, headers=headers)
        if r.status_code != 200:
            self.raise_from_response(r)
        return r.content

    def _get_recording(self, url: str) -> bytes:
        """Get a recording.

        Args:
            url: API URL for the recording

        Returns:
            Audio content as bytes

        Raises:
            CalldError: If the API returns an error

        """
        headers = self._get_headers()
        headers["Accept"] = "audio/wav"
        r = self.sync_client.get(url, headers=headers)
        if r.status_code != 200:
            self.raise_from_response(r)
        return r.content

    async def _get_async(self, url: str) -> dict[str, Any]:
        """Get a resource asynchronously.

        Args:
            url: API URL for the resource

        Returns:
            Response data as a dictionary

        Raises:
            CalldError: If the API returns an error

        """
        headers = self._get_headers()
        r = await self.async_client.get(url, headers=headers)
        if r.status_code != 200:
            self.raise_from_response(r)
        return r.json()

    def _get(self, url: str) -> dict[str, Any]:
        """Get a resource.

        Args:
            url: API URL for the resource

        Returns:
            Response data as a dictionary

        Raises:
            CalldError: If the API returns an error

        """
        headers = self._get_headers()
        r = self.sync_client.get(url, headers=headers)
        if r.status_code != 200:
            self.raise_from_response(r)
        return r.json()
