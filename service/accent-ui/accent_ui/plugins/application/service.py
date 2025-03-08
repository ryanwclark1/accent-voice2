# Copyright 2023 Accent Communications

from accent_ui.helpers.service import BaseConfdService


class ApplicationService(BaseConfdService):
    resource_confd = 'applications'

    def __init__(self, confd_client):
        self._confd = confd_client

    def create(self, resource):
        application_created = super().create(resource)
        resource['uuid'] = application_created['uuid']
