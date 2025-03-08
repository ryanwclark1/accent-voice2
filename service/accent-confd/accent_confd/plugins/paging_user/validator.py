# Copyright 2023 Accent Communications

from accent_dao.helpers import errors

from accent_confd.helpers.validator import ValidationAssociation, ValidatorAssociation


class PagingUserAssociationValidator(ValidatorAssociation):
    def validate(self, paging, users):
        for user in users:
            self.validate_same_tenant(paging, user)
        self.validate_no_duplicate_user(users)

    def validate_same_tenant(self, paging, user):
        if paging.tenant_uuid != user.tenant_uuid:
            raise errors.different_tenants(
                paging_tenant_uuid=paging.tenant_uuid, user_tenant_uuid=user.tenant_uuid
            )

    def validate_no_duplicate_user(self, users):
        if len(users) != len(set(users)):
            raise errors.not_permitted('Cannot associate same user more than once')


def build_validator():
    return ValidationAssociation(association=[PagingUserAssociationValidator()])
