# Copyright 2023 Accent Communications

from .resource import AccessFeatureItem, AccessFeatureList
from .service import build_service


class Plugin:
    def load(self, dependencies):
        api = dependencies['api']
        service = build_service()

        api.add_resource(
            AccessFeatureList, '/access_features', resource_class_args=(service,)
        )

        api.add_resource(
            AccessFeatureItem,
            '/access_features/<int:id>',
            endpoint='access_features',
            resource_class_args=(service,),
        )
