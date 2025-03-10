# Copyright 2025 Accent Communications

from __future__ import annotations

import logging

import httpx
from accent_lib_rest_client import RESTCommand

logger = logging.getLogger(__name__)


class EmailsCommand(RESTCommand):
    """Command for email-related operations.

    Provides methods for managing email addresses and confirmation.
    """

    resource = "emails"

    async def confirm_async(self, email_uuid: str) -> None:
        """Confirm an email address asynchronously.

        Args:
            email_uuid: Email identifier

        Raises:
            AccentAPIError: If the request fails

        """
        headers = self._get_headers()
        url = "/".join([self.base_url, email_uuid, "confirm"])

        r = await self.async_client.put(url, headers=headers)

        try:
            r.raise_for_status()
        except httpx.HTTPStatusError as e:
            if r.status_code != 204:
                logger.error(
                    "Failed to confirm email: %s, status code: %s",
                    str(e),
                    r.status_code,
                )
                self.raise_from_response(r)

    def confirm(self, email_uuid: str) -> None:
        """Confirm an email address.

        Args:
            email_uuid: Email identifier

        Raises:
            AccentAPIError: If the request fails

        """
        headers = self._get_headers()
        url = "/".join([self.base_url, email_uuid, "confirm"])

        r = self.sync_client.put(url, headers=headers)

        if r.status_code != 204:
            logger.error("Failed to confirm email: %s", email_uuid)
            self.raise_from_response(r)
