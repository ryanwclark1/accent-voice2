# Copyright 2023 Accent Communications

from accent_setupd_client.command import SetupdCommand


class StatusCommand(SetupdCommand):
    resource = 'status'

    def get(self, tenant_uuid=None):
        headers = self._get_headers(tenant_uuid=tenant_uuid)
        r = self.session.get(self.base_url, headers=headers)
        self.raise_from_response(r)
        return r.json()
