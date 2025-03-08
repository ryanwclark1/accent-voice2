# Copyright 2023 Accent Communications

from flask import request

from accent_confd.auth import required_acl
from accent_confd.helpers.restful import ConfdResource

from .schema import CallFilterFallbackSchema


class CallFilterFallbackList(ConfdResource):
    schema = CallFilterFallbackSchema
    has_tenant_uuid = True

    def __init__(self, service, call_filter_dao):
        super().__init__()
        self.service = service
        self.call_filter_dao = call_filter_dao

    @required_acl('confd.callfilters.{call_filter_id}.fallbacks.read')
    def get(self, call_filter_id):
        tenant_uuids = self._build_tenant_list({'recurse': True})
        call_filter = self.call_filter_dao.get(
            call_filter_id, tenant_uuids=tenant_uuids
        )
        return self.schema().dump(call_filter.fallbacks)

    @required_acl('confd.callfilters.{call_filter_id}.fallbacks.update')
    def put(self, call_filter_id):
        tenant_uuids = self._build_tenant_list({'recurse': True})
        call_filter = self.call_filter_dao.get(
            call_filter_id, tenant_uuids=tenant_uuids
        )
        fallbacks = self.schema().load(request.get_json())
        self.service.edit(call_filter, fallbacks)
        return '', 204
