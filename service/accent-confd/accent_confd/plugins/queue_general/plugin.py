# Copyright 2023 Accent Communications

from .resource import QueueGeneralList
from .service import build_service


class Plugin:
    def load(self, dependencies):
        api = dependencies['api']
        service = build_service()

        api.add_resource(
            QueueGeneralList, '/asterisk/queues/general', resource_class_args=(service,)
        )
