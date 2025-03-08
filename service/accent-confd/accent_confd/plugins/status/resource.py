# Copyright 2023 Accent Communications

from accent.auth_verifier import required_acl

from accent_confd.helpers.restful import ConfdResource


class StatusChecker(ConfdResource):
    def __init__(self, status_aggregator):
        self.status_aggregator = status_aggregator

    @required_acl('confd.status.read')
    def get(self):
        return self.status_aggregator.status(), 200
