# Copyright 2023 Accent Communications

from marshmallow import fields

from accent_confd.auth import required_acl
from accent_confd.helpers.mallow import BaseSchema, Link, ListLink
from accent_confd.helpers.restful import ConfdResource


class UserCallPermissionSchema(BaseSchema):
    user_id = fields.Integer()
    call_permission_id = fields.Integer()
    links = ListLink(
        Link('users', field='user_id', target='id'),
        Link('callpermissions', field='call_permission_id', target='id'),
    )


class UserCallPermission(ConfdResource):
    def __init__(self, service, user_dao, call_permission_dao):
        super().__init__()
        self.service = service
        self.user_dao = user_dao
        self.call_permission_dao = call_permission_dao


class UserCallPermissionAssociation(UserCallPermission):
    has_tenant_uuid = True

    @required_acl('confd.users.{user_id}.callpermissions.{call_permission_id}.update')
    def put(self, user_id, call_permission_id):
        tenant_uuids = self._build_tenant_list({'recurse': True})
        user = self.user_dao.get_by_id_uuid(user_id, tenant_uuids=tenant_uuids)
        call_permission = self.call_permission_dao.get(
            call_permission_id, tenant_uuids=tenant_uuids
        )
        self.service.associate(user, call_permission)
        return '', 204

    @required_acl('confd.users.{user_id}.callpermissions.{call_permission_id}.delete')
    def delete(self, user_id, call_permission_id):
        tenant_uuids = self._build_tenant_list({'recurse': True})
        user = self.user_dao.get_by_id_uuid(user_id, tenant_uuids=tenant_uuids)
        call_permission = self.call_permission_dao.get(
            call_permission_id, tenant_uuids=tenant_uuids
        )
        self.service.dissociate(user, call_permission)
        return '', 204
