# Copyright 2023 Accent Communications

from accent_dao.alchemy.rightcall import RightCall as CallPermission
from flask import url_for

from accent_confd.auth import required_acl
from accent_confd.helpers.restful import ItemResource, ListResource

from .schema import CallPermissionSchema


class CallPermissionList(ListResource):
    model = CallPermission
    schema = CallPermissionSchema

    def build_headers(self, call_permission):
        return {
            'Location': url_for(
                'callpermissions', id=call_permission.id, _external=True
            )
        }

    @required_acl('confd.callpermissions.create')
    def post(self):
        return super().post()

    @required_acl('confd.callpermissions.read')
    def get(self):
        return super().get()


class CallPermissionItem(ItemResource):
    schema = CallPermissionSchema
    has_tenant_uuid = True

    @required_acl('confd.callpermissions.{id}.read')
    def get(self, id):
        return super().get(id)

    @required_acl('confd.callpermissions.{id}.update')
    def put(self, id):
        return super().put(id)

    @required_acl('confd.callpermissions.{id}.delete')
    def delete(self, id):
        return super().delete(id)
