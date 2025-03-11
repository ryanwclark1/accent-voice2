# Copyright 2025 Accent Communications

"""Commands for sending mobile notifications.

This module provides commands for sending mobile notifications
through the Webhookd service.
"""

from __future__ import annotations

import logging
from typing import Any

from accent_webhookd_client.command import WebhookdCommand
from accent_webhookd_client.models import NotificationModel

# Configure logging
logger = logging.getLogger(__name__)


class MobileNotificationCommand(WebhookdCommand):
    """Command for sending mobile notifications.

    This command allows sending notifications to mobile devices
    through the Webhookd service.
    """

    resource = "mobile/notifications"

    def send(self, notification: NotificationModel | dict[str, Any]) -> None:
        """Send a mobile notification.

        Args:
            notification: Notification data to send

        Raises:
            WebhookdError: If the request fails

        """
        logger.info("Sending mobile notification")
        headers = self._get_headers()

        # Convert Pydantic model to dict if needed
        if isinstance(notification, NotificationModel):
            notification = notification.model_dump()

        r = self._sync_request(
            "post", self.base_url, headers=headers, json=notification
        )
        self.raise_from_response(r)
        logger.debug("Mobile notification sent successfully")

    async def send_async(
        self, notification: NotificationModel | dict[str, Any]
    ) -> None:
        """Send a mobile notification asynchronously.

        Args:
            notification: Notification data to send

        Raises:
            WebhookdError: If the request fails

        """
        logger.info("Sending mobile notification (async)")
        headers = self._get_headers()

        # Convert Pydantic model to dict if needed
        if isinstance(notification, NotificationModel):
            notification = notification.model_dump()

        r = await self._async_request(
            "post", self.base_url, headers=headers, json=notification
        )
        self.raise_from_response(r)
        logger.debug("Mobile notification sent successfully")
