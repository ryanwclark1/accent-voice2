# Copyright 2023 Accent Communications

from accent_dird.auth import required_acl
from accent_dird.http import AuthResource


class StatusResource(AuthResource):
    def __init__(self, status_aggregator):
        self.status_aggregator = status_aggregator

    @required_acl('dird.status.read')
    def get(self):
        return self.status_aggregator.status(), 200
