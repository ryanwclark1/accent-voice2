# Copyright 2023 Accent Communications

from accent_provd_client.command import ProvdCommand


class StatusCommand(ProvdCommand):
    resource = 'status'
    _headers = {'Content-Type': 'application/vnd.accent.provd+json'}

    def get(self):
        r = self.session.get(self.base_url, headers=self._headers)
        self.raise_from_response(r)
        return r.json()
