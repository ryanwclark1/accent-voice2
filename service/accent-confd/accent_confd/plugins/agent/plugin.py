# Copyright 2023 Accent Communications

from .middleware import AgentMiddleWare
from .resource import AgentItem, AgentList
from .service import build_service


class Plugin:
    def load(self, dependencies):
        api = dependencies['api']
        middleware_handle = dependencies['middleware_handle']
        service = build_service()
        agent_middleware = AgentMiddleWare(service, middleware_handle)
        middleware_handle.register('agent', agent_middleware)

        api.add_resource(
            AgentList, '/agents', resource_class_args=(service, agent_middleware)
        )

        api.add_resource(
            AgentItem,
            '/agents/<int:id>',
            endpoint='agents',
            resource_class_args=(service, agent_middleware),
        )
