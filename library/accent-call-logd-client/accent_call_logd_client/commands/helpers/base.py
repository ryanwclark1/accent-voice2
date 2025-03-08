# Copyright 2023 Accent Communications

from accent_call_logd_client.command import CallLogdCommand


class BaseCommand(CallLogdCommand):
    _headers = {'Accept': 'application/json'}

    def _get_headers(self, **kwargs):
        headers = dict(self._headers)
        # The requests session will use self.tenant_uuid by default
        tenant_uuid = kwargs.pop('tenant_uuid', None)
        if tenant_uuid:
            headers['Accent-Tenant'] = tenant_uuid
        return headers
