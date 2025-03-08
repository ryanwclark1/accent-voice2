# Copyright 2023 Accent Communications

from accent.tenant_flask_helpers import Tenant

from accent_calld.auth import required_acl
from accent_calld.http import AuthResource

from .schemas import line_endpoint_schema, trunk_endpoint_schema


class LineEndpoints(AuthResource):
    def __init__(self, endpoints_service):
        self._endpoints_service = endpoints_service

    @required_acl('calld.lines.read')
    def get(self):
        tenant_uuid = Tenant.autodetect().uuid

        items, total, filtered = self._endpoints_service.list_lines(tenant_uuid)
        result = {
            'items': line_endpoint_schema.dump(items, many=True),
            'total': total,
            'filtered': filtered,
        }

        return result, 200


class TrunkEndpoints(AuthResource):
    def __init__(self, endpoints_service):
        self._endpoints_service = endpoints_service

    @required_acl('calld.trunks.read')
    def get(self):
        tenant_uuid = Tenant.autodetect().uuid

        items, total, filtered = self._endpoints_service.list_trunks(tenant_uuid)
        result = {
            'items': trunk_endpoint_schema.dump(items, many=True),
            'total': total,
            'filtered': filtered,
        }

        return result, 200
