# Copyright 2023 Accent Communications

from .resource import ExtensionFeatureItem, ExtensionFeatureList
from .service import build_service


class Plugin:
    def load(self, dependencies):
        api = dependencies['api']

        service = build_service()

        api.add_resource(
            ExtensionFeatureItem,
            '/extensions/features/<uuid:uuid>',
            endpoint='extensions_features',
            resource_class_args=(service,),
        )
        api.add_resource(
            ExtensionFeatureList, '/extensions/features', resource_class_args=(service,)
        )
