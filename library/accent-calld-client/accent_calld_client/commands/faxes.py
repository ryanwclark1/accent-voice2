# Copyright 2025 Accent Communications

"""Commands for fax management in the Calld API.

This module provides commands for sending faxes.
"""

from __future__ import annotations

import logging
from typing import Any

from ..command import CalldCommand

logger = logging.getLogger(__name__)


class FaxesCommand(CalldCommand):
    """Command for managing faxes.

    This command provides methods for sending faxes through the Calld API.
    """

    resource = "faxes"

    async def send_async(
        self,
        fax_content: bytes,
        context: str,
        extension: str,
        caller_id: str | None = None,
        ivr_extension: str | None = None,
        wait_time: int | None = None,
    ) -> dict[str, Any]:
        """Send a fax asynchronously.

        Args:
            fax_content: The fax content as PDF binary data
            context: Calling context
            extension: Target extension
            caller_id: Optional caller ID to use
            ivr_extension: Optional IVR extension
            wait_time: Optional wait time in seconds

        Returns:
            Fax status data as a dictionary

        Raises:
            CalldError: If the API returns an error

        """
        url = self._client.url(self.resource)
        headers = self._get_headers()
        headers["Content-Type"] = "application/pdf"
        fax_infos = {"context": context, "extension": extension}
        if caller_id:
            fax_infos["caller_id"] = caller_id
        if ivr_extension:
            fax_infos["ivr_extension"] = ivr_extension
        if wait_time:
            fax_infos["wait_time"] = wait_time
        r = await self.async_client.post(
            url, headers=headers, params=fax_infos, content=fax_content
        )
        if r.status_code != 201:
            self.raise_from_response(r)
        return r.json()

    def send(
        self,
        fax_content: bytes,
        context: str,
        extension: str,
        caller_id: str | None = None,
        ivr_extension: str | None = None,
        wait_time: int | None = None,
    ) -> dict[str, Any]:
        """Send a fax.

        Args:
            fax_content: The fax content as PDF binary data
            context: Calling context
            extension: Target extension
            caller_id: Optional caller ID to use
            ivr_extension: Optional IVR extension
            wait_time: Optional wait time in seconds

        Returns:
            Fax status data as a dictionary

        Raises:
            CalldError: If the API returns an error

        """
        url = self._client.url(self.resource)
        headers = self._get_headers()
        headers["Content-Type"] = "application/pdf"
        fax_infos = {"context": context, "extension": extension}
        if caller_id:
            fax_infos["caller_id"] = caller_id
        if ivr_extension:
            fax_infos["ivr_extension"] = ivr_extension
        if wait_time:
            fax_infos["wait_time"] = wait_time
        r = self.sync_client.post(
            url, headers=headers, params=fax_infos, content=fax_content
        )
        if r.status_code != 201:
            self.raise_from_response(r)
        return r.json()

    async def send_from_user_async(
        self,
        fax_content: bytes,
        extension: str,
        caller_id: str | None = None,
        ivr_extension: str | None = None,
        wait_time: int | None = None,
    ) -> dict[str, Any]:
        """Send a fax as the current user asynchronously.

        Args:
            fax_content: The fax content as PDF binary data
            extension: Target extension
            caller_id: Optional caller ID to use
            ivr_extension: Optional IVR extension
            wait_time: Optional wait time in seconds

        Returns:
            Fax status data as a dictionary

        Raises:
            CalldError: If the API returns an error

        """
        url = self._client.url("users", "me", self.resource)
        headers = self._get_headers()
        headers["Content-Type"] = "application/pdf"
        fax_infos = {"extension": extension}
        if caller_id:
            fax_infos["caller_id"] = caller_id
        if ivr_extension:
            fax_infos["ivr_extension"] = ivr_extension
        if wait_time:
            fax_infos["wait_time"] = wait_time
        r = await self.async_client.post(
            url, headers=headers, params=fax_infos, content=fax_content
        )
        if r.status_code != 201:
            self.raise_from_response(r)
        return r.json()

    def send_from_user(
        self,
        fax_content: bytes,
        extension: str,
        caller_id: str | None = None,
        ivr_extension: str | None = None,
        wait_time: int | None = None,
    ) -> dict[str, Any]:
        """Send a fax as the current user.

        Args:
            fax_content: The fax content as PDF binary data
            extension: Target extension
            caller_id: Optional caller ID to use
            ivr_extension: Optional IVR extension
            wait_time: Optional wait time in seconds

        Returns:
            Fax status data as a dictionary

        Raises:
            CalldError: If the API returns an error

        """
        url = self._client.url("users", "me", self.resource)
        headers = self._get_headers()
        headers["Content-Type"] = "application/pdf"
        fax_infos = {"extension": extension}
        if caller_id:
            fax_infos["caller_id"] = caller_id
        if ivr_extension:
            fax_infos["ivr_extension"] = ivr_extension
        if wait_time:
            fax_infos["wait_time"] = wait_time
        r = self.sync_client.post(
            url, headers=headers, params=fax_infos, content=fax_content
        )
        if r.status_code != 201:
            self.raise_from_response(r)
        return r.json()
