# Copyright 2023 Accent Communications

from accent_dao.helpers import errors

from accent_confd.helpers.validator import ValidationAssociation, ValidatorAssociation


class GroupScheduleAssociationValidator(ValidatorAssociation):
    def validate(self, group, schedule):
        self.validate_same_tenant(group, schedule)
        self.validate_group_not_already_associated(group)

    def validate_same_tenant(self, group, schedule):
        if group.tenant_uuid != schedule.tenant_uuid:
            raise errors.different_tenants(
                group_tenant_uuid=group.tenant_uuid,
                schedule_tenant_uuid=schedule.tenant_uuid,
            )

    def validate_group_not_already_associated(self, group):
        if group.schedules:
            raise errors.resource_associated(
                'Group',
                'Schedule',
                group_uuid=group.uuid,
                schedule_id=group.schedules[0].id,
            )


def build_validator():
    return ValidationAssociation(association=[GroupScheduleAssociationValidator()])
