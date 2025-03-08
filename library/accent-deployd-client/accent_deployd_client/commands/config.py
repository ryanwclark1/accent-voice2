# Copyright 2023 Accent Communications

from accent_deployd_client.command import DeploydCommand


class ConfigCommand(DeploydCommand):
    resource = 'config'

    def get(self):
        headers = self._get_headers()
        r = self.session.get(self.base_url, headers=headers)
        self.raise_from_response(r)
        return r.json()
