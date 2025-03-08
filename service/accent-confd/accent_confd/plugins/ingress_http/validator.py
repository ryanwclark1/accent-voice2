# Copyright 2023 Accent Communications

from accent_dao.helpers import errors
from accent_dao.resources.ingress_http import dao

from accent_confd.helpers.validator import ValidationGroup, Validator


class CreateIngressHTTPSingleInstanceByTenantValidator(Validator):
    def __init__(self, dao):
        self.dao = dao

    def validate(self, ingress_http):
        existing = self.dao.find_by(tenant_uuid=ingress_http.tenant_uuid)

        if existing:
            raise errors.resource_exists(
                'IngressHTTP',
                tenant_uuid=str(ingress_http.tenant_uuid),
            )


def build_validator():
    return ValidationGroup(
        create=[CreateIngressHTTPSingleInstanceByTenantValidator(dao)],
    )
