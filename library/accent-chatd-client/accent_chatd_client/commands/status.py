# Copyright 2023 Accent Communications

from .helpers.base import BaseCommand


class StatusCommand(BaseCommand):
    resource = 'status'

    def get(self):
        headers = self._get_headers()
        r = self.session.get(self.base_url, headers=headers)
        self.raise_from_response(r)
        return r.json()
