# Copyright 2023 Accent Communications

from .resource import PagingItem, PagingList
from .service import build_service


class Plugin:
    def load(self, dependencies):
        api = dependencies['api']
        service = build_service()

        api.add_resource(PagingList, '/pagings', resource_class_args=(service,))

        api.add_resource(
            PagingItem,
            '/pagings/<int:id>',
            endpoint='pagings',
            resource_class_args=(service,),
        )
