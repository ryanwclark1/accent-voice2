# Copyright 2023 Accent Communications

from . import http


class Plugin:
    def load(self, dependencies):
        api = dependencies['api']
        args = (dependencies['group_service'],)

        api.add_resource(
            http.Group,
            '/groups/<uuid:group_uuid>',
            resource_class_args=args,
        )
        api.add_resource(
            http.Groups,
            '/groups',
            resource_class_args=args,
        )
