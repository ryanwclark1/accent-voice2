# Copyright 2023 Accent Communications

import logging

from .http import GoogleAuth

logger = logging.getLogger(__name__)


class GooglePlugin:
    def load(self, dependencies):
        api = dependencies['api']
        config = dependencies['config']
        args = (
            dependencies['external_auth_service'],
            dependencies['user_service'],
            config,
        )

        api.add_resource(
            GoogleAuth,
            '/users/<uuid:user_uuid>/external/google',
            resource_class_args=args,
        )
