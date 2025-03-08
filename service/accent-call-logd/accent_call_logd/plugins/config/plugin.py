# Copyright 2023 Accent Communications

from .http import ConfigResource
from .service import ConfigService


class Plugin:
    def load(self, dependencies):
        api = dependencies['api']
        config = dependencies['config']

        config_service = ConfigService(config)
        api.add_resource(
            ConfigResource,
            '/config',
            resource_class_args=[config_service],
        )
