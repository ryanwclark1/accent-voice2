# Copyright 2023 Accent Communications

from accent_dao.resources.endpoint_iax import dao as iax_dao

from accent_confd.helpers.validator import (
    Optional,
    UniqueField,
    UniqueFieldChanged,
    ValidationGroup,
)


def build_validator():
    return ValidationGroup(
        create=[
            Optional(
                'name',
                UniqueField(
                    'name', lambda value: iax_dao.find_by(name=value), 'IAXEndpoint'
                ),
            )
        ],
        edit=[
            Optional('name', UniqueFieldChanged('name', iax_dao.find_by, 'IAXEndpoint'))
        ],
    )
