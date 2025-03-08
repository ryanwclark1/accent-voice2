# Copyright 2023 Accent Communications

from accent.auth_verifier import required_acl

from accent_setupd.http import AuthResource


class StatusResource(AuthResource):
    def __init__(self, status_aggregator):
        self.status_aggregator = status_aggregator

    @required_acl('setupd.status.read')
    def get(self):
        return self.status_aggregator.status(), 200
