# Copyright 2023 Accent Communications

from accent_dao.resources.extension import dao as extension_dao
from accent_dao.resources.group import dao as group_dao

from .resource import GroupExtensionItem
from .service import build_service


class Plugin:
    def load(self, dependencies):
        api = dependencies['api']
        service = build_service()

        api.add_resource(
            GroupExtensionItem,
            '/groups/<int:group_uuid>/extensions/<int:extension_id>',
            '/groups/<uuid:group_uuid>/extensions/<int:extension_id>',
            endpoint='group_extensions',
            resource_class_args=(service, group_dao, extension_dao),
        )
