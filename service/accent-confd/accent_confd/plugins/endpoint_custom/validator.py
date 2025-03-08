# Copyright 2023 Accent Communications

from accent_dao.resources.endpoint_custom import dao as custom_dao

from accent_confd.helpers.validator import (
    UniqueField,
    UniqueFieldChanged,
    ValidationGroup,
)


def find_by_interface(interface):
    return custom_dao.find_by(interface=interface)


def build_validator():
    return ValidationGroup(
        create=[UniqueField('interface', find_by_interface, 'CustomEndpoint')],
        edit=[UniqueFieldChanged('interface', custom_dao.find_by, 'CustomEndpoint')],
    )
