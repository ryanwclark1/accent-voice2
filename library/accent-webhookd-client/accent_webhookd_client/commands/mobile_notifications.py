# Copyright 2023 Accent Communications

from __future__ import annotations

from typing import TYPE_CHECKING

from accent_webhookd_client.command import WebhookdCommand

if TYPE_CHECKING:
    from webhookd.plugins.mobile.schema import NotificationDict


class MobileNotificationCommand(WebhookdCommand):
    resource = 'mobile/notifications'

    def send(self, notification: NotificationDict) -> None:
        headers = self._get_headers()
        r = self.session.post(
            self.base_url,
            json=notification,
            headers=headers,
        )
        self.raise_from_response(r)
