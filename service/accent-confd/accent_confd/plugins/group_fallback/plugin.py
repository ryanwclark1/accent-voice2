# Copyright 2023 Accent Communications

from accent_dao.resources.group import dao as group_dao

from .resource import GroupFallbackList
from .service import build_service


class Plugin:
    def load(self, dependencies):
        api = dependencies['api']
        service = build_service()

        api.add_resource(
            GroupFallbackList,
            '/groups/<int:group_uuid>/fallbacks',
            '/groups/<uuid:group_uuid>/fallbacks',
            resource_class_args=(service, group_dao),
        )
