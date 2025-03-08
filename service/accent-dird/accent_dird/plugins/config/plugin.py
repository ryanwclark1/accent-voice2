# Copyright 2023 Accent Communications

import logging

from accent_dird import BaseViewPlugin

from .http import Config

logger = logging.getLogger(__name__)


class ConfigViewPlugin(BaseViewPlugin):
    url = '/config'

    def load(self, dependencies):
        api = dependencies['api']
        config_service = dependencies['services'].get('config')
        if not config_service:
            logger.info(
                'failed to load the %s config service is disabled',
                self.__class__.__name__,
            )
            return

        Config.configure(config_service)

        api.add_resource(Config, self.url)
