# Copyright 2023 Accent Communications

from .resource import ConferenceItem, ConferenceList
from .service import build_service


class Plugin:
    def load(self, dependencies):
        api = dependencies['api']
        service = build_service()

        api.add_resource(ConferenceList, '/conferences', resource_class_args=(service,))

        api.add_resource(
            ConferenceItem,
            '/conferences/<int:id>',
            endpoint='conferences',
            resource_class_args=(service,),
        )
