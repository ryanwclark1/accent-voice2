# Copyright 2023 Accent Communications

from accent.status import Status

from .http import StatusList


class Plugin:
    def load(self, dependencies):
        api = dependencies['api']
        status_aggregator = dependencies['status_aggregator']

        status_aggregator.add_provider(provide_status)

        api.add_resource(
            StatusList,
            '/status',
            resource_class_args=[status_aggregator],
        )


def provide_status(status):
    status['rest_api']['status'] = Status.ok
