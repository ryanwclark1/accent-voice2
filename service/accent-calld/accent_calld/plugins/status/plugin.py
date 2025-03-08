# Copyright 2023 Accent Communications

from __future__ import annotations

from accent_calld.types import PluginDependencies

from .http import StatusResource


class Plugin:
    def load(self, dependencies: PluginDependencies) -> None:
        api = dependencies['api']
        status_aggregator = dependencies['status_aggregator']

        api.add_resource(
            StatusResource, '/status', resource_class_args=[status_aggregator]
        )
