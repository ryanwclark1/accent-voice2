# Copyright 2023 Accent Communications

from accent_provd_client import Client as ProvdClient

from .middleware import LineMiddleWare
from .resource import LineItem, LineList
from .service import build_service


class Plugin:
    def load(self, dependencies):
        api = dependencies['api']
        config = dependencies['config']
        token_changed_subscribe = dependencies['token_changed_subscribe']
        middleware_handle = dependencies['middleware_handle']

        provd_client = ProvdClient(**config['provd'])
        token_changed_subscribe(provd_client.set_token)

        service = build_service(provd_client)

        line_middleware = LineMiddleWare(service, middleware_handle)
        middleware_handle.register('line', line_middleware)

        api.add_resource(
            LineItem,
            '/lines/<int:id>',
            endpoint='lines',
            resource_class_args=(service, line_middleware),
        )
        api.add_resource(
            LineList,
            '/lines',
            resource_class_args=(service, line_middleware),
        )
