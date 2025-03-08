# Copyright 2023 Accent Communications

from . import http


class Plugin:
    def load(self, dependencies):
        api = dependencies['api']

        api.add_resource(
            http.IDPList,
            '/idp',
        )
        api.add_resource(
            http.IDPUser,
            '/idp/<idp_type>/users/<uuid:user_uuid>',
            resource_class_args=(
                dependencies['user_service'],
                dependencies['idp_service'],
            ),
        )
        api.add_resource(
            http.IDPUsers,
            '/idp/<idp_type>/users',
            resource_class_args=(
                dependencies['user_service'],
                dependencies['idp_service'],
            ),
        )
