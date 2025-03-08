# Copyright 2023 Accent Communications

from .middleware import IncallMiddleWare
from .resource import IncallItem, IncallList
from .service import build_service


class Plugin:
    def load(self, dependencies):
        api = dependencies['api']
        middleware_handle = dependencies['middleware_handle']
        service = build_service()
        incall_middleware = IncallMiddleWare(service)
        middleware_handle.register('incall', incall_middleware)

        api.add_resource(
            IncallList,
            '/incalls',
            resource_class_args=(
                service,
                incall_middleware,
            ),
        )

        api.add_resource(
            IncallItem,
            '/incalls/<int:id>',
            endpoint='incalls',
            resource_class_args=(
                service,
                incall_middleware,
            ),
        )
