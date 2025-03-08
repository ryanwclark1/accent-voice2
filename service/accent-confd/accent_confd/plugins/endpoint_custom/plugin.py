# Copyright 2023 Accent Communications

from .middleware import EndpointCustomMiddleWare
from .resource import CustomItem, CustomList
from .service import build_service


class Plugin:
    def load(self, dependencies):
        api = dependencies['api']
        middleware_handle = dependencies['middleware_handle']

        service = build_service()

        endpoint_custom_middleware = EndpointCustomMiddleWare(service)

        middleware_handle.register('endpoint_custom', endpoint_custom_middleware)

        api.add_resource(
            CustomItem,
            '/endpoints/custom/<int:id>',
            endpoint='endpoint_custom',
            resource_class_args=(service, endpoint_custom_middleware),
        )
        api.add_resource(
            CustomList,
            '/endpoints/custom',
            resource_class_args=(service, endpoint_custom_middleware),
        )
