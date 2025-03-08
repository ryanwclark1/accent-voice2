# Copyright 2023 Accent Communications

from accent_phoned.plugin_helpers.common import create_blueprint_api

from .http import OpenAPIResource


class Plugin:
    def load(self, dependencies):
        app = dependencies['app']
        api = create_blueprint_api(app, 'api_plugin', __name__)
        api.add_resource(OpenAPIResource, '/api/api.yml')
