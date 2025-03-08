# Copyright 2023 Accent Communications

from accent_dao.helpers import errors
from accent_dao.resources.context import dao as context_dao_module

from accent_confd.helpers.validator import (
    GetResource,
    Optional,
    ValidationGroup,
    Validator,
)


class ContextTenantValidator(Validator):
    def __init__(self, context_dao_module):
        self.context_dao = context_dao_module

    def validate(self, trunk):
        context = self.context_dao.find_by(name=trunk.context)
        if not context:
            return

        if trunk.tenant_uuid != context.tenant_uuid:
            raise errors.different_tenants(
                trunk_tenant_uuid=trunk.tenant_uuid,
                context_tenant_uuid=context.tenant_uuid,
            )


def build_validator():
    return ValidationGroup(
        create=[
            Optional(
                'context',
                GetResource('context', context_dao_module.get_by_name, 'Context'),
            ),
            ContextTenantValidator(context_dao_module),
        ],
        edit=[
            Optional(
                'context',
                GetResource('context', context_dao_module.get_by_name, 'Context'),
            ),
            ContextTenantValidator(context_dao_module),
        ],
    )
