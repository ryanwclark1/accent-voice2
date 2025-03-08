# Copyright 2023 Accent Communications

from accent_phoned.auth import AuthResource


class Status(AuthResource):
    def __init__(self, status_aggregator):
        self.status_aggregator = status_aggregator

    def get(self):
        return self.status_aggregator.status(), 200
