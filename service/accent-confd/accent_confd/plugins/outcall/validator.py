# Copyright 2023 Accent Communications

from accent_dao.resources.outcall import dao as outcall_dao

from accent_confd.helpers.validator import (
    UniqueField,
    UniqueFieldChanged,
    ValidationGroup,
)


def build_validator():
    return ValidationGroup(
        create=[
            UniqueField('name', lambda name: outcall_dao.find_by(name=name), 'Outcall')
        ],
        edit=[UniqueFieldChanged('name', outcall_dao.find_by, 'Outcall')],
    )
