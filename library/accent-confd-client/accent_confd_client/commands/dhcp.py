# Copyright 2023 Accent Communications

from accent_lib_rest_client import HTTPCommand

from accent_confd_client.util import url_join


class DHCPCommand(HTTPCommand):
    headers = {'Accept': 'application/json'}

    def get(self):
        url = url_join('dhcp')
        r = self.session.get(url, headers=self.headers)

        return r.json()

    def update(self, body):
        url = url_join('dhcp')
        self.session.put(url, json=body, headers=self.headers)
