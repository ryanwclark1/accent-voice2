# Copyright 2023 Accent Communications

from accent_dao.resources.call_permission import dao as call_permission_dao

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
                lambda name, tenant_uuids: call_permission_dao.find_by(
                    name=name, tenant_uuids=tenant_uuids
                ),
                'CallPermission',
            )
        ],
        edit=[
            UniqueFieldChanged('name', call_permission_dao.find_by, 'CallPermission'),
        ],
    )
