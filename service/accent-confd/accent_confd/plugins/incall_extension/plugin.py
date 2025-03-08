# Copyright 2023 Accent Communications

from .middleware import IncallExtensionAssociationMiddleWare
from .resource import IncallExtensionItem
from .service import build_service


class Plugin:
    def load(self, dependencies):
        api = dependencies['api']
        middleware_handle = dependencies['middleware_handle']
        service = build_service()
        incall_extension_association_middleware = IncallExtensionAssociationMiddleWare(
            service
        )
        middleware_handle.register(
            'incall_extension_association', incall_extension_association_middleware
        )

        api.add_resource(
            IncallExtensionItem,
            '/incalls/<int:incall_id>/extensions/<int:extension_id>',
            endpoint='incall_extensions',
            resource_class_args=(incall_extension_association_middleware,),
        )
