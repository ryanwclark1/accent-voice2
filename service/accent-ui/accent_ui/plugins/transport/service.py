# Copyright 2023 Accent Communications

from accent_ui.helpers.service import BaseConfdService


class TransportService(BaseConfdService):
    resource_confd = 'sip_transports'

    def __init__(self, confd_client):
        self._confd = confd_client
