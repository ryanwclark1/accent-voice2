# Copyright 2023 Accent Communications

from accent_dao.resources.skill import dao as skill_dao

from accent_confd.helpers.validator import (
    UniqueField,
    UniqueFieldChanged,
    ValidationGroup,
)


def build_validator():
    return ValidationGroup(
        create=[
            UniqueField(
                'name',
                lambda name, tenant_uuids: skill_dao.find_by(
                    name=name, tenant_uuids=tenant_uuids
                ),
                'Skill',
            )
        ],
        edit=[UniqueFieldChanged('name', skill_dao.find_by, 'Skill')],
    )
