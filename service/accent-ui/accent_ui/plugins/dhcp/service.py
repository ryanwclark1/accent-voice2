# Copyright 2023 Accent Communications

from accent_ui.helpers.service import BaseConfdService


class DhcpService(BaseConfdService):
    resource_confd = 'dhcp'

    def __init__(self, confd):
        self._confd = confd

    def get(self):
        return self._confd.dhcp.get()

    def update(self, resource):
        return self._confd.dhcp.update(resource)
