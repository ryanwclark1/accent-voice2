# Copyright 2023 Accent Communications

from accent.status import Status

from .resource import StatusResource


class Plugin:
    def load(self, dependencies):
        api = dependencies['api']
        status_aggregator = dependencies['status_aggregator']

        status_aggregator.add_provider(provide_status)

        api.add_resource(StatusResource, '/status', resource_class_args=[status_aggregator])


def provide_status(status):
    status['rest_api']['status'] = Status.ok
