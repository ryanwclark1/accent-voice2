# Copyright 2023 Accent Communications

from .http import ConfigResource


class Plugin:
    def load(self, dependencies):
        api = dependencies['api']
        config = dependencies['config']
        api.add_resource(ConfigResource, '/config', resource_class_args=[config])
