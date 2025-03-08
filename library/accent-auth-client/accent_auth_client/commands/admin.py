# Copyright 2023 Accent Communications

from __future__ import annotations

from accent_lib_rest_client import RESTCommand

from ..types import JSON


class AdminCommand(RESTCommand):
    resource = 'admin'

    def update_user_emails(self, user_uuid: str, emails: list[JSON]) -> JSON:
        headers = self._get_headers()
        url = f'{self.base_url}/users/{user_uuid}/emails'
        body = {'emails': emails}
        r = self.session.put(url, headers=headers, json=body)
        if r.status_code != 200:
            self.raise_from_response(r)

        return r.json()
