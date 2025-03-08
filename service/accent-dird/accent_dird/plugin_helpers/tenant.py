# Copyright 2023 Accent Communications

from accent.tenant_flask_helpers import Tenant, token


def get_tenant_uuids(recurse=False):
    tenant_uuid = Tenant.autodetect().uuid
    if not recurse:
        return [tenant_uuid]
    return [tenant.uuid for tenant in token.visible_tenants(tenant_uuid)]
