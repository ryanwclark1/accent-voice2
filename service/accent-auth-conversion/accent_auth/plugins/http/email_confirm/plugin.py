# Copyright 2023 Accent Communications

from . import http


class Plugin:
    def load(self, dependencies):
        api = dependencies['api']
        args = (
            dependencies['email_service'],
            dependencies['template_formatter'],
            dependencies['config'],
        )

        api.add_resource(
            http.EmailConfirm,
            '/emails/<uuid:email_uuid>/confirm',
            resource_class_args=args,
        )
