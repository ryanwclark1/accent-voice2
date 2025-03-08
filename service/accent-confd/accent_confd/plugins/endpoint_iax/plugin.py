# Copyright 2023 Accent Communications

from .resource import IAXItem, IAXList
from .service import build_service


class Plugin:
    def load(self, dependencies):
        api = dependencies['api']

        service = build_service()

        api.add_resource(
            IAXItem,
            '/endpoints/iax/<int:id>',
            endpoint='endpoint_iax',
            resource_class_args=(service,),
        )
        api.add_resource(IAXList, '/endpoints/iax', resource_class_args=(service,))
