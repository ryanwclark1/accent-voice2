# Copyright 2023 Accent Communications

from .http import MobileAuth, MobileAuthSenderID


class Plugin:
    def load(self, dependencies):
        api = dependencies['api']
        api.add_resource(
            MobileAuth,
            '/users/<uuid:user_uuid>/external/mobile',
            resource_class_args=[
                dependencies['external_auth_service'],
                dependencies['config'],
            ],
        )
        api.add_resource(
            MobileAuthSenderID,
            '/users/<uuid:user_uuid>/external/mobile/sender_id',
            resource_class_args=[
                dependencies['external_auth_service'],
                dependencies['user_service'],
            ],
        )
