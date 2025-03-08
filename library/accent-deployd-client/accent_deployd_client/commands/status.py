# Copyright 2023 Accent Communications

from accent_deployd_client.command import DeploydCommand


class StatusCommand(DeploydCommand):
    resource = 'status'

    def check(self):
        headers = self._get_headers()
        r = self.session.head(self.base_url, headers=headers)
        if r.status_code != 200:
            self.raise_from_response(r)
