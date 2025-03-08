# Copyright 2023 Accent Communications

from . import http


class Plugin:
    def load(self, dependencies):
        api = dependencies['api']
        args = (dependencies['external_auth_service'],)

        api.add_resource(
            http.External,
            '/users/<uuid:user_uuid>/external',
            resource_class_args=args,
        )
        api.add_resource(
            http.ExternalConfig,
            '/external/<string:auth_type>/config',
            resource_class_args=args,
        )

        api.add_resource(
            http.ExternalUsers,
            '/external/<string:auth_type>/users',
            resource_class_args=args,
        )
