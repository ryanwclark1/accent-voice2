# Copyright 2023 Accent Communications

from __future__ import annotations

from accent_calld.types import PluginDependencies

from .http import ConfigResource
from .service import ConfigService


class Plugin:
    def load(self, dependencies: PluginDependencies) -> None:
        api = dependencies['api']
        config = dependencies['config']
        config_service = ConfigService(config)
        api.add_resource(
            ConfigResource, '/config', resource_class_args=[config_service]
        )
