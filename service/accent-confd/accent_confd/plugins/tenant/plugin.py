# Copyright 2023 Accent Communications

from .resource import TenantItem, TenantList
from .service import build_service


class Plugin:
    def load(self, dependencies):
        api = dependencies['api']
        service = build_service()

        api.add_resource(
            TenantList,
            '/tenants',
            resource_class_args=[service],
        )
        api.add_resource(
            TenantItem,
            '/tenants/<uuid:uuid>',
            endpoint='tenants',
            resource_class_args=[service],
        )
