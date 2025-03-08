# Copyright 2023 Accent Communications

from accent_lib_rest_client import RESTCommand


class PJSIPDocCommand(RESTCommand):
    resource = 'asterisk/pjsip/doc'

    def get(self):
        response = self.session.get(self.resource)
        return response.json()
