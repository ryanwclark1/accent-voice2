# Copyright 2023 Accent Communications

from accent_amid_client.command import AmidCommand


class StatusCommand(AmidCommand):
    resource = 'status'

    def __call__(self):
        headers = self._get_headers()
        url = self.base_url
        r = self.session.get(url, headers=headers)

        if r.status_code != 200:
            self.raise_from_response(r)

        return r.json()
