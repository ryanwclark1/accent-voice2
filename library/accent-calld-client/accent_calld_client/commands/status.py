# Copyright 2023 Accent Communications

from accent_calld_client.command import CalldCommand


class StatusCommand(CalldCommand):
    resource = 'status'

    def get(self):
        headers = self._get_headers()
        url = self.base_url
        r = self.session.get(url, headers=headers)
        self.raise_from_response(r)
        return r.json()
