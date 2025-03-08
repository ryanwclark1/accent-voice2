# Copyright 2023 Accent Communications

from __future__ import annotations

from accent_lib_rest_client import RESTCommand


class EmailsCommand(RESTCommand):
    resource = 'emails'

    def confirm(self, email_uuid: str) -> None:
        headers = self._get_headers()
        url = '/'.join([self.base_url, email_uuid, 'confirm'])
        r = self.session.put(url, headers=headers)
        if r.status_code != 204:
            self.raise_from_response(r)
