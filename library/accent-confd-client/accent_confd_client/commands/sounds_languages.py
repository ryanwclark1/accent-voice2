# Copyright 2023 Accent Communications

from accent_lib_rest_client import RESTCommand

from accent_confd_client.util import url_join


class SoundsLanguagesCommand(RESTCommand):
    resource = 'sounds/languages'

    def list(self):
        url = url_join(self.resource)
        response = self.session.get(url)
        return response.json()
