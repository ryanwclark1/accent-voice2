# Copyright 2023 Accent Communications

from .resource import TrunkItem, TrunkList
from .service import build_service


class Plugin:
    def load(self, dependencies):
        api = dependencies['api']
        service = build_service()

        api.add_resource(TrunkList, '/trunks', resource_class_args=(service,))

        api.add_resource(
            TrunkItem,
            '/trunks/<int:id>',
            endpoint='trunks',
            resource_class_args=(service,),
        )
