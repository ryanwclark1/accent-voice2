# Copyright 2023 Accent Communications

from . import http


class Plugin:
    def load(self, dependencies):
        api = dependencies['api']
        args = (dependencies['user_service'],)

        api.add_resource(
            http.Users,
            '/users',
            resource_class_args=args,
        )
        api.add_resource(
            http.User,
            '/users/<uuid:user_uuid>',
            resource_class_args=args,
        )
        api.add_resource(
            http.UserPassword,
            '/users/<uuid:user_uuid>/password',
            resource_class_args=args,
        )
