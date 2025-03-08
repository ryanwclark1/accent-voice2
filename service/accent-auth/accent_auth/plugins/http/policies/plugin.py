# Copyright 2023 Accent Communications

from . import http


class Plugin:
    def load(self, dependencies):
        api = dependencies['api']
        args = (dependencies['policy_service'],)

        api.add_resource(
            http.Policies,
            '/policies',
            resource_class_args=args,
        )
        api.add_resource(
            http.PolicyUUID,
            '/policies/<uuid:policy_uuid>',
            resource_class_args=args,
        )
        api.add_resource(
            http.PolicyUUIDAccess,
            '/policies/<uuid:policy_uuid>/acl/<access>',
            resource_class_args=args,
        )
        api.add_resource(
            http.PolicySlug,
            '/policies/<string:policy_slug>',
            resource_class_args=args,
        )
        api.add_resource(
            http.PolicySlugAccess,
            '/policies/<string:policy_slug>/acl/<access>',
            resource_class_args=args,
        )
