# Copyright 2023 Accent Communications

from .helpers.base import BaseCommand


class StatusCommand(BaseCommand):
    def get(self):
        headers = self._get_headers()
        url = self._client.url('status')
        r = self.session.get(url, headers=headers)
        self.raise_from_response(r)
        return r.json()
