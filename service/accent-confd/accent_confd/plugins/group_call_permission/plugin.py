# Copyright 2023 Accent Communications

from accent_dao.resources.call_permission import dao as call_permission_dao
from accent_dao.resources.group import dao as group_dao

from .resource import GroupCallPermissionAssociation
from .service import build_service


class Plugin:
    def load(self, dependencies):
        api = dependencies['api']
        service = build_service()

        api.add_resource(
            GroupCallPermissionAssociation,
            '/groups/<int:group_uuid>/callpermissions/<int:call_permission_id>',
            '/groups/<uuid:group_uuid>/callpermissions/<int:call_permission_id>',
            endpoint='group_call_permissions',
            resource_class_args=(service, group_dao, call_permission_dao),
        )
