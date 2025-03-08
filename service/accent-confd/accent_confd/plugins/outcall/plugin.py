# Copyright 2023 Accent Communications

from .resource import OutcallItem, OutcallList
from .service import build_service


class Plugin:
    def load(self, dependencies):
        api = dependencies['api']
        service = build_service()

        api.add_resource(OutcallList, '/outcalls', resource_class_args=(service,))

        api.add_resource(
            OutcallItem,
            '/outcalls/<int:id>',
            endpoint='outcalls',
            resource_class_args=(service,),
        )
