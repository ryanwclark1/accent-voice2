# Copyright 2023 Accent Communications

from accent.rest_api_helpers import APIException


class DeleteOwnTenantForbidden(APIException):
    def __init__(self, tenant_uuid):
        details = {'tenant_uuid': str(tenant_uuid)}
        msg = f'Deleting its own tenant is forbidden: "{tenant_uuid}"'
        error_id = 'deleting-own-tenant-forbidden'
        super().__init__(403, msg, error_id, details, resource='tenants')
