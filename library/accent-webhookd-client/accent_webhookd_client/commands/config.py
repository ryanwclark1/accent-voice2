# Copyright 2023 Accent Communications

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from accent_webhookd_client.command import WebhookdCommand

if TYPE_CHECKING:
    from webhookd.types import WebhookdConfigDict


class ConfigCommand(WebhookdCommand):
    resource = 'config'

    def get(self) -> WebhookdConfigDict:
        headers = self._get_headers()
        r = self.session.get(self.base_url, headers=headers)
        self.raise_from_response(r)
        response: WebhookdConfigDict = r.json()
        return response

    def patch(
        self, config_patch: WebhookdConfigDict | dict[str, Any]
    ) -> WebhookdConfigDict:
        headers = self._get_headers()
        r = self.session.patch(self.base_url, headers=headers, json=config_patch)
        self.raise_from_response(r)
        response: WebhookdConfigDict = r.json()
        return response
