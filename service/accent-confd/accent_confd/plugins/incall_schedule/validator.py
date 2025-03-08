# Copyright 2023 Accent Communications

from accent_dao.helpers import errors

from accent_confd.helpers.validator import ValidationAssociation, ValidatorAssociation


class IncallScheduleAssociationValidator(ValidatorAssociation):
    def validate(self, incall, schedule):
        self.validate_same_tenant(incall, schedule)
        self.validate_incall_not_already_associated(incall)

    def validate_same_tenant(self, incall, schedule):
        if incall.tenant_uuid != schedule.tenant_uuid:
            raise errors.different_tenants(
                incall_tenant_uuid=incall.tenant_uuid,
                schedule_tenant_uuid=schedule.tenant_uuid,
            )

    def validate_incall_not_already_associated(self, incall):
        if incall.schedules:
            raise errors.resource_associated(
                'Incall',
                'Schedule',
                incall_id=incall.id,
                schedule_id=incall.schedules[0].id,
            )


def build_validator():
    return ValidationAssociation(association=[IncallScheduleAssociationValidator()])
