# Copyright 2023 Accent Communications

from accent_dao.helpers import errors
from accent_dao.resources.context import dao as context_dao
from accent_dao.resources.line import dao as line_dao

from accent_confd.helpers.validator import (
    GetResource,
    Optional,
    ValidationGroup,
    Validator,
)


class ProvCodeAvailable(Validator):
    def __init__(self, dao):
        self.dao = dao

    def validate(self, line):
        existing = self.dao.find_by(provisioningid=line.provisioningid)
        if existing:
            raise errors.resource_exists(
                'Line', provisioning_code=line.provisioning_code
            )


class ProvCodeChanged(ProvCodeAvailable):
    def validate(self, line):
        old_line = self.dao.get(line.id)
        if old_line.provisioning_code != line.provisioning_code:
            super().validate(line)


def build_validator(registrar_dao):
    return ValidationGroup(
        create=[
            Optional('provisioning_code', ProvCodeAvailable(line_dao)),
            Optional(
                'registrar', GetResource('registrar', registrar_dao.get, 'Registrar')
            ),
            GetResource('context', context_dao.get_by_name, 'Context'),
        ],
        edit=[
            ProvCodeChanged(line_dao),
            GetResource('registrar', registrar_dao.get, 'Registrar'),
            GetResource('context', context_dao.get_by_name, 'Context'),
        ],
    )
