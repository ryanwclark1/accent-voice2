# Copyright 2023 Accent Communications

from __future__ import annotations

from typing import TYPE_CHECKING

from .http import ConfigResource
from .service import ConfigService

if TYPE_CHECKING:
    from accent_amid.rest_api import PluginDependencies


class Plugin:
    def load(self, dependencies: PluginDependencies) -> None:
        api = dependencies['api']
        config = dependencies['config']
        config_service = ConfigService(config)
        api.add_resource(
            ConfigResource, '/config', resource_class_args=[config_service]
        )
