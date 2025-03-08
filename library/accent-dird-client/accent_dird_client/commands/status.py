# Copyright 2023 Accent Communications

from accent_dird_client.commands.helpers.base_command import DirdRESTCommand


class StatusCommand(DirdRESTCommand):
    resource = 'status'

    def get(self, tenant_uuid=None):
        headers = self.build_headers(tenant_uuid=tenant_uuid)
        r = self.session.get(self.base_url, headers=headers)
        self.raise_from_response(r)
        return r.json()
