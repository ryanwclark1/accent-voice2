# Copyright 2023 Accent Communications


from .http import StatusResource


class Plugin:
    def load(self, dependencies):
        api = dependencies['api']
        status_aggregator = dependencies['status_aggregator']

        api.add_resource(
            StatusResource, '/status', resource_class_args=[status_aggregator]
        )
