# Copyright 2023 Accent Communications

from . import http


class Plugin:
    def load(self, dependencies):
        api = dependencies['api']
        args = (dependencies['group_service'], dependencies['user_service'])

        api.add_resource(
            http.GroupUser,
            '/groups/<uuid:group_uuid>/users/<uuid:user_uuid>',
            resource_class_args=args,
        )
        api.add_resource(
            http.GroupUsers,
            '/groups/<uuid:group_uuid>/users',
            resource_class_args=args,
        )
        api.add_resource(
            http.UserGroups,
            '/users/<uuid:user_uuid>/groups',
            resource_class_args=(dependencies['user_service'],),
        )
