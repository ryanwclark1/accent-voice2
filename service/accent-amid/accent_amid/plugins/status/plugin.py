# Copyright 2023 Accent Communications

from __future__ import annotations

from typing import TYPE_CHECKING

from accent.status import Status

from .http import StatusResource

if TYPE_CHECKING:
    from collections import defaultdict

    from accent_amid.rest_api import PluginDependencies


class Plugin:
    def load(self, dependencies: PluginDependencies) -> None:
        api = dependencies['api']
        status_aggregator = dependencies['status_aggregator']

        status_aggregator.add_provider(provide_status)

        api.add_resource(
            StatusResource,
            '/status',
            resource_class_args=[status_aggregator],
        )


def provide_status(status: defaultdict[str, defaultdict[str, str]]) -> None:
    status['rest_api']['status'] = Status.ok
