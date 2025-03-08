# Copyright 2023 Accent Communications

from accent_lib_rest_client import RESTCommand


class EmailsCommand(RESTCommand):
    resource = 'emails'

    def get(self):
        r = self.session.get(self.resource)
        return r.json()

    def update(self, body):
        self.session.put(self.resource, body)
