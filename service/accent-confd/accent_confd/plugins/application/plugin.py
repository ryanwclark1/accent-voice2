# Copyright 2023 Accent Communications

from .resource import ApplicationItem, ApplicationList
from .service import build_service


class Plugin:
    def load(self, dependencies):
        api = dependencies['api']
        service = build_service()

        api.add_resource(
            ApplicationList, '/applications', resource_class_args=(service,)
        )

        api.add_resource(
            ApplicationItem,
            '/applications/<uuid:application_uuid>',
            endpoint='applications',
            resource_class_args=(service,),
        )
