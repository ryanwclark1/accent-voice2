# Copyright 2023 Accent Communications

from accent_dao.resources.queue import dao as queue_dao
from accent_dao.resources.user import dao as user_dao

from .middleware import QueueMemberMiddleWare
from .resource import (
    QueueMemberAgentItem,
    QueueMemberUserItem,
)
from .service import build_service


class Plugin:
    def load(self, dependencies):
        api = dependencies['api']
        middleware_handle = dependencies['middleware_handle']

        service = build_service()

        queue_member_middleware = QueueMemberMiddleWare(service)
        middleware_handle.register('queue_member', queue_member_middleware)

        api.add_resource(
            QueueMemberAgentItem,
            '/queues/<int:queue_id>/members/agents/<int:agent_id>',
            endpoint='queue_member_agents',
            resource_class_args=(queue_member_middleware,),
        )

        api.add_resource(
            QueueMemberUserItem,
            '/queues/<int:queue_id>/members/users/<uuid:user_id>',
            '/queues/<int:queue_id>/members/users/<int:user_id>',
            endpoint='queue_member_users',
            resource_class_args=(service, queue_dao, user_dao),
        )
