# Copyright 2023 Accent Communications

from .http import (
    AgentsStatisticsResource,
    AgentStatisticsResource,
    QueuesStatisticsResource,
    QueueStatisticsQoSResource,
    QueueStatisticsResource,
)
from .services import AgentStatisticsService, QueueStatisticsService


class Plugin:
    def load(self, dependencies):
        api = dependencies['api']
        dao = dependencies['dao']

        queue_service = QueueStatisticsService(dao.queue_stat)
        agent_service = AgentStatisticsService(dao.agent_stat)

        api.add_resource(
            AgentsStatisticsResource,
            '/agents/statistics',
            resource_class_args=[agent_service],
        )
        api.add_resource(
            AgentStatisticsResource,
            '/agents/<int:agent_id>/statistics',
            resource_class_args=[agent_service],
        )
        api.add_resource(
            QueuesStatisticsResource,
            '/queues/statistics',
            resource_class_args=[queue_service],
        )
        api.add_resource(
            QueueStatisticsResource,
            '/queues/<int:queue_id>/statistics',
            resource_class_args=[queue_service],
        )
        api.add_resource(
            QueueStatisticsQoSResource,
            '/queues/<int:queue_id>/statistics/qos',
            resource_class_args=[queue_service],
        )
