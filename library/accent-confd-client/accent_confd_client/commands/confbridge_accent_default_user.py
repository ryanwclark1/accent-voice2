# Copyright 2023 Accent Communications

from accent_lib_rest_client import RESTCommand


class ConfBridgeAccentDefaultUserCommand(RESTCommand):
    resource = 'asterisk/confbridge/accent_default_user'

    def get(self):
        response = self.session.get(self.resource)
        return response.json()

    def update(self, body):
        self.session.put(self.resource, body)
