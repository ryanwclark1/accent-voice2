# Copyright 2023 Accent Communications

from accent_webhookd_client.command import WebhookdCommand


class SentinelBusCommand(WebhookdCommand):
    resource = 'sentinel'
    _ro_headers = {'Accept': 'application/json'}

    def get(self):
        r = self.session.get(self.base_url + '/bus', headers=self._ro_headers)
        self.raise_from_response(r)
        return r.json()
