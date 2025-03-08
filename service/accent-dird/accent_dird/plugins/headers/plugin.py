# Copyright 2023 Accent Communications

import logging

from accent_dird import BaseViewPlugin

from .http import Headers

logger = logging.getLogger(__name__)


class HeadersViewPlugin(BaseViewPlugin):
    def load(self, dependencies):
        api = dependencies['api']
        display_service = dependencies['services'].get('display')
        profile_service = dependencies['services'].get('profile')

        api.add_resource(
            Headers,
            '/directories/lookup/<profile>/headers',
            resource_class_args=(display_service, profile_service),
        )
