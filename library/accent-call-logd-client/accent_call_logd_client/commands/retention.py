# Copyright 2023 Accent Communications

from .helpers.base import BaseCommand


class RetentionCommand(BaseCommand):
    def get(self, tenant_uuid=None):
        headers = self._get_headers(tenant_uuid=tenant_uuid)
        url = self._client.url('retention')
        r = self.session.get(url, headers=headers)
        self.raise_from_response(r)
        return r.json()

    def update(self, tenant_uuid=None, **body):
        headers = self._get_headers(tenant_uuid=tenant_uuid)
        url = self._client.url('retention')
        r = self.session.put(url, json=body, headers=headers)
        self.raise_from_response(r)
