# Copyright 2023 Accent Communications

from accent_dao.helpers import errors

from accent_confd.helpers.validator import ValidationAssociation, Validator


class AssociateGroupCallPermission(Validator):
    def validate(self, group, call_permission):
        self.validate_same_tenant(group, call_permission)

    def validate_same_tenant(self, group, call_permission):
        if group.tenant_uuid != call_permission.tenant_uuid:
            raise errors.different_tenants(
                group_tenant_uuid=group.tenant_uuid,
                call_permission_tenant_uuid=call_permission.tenant_uuid,
            )


def build_validator():
    return ValidationAssociation(association=[AssociateGroupCallPermission()])
