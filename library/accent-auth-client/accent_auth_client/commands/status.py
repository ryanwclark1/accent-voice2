# Copyright 2023 Accent Communications

from __future__ import annotations

from accent_lib_rest_client import RESTCommand


class StatusCommand(RESTCommand):
    resource = 'status'

    def check(self) -> None:
        headers = self._get_headers()
        r = self.session.head(self.base_url, headers=headers)
        if r.status_code != 200:
            self.raise_from_response(r)
