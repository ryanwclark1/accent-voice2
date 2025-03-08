# Copyright 2023 Accent Communications

from accent_dao.alchemy.tenant import Tenant
from flask import url_for

from accent_confd.auth import required_acl
from accent_confd.helpers.restful import ItemResource, ListResource

from .schema import TenantSchema


class TenantList(ListResource):
    model = Tenant
    schema = TenantSchema
    has_tenant_uuid = True

    def build_headers(self, tenant):
        return {'Location': url_for('tenants', uuid=tenant.uuid, _external=True)}

    @required_acl('confd.tenants.read')
    def get(self):
        return super().get()


class TenantItem(ItemResource):
    schema = TenantSchema
    has_tenant_uuid = True

    @required_acl('confd.tenants.{uuid}.read')
    def get(self, uuid):
        return super().get(str(uuid))
