# Copyright 2023 Accent Communications

from accent_ui.helpers.service import BaseConfdService


class AccessFeaturesService(BaseConfdService):
    resource_confd = 'access_features'

    def __init__(self, confd_client):
        self._confd = confd_client
