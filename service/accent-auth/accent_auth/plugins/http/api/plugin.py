# Copyright 2023 Accent Communications

from . import http


class Plugin:
    def load(self, dependencies):
        api = dependencies['api']

        api.add_resource(http.Swagger, '/api/api.yml')
