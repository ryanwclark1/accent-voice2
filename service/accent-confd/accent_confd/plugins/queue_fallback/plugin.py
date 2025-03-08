# Copyright 2023 Accent Communications

from accent_dao.resources.queue import dao as queue_dao

from .resource import QueueFallbackList
from .service import build_service


class Plugin:
    def load(self, dependencies):
        api = dependencies['api']
        service = build_service()

        api.add_resource(
            QueueFallbackList,
            '/queues/<int:queue_id>/fallbacks',
            resource_class_args=(service, queue_dao),
        )
