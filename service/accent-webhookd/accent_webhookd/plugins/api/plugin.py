# Copyright 2023 Accent Communications

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ...types import PluginDependencyDict

from .http import SwaggerResource


class Plugin:
    def load(self, dependencies: PluginDependencyDict) -> None:
        api = dependencies['api']
        api.add_resource(SwaggerResource, '/api/api.yml')
