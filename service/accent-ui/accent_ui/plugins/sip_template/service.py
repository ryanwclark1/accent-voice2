# Copyright 2023 Accent Communications

from accent_ui.helpers.service import BaseConfdService


class EndpointSIPTemplateService(BaseConfdService):
    resource_confd = 'endpoints_sip_templates'

    def __init__(self, confd_client):
        self._confd = confd_client

    def get_transport(self, uuid):
        return self._confd.sip_transports.get(uuid)

    def get_sip_template(self, uuid):
        return self._confd.endpoints_sip_templates.get(uuid)
