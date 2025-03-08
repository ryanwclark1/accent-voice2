# Copyright 2023 Accent Communications

from accent_phoned.plugin_helpers.common import create_blueprint_api

from .http import Status


class Plugin:
    def load(self, dependencies):
        app = dependencies['app']
        status_aggregator = dependencies['status_aggregator']
        api = create_blueprint_api(app, 'status_plugin', __name__)
        api.add_resource(Status, '/status', resource_class_args=[status_aggregator])
