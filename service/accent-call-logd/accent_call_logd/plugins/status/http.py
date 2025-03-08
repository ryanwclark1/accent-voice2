# Copyright 2023 Accent Communications

from accent_call_logd.auth import required_acl
from accent_call_logd.http import AuthResource


class StatusResource(AuthResource):
    def __init__(self, status_aggregator):
        self.status_aggregator = status_aggregator

    @required_acl('call-logd.status.read')
    def get(self):
        return self.status_aggregator.status(), 200
