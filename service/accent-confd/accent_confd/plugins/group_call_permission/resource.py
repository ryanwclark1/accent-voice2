# Copyright 2023 Accent Communications

from accent_confd.auth import required_acl
from accent_confd.helpers.restful import ConfdResource


class GroupCallPermissionAssociation(ConfdResource):
    has_tenant_uuid = True

    def __init__(self, service, group_dao, call_permission_dao):
        super().__init__()
        self.service = service
        self.group_dao = group_dao
        self.call_permission_dao = call_permission_dao

    @required_acl(
        'confd.groups.{group_uuid}.callpermissions.{call_permission_id}.update'
    )
    def put(self, group_uuid, call_permission_id):
        tenant_uuids = self._build_tenant_list({'recurse': True})
        group = self.group_dao.get(group_uuid, tenant_uuids=tenant_uuids)
        call_permission = self.call_permission_dao.get(
            call_permission_id, tenant_uuids=tenant_uuids
        )
        self.service.associate(group, call_permission)
        return '', 204

    @required_acl(
        'confd.groups.{group_uuid}.callpermissions.{call_permission_id}.delete'
    )
    def delete(self, group_uuid, call_permission_id):
        tenant_uuids = self._build_tenant_list({'recurse': True})
        group = self.group_dao.get(group_uuid, tenant_uuids=tenant_uuids)
        call_permission = self.call_permission_dao.get(
            call_permission_id, tenant_uuids=tenant_uuids
        )
        self.service.dissociate(group, call_permission)
        return '', 204
