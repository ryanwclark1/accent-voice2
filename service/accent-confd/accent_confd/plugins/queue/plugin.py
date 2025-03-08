# Copyright 2023 Accent Communications

from .resource import QueueItem, QueueList
from .service import build_service


class Plugin:
    def load(self, dependencies):
        api = dependencies['api']
        service = build_service()

        api.add_resource(QueueList, '/queues', resource_class_args=(service,))

        api.add_resource(
            QueueItem,
            '/queues/<int:id>',
            endpoint='queues',
            resource_class_args=(service,),
        )
