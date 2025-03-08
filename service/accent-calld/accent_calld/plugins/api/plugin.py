# Copyright 2023 Accent Communications

from __future__ import annotations

from accent_calld.types import PluginDependencies

from .http import SwaggerResource


class Plugin:
    def load(self, dependencies: PluginDependencies) -> None:
        api = dependencies['api']
        api.add_resource(SwaggerResource, '/api/api.yml')
