# Copyright 2023 Accent Communications

from flask import request

from accent_dird.auth import required_acl
from accent_dird.http import AuthResource
from accent_dird.plugin_helpers.tenant import get_tenant_uuids

from .schemas import list_schema, source_list_schema


class Sources(AuthResource):
    def __init__(self, source_service):
        self._source_service = source_service

    @required_acl('dird.sources.read')
    def get(self):
        list_params = list_schema.load(request.args)
        visible_tenants = get_tenant_uuids(recurse=list_params['recurse'])
        backend = list_params.pop('backend', None)
        sources = self._source_service.list_(backend, visible_tenants, **list_params)
        items = source_list_schema.dump(sources)
        filtered = self._source_service.count(backend, visible_tenants, **list_params)
        total = self._source_service.count(None, visible_tenants)

        return {'total': total, 'filtered': filtered, 'items': items}
