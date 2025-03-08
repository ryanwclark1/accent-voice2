# Copyright 2023 Accent Communications

from accent_lib_rest_client import RESTCommand


class PJSIPGlobalCommand(RESTCommand):
    resource = 'asterisk/pjsip/global'

    def get(self):
        response = self.session.get(self.resource)
        return response.json()

    def update(self, body):
        self.session.put(self.resource, body)
