# Copyright 2023 Accent Communications

from .http import SwaggerResource


class Plugin:
    def load(self, dependencies):
        api = dependencies['api']
        api.add_resource(SwaggerResource, '/api/api.yml')
