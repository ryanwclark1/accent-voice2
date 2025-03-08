# Copyright 2023 Accent Communications

from accent_dao.resources.call_filter import dao as call_filter_dao

from accent_confd.helpers.validator import (
    Optional,
    UniqueField,
    UniqueFieldChanged,
    ValidationGroup,
)


def build_validator():
    return ValidationGroup(
        create=[
            UniqueField(
                'name', lambda name: call_filter_dao.find_by(name=name), 'CallFilter'
            )
        ],
        edit=[
            Optional(
                'name',
                UniqueFieldChanged('name', call_filter_dao.find_by, 'CallFilter'),
            )
        ],
    )
