# Copyright 2023 Accent Communications

from ..command import CalldCommand


class LinesCommand(CalldCommand):
    resource = 'lines'

    def list_lines(self, tenant_uuid=None):
        headers = self._get_headers(tenant_uuid=tenant_uuid)
        url = self._client.url(self.resource)

        r = self.session.get(url, headers=headers)
        if r.status_code != 200:
            self.raise_from_response(r)

        return r.json()
