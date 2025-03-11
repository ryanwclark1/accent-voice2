# Copyright 2025 Accent Communications

from __future__ import annotations

import logging
from typing import cast

import httpx
from accent_lib_rest_client import RESTCommand

from accent_auth_client.type_definitions import JSON

logger = logging.getLogger(__name__)


class AdminCommand(RESTCommand):
    """Command for administrative operations.

    Provides methods for system administration tasks.
    """

    resource = "admin"

    async def update_user_emails_async(
        self, user_uuid: str, emails: list[JSON]
    ) -> JSON:
        """Update user emails asynchronously.

        Args:
            user_uuid: User identifier
            emails: List of email data

        Returns:
            JSON: Updated user email information

        Raises:
            AccentAPIError: If the request fails

        """
        headers = self._get_headers()
        url = f"{self.base_url}/users/{user_uuid}/emails"
        body = {"emails": emails}

        r = await self.async_client.put(url, headers=headers, json=body)

        try:
            r.raise_for_status()
        except httpx.HTTPStatusError:
            logger.error("Failed to update user emails for user: %s", user_uuid)
            self.raise_from_response(r)

        return cast(JSON, r.json())

    def update_user_emails(self, user_uuid: str, emails: list[JSON]) -> JSON:
        """Update user emails.

        Args:
            user_uuid: User identifier
            emails: List of email data

        Returns:
            JSON: Updated user email information

        Raises:
            AccentAPIError: If the request fails

        """
        headers = self._get_headers()
        url = f"{self.base_url}/users/{user_uuid}/emails"
        body = {"emails": emails}

        r = self.sync_client.put(url, headers=headers, json=body)

        if r.status_code != 200:
            logger.error("Failed to update user emails for user: %s", user_uuid)
            self.raise_from_response(r)

        return cast(JSON, r.json())
