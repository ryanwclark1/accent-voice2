# Copyright 2023 Accent Communications

from . import http


class Plugin:
    def load(self, dependencies):
        api = dependencies['api']
        args = (dependencies['user_service'], dependencies['policy_service'])

        api.add_resource(
            http.UserPolicyUUID,
            '/users/<uuid:user_uuid>/policies/<uuid:policy_uuid>',
            resource_class_args=args,
        )
        api.add_resource(
            http.UserPolicySlug,
            '/users/<uuid:user_uuid>/policies/<string:policy_slug>',
            resource_class_args=args,
        )
        api.add_resource(
            http.UserPolicies,
            '/users/<uuid:user_uuid>/policies',
            resource_class_args=args,
        )
