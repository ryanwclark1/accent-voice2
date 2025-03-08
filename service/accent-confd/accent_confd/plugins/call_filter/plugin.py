# Copyright 2023 Accent Communications

from .resource import CallFilterItem, CallFilterList
from .service import build_service


class Plugin:
    def load(self, dependencies):
        api = dependencies['api']
        service = build_service()

        api.add_resource(CallFilterList, '/callfilters', resource_class_args=(service,))

        api.add_resource(
            CallFilterItem,
            '/callfilters/<int:id>',
            endpoint='callfilters',
            resource_class_args=(service,),
        )
