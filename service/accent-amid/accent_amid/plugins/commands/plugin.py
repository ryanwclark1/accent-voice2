# Copyright 2023 Accent Communications

from __future__ import annotations

from typing import TYPE_CHECKING

from .http import CommandResource

if TYPE_CHECKING:
    from accent_amid.rest_api import PluginDependencies


class Plugin:
    def load(self, dependencies: PluginDependencies) -> None:
        api = dependencies['api']
        ajam_client = dependencies['ajam_client']

        api.add_resource(
            CommandResource,
            '/action/Command',
            resource_class_args=[ajam_client],
        )
