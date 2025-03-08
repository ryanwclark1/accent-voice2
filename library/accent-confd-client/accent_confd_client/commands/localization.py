# Copyright 2023 Accent Communications

from accent_lib_rest_client import HTTPCommand

from accent_confd_client.util import url_join


class LocalizationCommand(HTTPCommand):
    resource = 'localization'

    def get(self, **kwargs):
        tenant_uuid = kwargs.pop('tenant_uuid', None)
        headers = dict(self.session.READ_HEADERS)
        if tenant_uuid:
            headers['Accent-Tenant'] = tenant_uuid
        url = url_join(self.resource)
        response = self.session.get(url, headers=headers, params=kwargs)
        return response.json()

    def update(self, body, **kwargs):
        tenant_uuid = kwargs.pop('tenant_uuid', None)
        headers = dict(self.session.WRITE_HEADERS)
        if tenant_uuid:
            headers['Accent-Tenant'] = tenant_uuid
        url = url_join(self.resource)
        self.session.put(url, json=body, headers=headers, params=kwargs)
