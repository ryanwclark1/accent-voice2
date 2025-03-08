# Copyright 2023 Accent Communications

from . import http


class Plugin:
    def load(self, dependencies):
        api = dependencies['api']
        args = (
            dependencies['email_service'],
            dependencies['tenant_service'],
            dependencies['user_service'],
        )

        api.add_resource(
            http.Register,
            '/users/register',
            resource_class_args=args,
        )
