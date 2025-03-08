# Copyright 2023 Accent Communications

from accent.status import Status

from accent_auth.http import ErrorCatchingResource


class StatusList(ErrorCatchingResource):
    def __init__(self, status_aggregator):
        self.status_aggregator = status_aggregator

    def head(self):
        for component in self.status_aggregator.status().values():
            if component.get('status') == Status.fail:
                return '', 503
        return '', 200
