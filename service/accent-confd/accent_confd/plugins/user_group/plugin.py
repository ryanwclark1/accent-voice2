# Copyright 2023 Accent Communications

from .middleware import UserGroupAssociationMiddleWare
from .resource import UserGroupItem
from .service import build_service


class Plugin:
    def load(self, dependencies):
        api = dependencies['api']
        middleware_handle = dependencies['middleware_handle']
        service = build_service()
        user_group_association_middleware = UserGroupAssociationMiddleWare(service)
        middleware_handle.register(
            'user_group_association', user_group_association_middleware
        )

        api.add_resource(
            UserGroupItem,
            '/users/<uuid:user_id>/groups',
            '/users/<int:user_id>/groups',
            endpoint='user_groups',
            resource_class_args=(
                service,
                user_group_association_middleware,
            ),
        )
