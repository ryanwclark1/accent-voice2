# Copyright 2023 Accent Communications

from flask import request

from accent_confd.auth import required_acl
from accent_confd.helpers.restful import ConfdResource

from .schema import GroupFallbackSchema


class GroupFallbackList(ConfdResource):
    schema = GroupFallbackSchema

    def __init__(self, service, group_dao):
        super().__init__()
        self.service = service
        self.group_dao = group_dao

    @required_acl('confd.groups.{group_uuid}.fallbacks.read')
    def get(self, group_uuid):
        group = self.group_dao.get(group_uuid)
        return self.schema().dump(group.fallbacks)

    @required_acl('confd.groups.{group_uuid}.fallbacks.update')
    def put(self, group_uuid):
        group = self.group_dao.get(group_uuid)
        fallbacks = self.schema().load(request.get_json())
        self.service.edit(group, fallbacks)
        return '', 204
