# Copyright 2023 Accent Communications

from accent_dao.helpers import errors
from accent_dao.resources.moh import dao as moh_dao

from accent_confd.helpers.validator import UniqueField, ValidationGroup, Validator


class MohModelValidator(Validator):
    def validate(self, moh):
        if moh.mode == 'custom' and moh.application is None:
            raise errors.moh_custom_no_app()


def build_validator():
    moh_validator = MohModelValidator()
    validation_group = ValidationGroup(
        create=[
            UniqueField('name', lambda name: moh_dao.find_by(name=name), 'MOH'),
            moh_validator,
        ],
        edit=[moh_validator],
    )

    return validation_group
