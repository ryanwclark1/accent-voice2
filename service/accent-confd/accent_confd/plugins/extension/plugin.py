# Copyright 2023 Accent Communications

from accent_provd_client import Client as ProvdClient

from .middleware import ExtensionMiddleWare
from .resource import ExtensionItem, ExtensionList
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
        extension_middleware = ExtensionMiddleWare(service)
        middleware_handle.register('extension', extension_middleware)

        api.add_resource(
            ExtensionItem,
            '/extensions/<int:id>',
            endpoint='extensions',
            resource_class_args=(service, extension_middleware),
        )
        api.add_resource(
            ExtensionList,
            '/extensions',
            resource_class_args=(service, extension_middleware),
        )
