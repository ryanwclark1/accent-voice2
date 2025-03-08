# Copyright 2023 Accent Communications

from accent_confd.auth import required_acl
from accent_confd.helpers.restful import ListResource

from .schema import UserCallerIDSchema


class UserCallerIDList(ListResource):
    schema = UserCallerIDSchema
    has_tenant_uuid = True

    def __init__(self, service, user_dao):
        self.service = service
        self.user_dao = user_dao

    @required_acl('confd.users.{user_id}.callerids.outgoing.read')
    def get(self, user_id):
        params = {}  # NOTE: search is not implemented
        tenant_uuids = self._build_tenant_list({'recurse': True})
        user = self.user_dao.get_by_id_uuid(user_id, tenant_uuids=tenant_uuids)
        total, items = self.service.search(user.id, user.tenant_uuid, params)
        return {'total': total, 'items': self.schema().dump(items, many=True)}

    def post(self):
        return '', 405
