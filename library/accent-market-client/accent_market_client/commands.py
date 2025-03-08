# Copyright 2023 Accent Communications

from accent_lib_rest_client import RESTCommand

DEFAULT_HEADERS = {'Accept': 'application/json', 'Content-Type': 'application/json'}


class PluginCommand(RESTCommand):
    resource = 'plugins'

    def list(self):
        r = self.session.get(self.base_url, headers=DEFAULT_HEADERS)
        if r.status_code != 200:
            self.raise_from_response(r)

        return r.json()
