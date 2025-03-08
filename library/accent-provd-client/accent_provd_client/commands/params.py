# Copyright 2023 Accent Communications

from accent_provd_client.command import ProvdCommand


class ParamsCommand(ProvdCommand):
    resource = 'configure'
    _headers = {'Content-Type': 'application/vnd.accent.provd+json'}

    def list(self):
        url = f'{self.base_url}'
        r = self.session.get(url)
        self.raise_from_response(r)
        return r.json()

    def get(self, param, tenant_uuid=None, **kwargs):
        url = f'{self.base_url}/{param}'
        headers = self._get_headers(tenant_uuid=tenant_uuid)
        r = self.session.get(url, headers=headers)
        self.raise_from_response(r)
        return r.json()['param']

    def update(self, param, value, tenant_uuid=None, **kwargs):
        url = f'{self.base_url}/{param}'
        data = {'param': {'value': value}}
        headers = self._get_headers(tenant_uuid=tenant_uuid)
        r = self.session.put(url, json=data, headers=headers)
        self.raise_from_response(r)

    def delete(self, param):
        self.update(param, None)
