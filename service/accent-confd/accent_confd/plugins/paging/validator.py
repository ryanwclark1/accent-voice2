# Copyright 2023 Accent Communications

from accent_dao.resources.paging import dao as paging_dao

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
                'number', lambda number: paging_dao.find_by(number=number), 'Paging'
            )
        ],
        edit=[
            Optional(
                'number', UniqueFieldChanged('number', paging_dao.find_by, 'Paging')
            )
        ],
    )
