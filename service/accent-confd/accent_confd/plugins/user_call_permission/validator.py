# Copyright 2023 Accent Communications

from accent_dao.helpers import errors

from accent_confd.helpers.validator import ValidationAssociation, Validator


class AssociateUserCallPermission(Validator):
    def validate(self, user, call_permission):
        self.validate_same_tenant(user, call_permission)

    def validate_same_tenant(self, user, call_permission):
        if user.tenant_uuid != call_permission.tenant_uuid:
            raise errors.different_tenants(
                user_tenant_uuid=user.tenant_uuid,
                call_permission_tenant_uuid=call_permission.tenant_uuid,
            )


def build_validator():
    return ValidationAssociation(association=[AssociateUserCallPermission()])
