# Copyright 2023 Accent Communications

from accent_dao.resources.tenant import dao as tenant_dao

from .middleware import ContextMiddleWare
from .resource import ContextItem, ContextList
from .service import build_service


class Plugin:
    def load(self, dependencies):
        api = dependencies['api']
        middleware_handle = dependencies['middleware_handle']

        service = build_service()
        context_middleware = ContextMiddleWare(service)
        middleware_handle.register('context', context_middleware)

        api.add_resource(
            ContextList, '/contexts', resource_class_args=(tenant_dao, service)
        )

        api.add_resource(
            ContextItem,
            '/contexts/<int:id>',
            endpoint='contexts',
            resource_class_args=(service, context_middleware),
        )
