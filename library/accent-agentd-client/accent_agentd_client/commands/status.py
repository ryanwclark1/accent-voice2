# Copyright 2023 Accent Communications


from accent_lib_rest_client.command import RESTCommand

from accent_agentd_client.helpers import ResponseProcessor


class StatusCommand(RESTCommand):
    resource = 'status'

    def __call__(self):
        _resp_processor = ResponseProcessor()
        headers = self._get_headers()
        url = self.base_url
        r = self.session.get(url, headers=headers)

        if r.status_code != 200:
            _resp_processor.generic(r)

        return r.json()
