# Copyright 2023 Accent Communications

from accent_dao.resources.call_pickup import dao as call_pickup_dao

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
                'name', lambda name: call_pickup_dao.find_by(name=name), 'CallPickup'
            )
        ],
        edit=[
            Optional(
                'name',
                UniqueFieldChanged('name', call_pickup_dao.find_by, 'CallPickup'),
            )
        ],
    )
