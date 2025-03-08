# Copyright 2023 Accent Communications

from .middleware import EndpointSCCPMiddleWare
from .resource import SccpItem, SccpList
from .service import build_service


class Plugin:
    def load(self, dependencies):
        api = dependencies['api']
        middleware_handle = dependencies['middleware_handle']

        service = build_service()

        endpoint_sccp_middleware = EndpointSCCPMiddleWare(service)
        middleware_handle.register('endpoint_sccp', endpoint_sccp_middleware)

        api.add_resource(
            SccpItem,
            '/endpoints/sccp/<int:id>',
            endpoint='endpoint_sccp',
            resource_class_args=(service, endpoint_sccp_middleware),
        )
        api.add_resource(
            SccpList,
            '/endpoints/sccp',
            resource_class_args=(service, endpoint_sccp_middleware),
        )
