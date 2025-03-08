# Copyright 2023 Accent Communications

from accent_auth import http


class Backends(http.ErrorCatchingResource):
    def __init__(self, config):
        self._config = config

    def get(self):
        return {'data': self._config['loaded_plugins']}
