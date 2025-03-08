# Copyright 2023 Accent Communications

from accent_lib_rest_client import HTTPCommand

from accent_confd_client.util import url_join


class LiveReloadCommand(HTTPCommand):
    def get(self):
        url = url_join('configuration', 'live_reload')
        r = self.session.get(url)

        return r.json()

    def update(self, body):
        url = url_join('configuration', 'live_reload')
        self.session.put(url, body)


class ConfigurationCommand:
    def __init__(self, client):
        self.live_reload = LiveReloadCommand(client)
