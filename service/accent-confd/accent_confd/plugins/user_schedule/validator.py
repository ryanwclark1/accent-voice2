# Copyright 2023 Accent Communications

from accent_dao.helpers import errors

from accent_confd.helpers.validator import ValidationAssociation, ValidatorAssociation


class UserScheduleAssociationValidator(ValidatorAssociation):
    def validate(self, user, schedule):
        self.validate_same_tenant(user, schedule)
        self.validate_user_not_already_associated(user)

    def validate_same_tenant(self, user, schedule):
        if user.tenant_uuid != schedule.tenant_uuid:
            raise errors.different_tenants(
                user_tenant_uuid=user.tenant_uuid,
                schedule_tenant_uuid=schedule.tenant_uuid,
            )

    def validate_user_not_already_associated(self, user):
        if user.schedules:
            raise errors.resource_associated(
                'User', 'Schedule', user_id=user.id, schedule_id=user.schedules[0].id
            )


def build_validator():
    return ValidationAssociation(association=[UserScheduleAssociationValidator()])
