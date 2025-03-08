# Copyright 2023 Accent Communications

from accent_dao.helpers import errors

from accent_confd.helpers.validator import ValidationAssociation, ValidatorAssociation


class SwitchboardMemberUserValidator(ValidatorAssociation):
    def validate(self, switchboard, users):
        self.validate_same_tenant(switchboard, users)

    def validate_same_tenant(self, switchboard, users):
        for user in users:
            if switchboard.tenant_uuid != user.tenant_uuid:
                raise errors.different_tenants(
                    switchboard_tenant_uuid=switchboard.tenant_uuid,
                    user_tenant_uuid=user.tenant_uuid,
                )


def build_validator():
    return ValidationAssociation(association=[SwitchboardMemberUserValidator()])
