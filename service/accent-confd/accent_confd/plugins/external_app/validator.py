# Copyright 2023 Accent Communications

from accent_dao.helpers import errors
from accent_dao.resources.external_app import dao as external_app_dao

from accent_confd.helpers.validator import ValidationGroup, Validator


class UniqueNameField(Validator):
    def __init__(self, dao):
        self.dao = dao

    def validate(self, external_app):
        tenant_uuid = external_app.tenant_uuid
        name = external_app.name
        found = self.dao.find_by(tenant_uuid=tenant_uuid, name=name)
        if found is not None:
            metadata = {'tenant_uuid': tenant_uuid, 'name': name}
            raise errors.resource_exists('ExternalApp', **metadata)


def build_validator():
    return ValidationGroup(
        create=[UniqueNameField(external_app_dao)],
    )
