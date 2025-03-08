# Copyright 2023 Accent Communications

from accent_dird_client.commands.helpers.base_command import DirdRESTCommand


class BackendsCommand(DirdRESTCommand):
    resource = 'backends'

    def create_source(self, backend, body, tenant_uuid=None, token=None):
        url = self._build_base_url(backend)
        headers = self.build_headers(tenant_uuid, token)
        r = self.session.post(url, headers=headers, json=body)
        self.raise_from_response(r)

        return r.json()

    def delete_source(self, backend, source_uuid, tenant_uuid=None, token=None):
        url = self._build_url(backend, source_uuid)
        headers = self.build_headers(tenant_uuid, token)
        r = self.session.delete(url, headers=headers)
        self.raise_from_response(r)

    def edit_source(self, backend, source_uuid, body, tenant_uuid=None, token=None):
        url = self._build_url(backend, source_uuid)
        headers = self.build_headers(tenant_uuid, token)
        r = self.session.put(url, headers=headers, json=body)
        self.raise_from_response(r)

    def get_source(self, backend, source_uuid, tenant_uuid=None, token=None):
        url = self._build_url(backend, source_uuid)
        headers = self.build_headers(tenant_uuid, token)
        r = self.session.get(url, headers=headers)
        self.raise_from_response(r)

        return r.json()

    def list(self, token=None, tenant_uuid=None, **kwargs):
        headers = self.build_headers(tenant_uuid, token)
        r = self.session.get(self.base_url, params=kwargs, headers=headers)
        self.raise_from_response(r)
        return r.json()

    def list_sources(self, backend, tenant_uuid=None, token=None, **kwargs):
        url = self._build_base_url(backend)
        headers = self.build_headers(tenant_uuid, token)
        r = self.session.get(url, headers=headers, params=kwargs)
        self.raise_from_response(r)

        return r.json()

    def list_contacts_from_source(
        self, backend, source_uuid, tenant_uuid=None, token=None, uuids=None, **kwargs
    ):
        if backend == 'accent' and uuids is not None:
            kwargs['uuid'] = ','.join(uuid for uuid in uuids)
        url = self._build_url(backend, source_uuid, 'contacts')
        headers = self.build_headers(tenant_uuid, token)
        r = self.session.get(url, headers=headers, params=kwargs)
        self.raise_from_response(r)

        return r.json()

    def _build_base_url(self, backend):
        return '/'.join([self.base_url, backend, 'sources'])

    def _build_url(self, backend, source_uuid, *args):
        return '/'.join([self.base_url, backend, 'sources', source_uuid] + list(args))
