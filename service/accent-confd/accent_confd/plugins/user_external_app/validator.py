# Copyright 2023 Accent Communications

from accent_dao.helpers import errors
from accent_dao.resources.user_external_app import dao as user_external_app_dao

from accent_confd.helpers.validator import ValidationGroup, Validator


class UniqueNameField(Validator):
    def __init__(self, dao):
        self.dao = dao

    def validate(self, external_app):
        user_uuid = external_app.user_uuid
        name = external_app.name
        found = self.dao.find_by(user_uuid=user_uuid, name=name)
        if found is not None:
            metadata = {'user_uuid': user_uuid, 'name': name}
            raise errors.resource_exists('UserExternalApp', **metadata)


def build_validator():
    return ValidationGroup(
        create=[UniqueNameField(user_external_app_dao)],
    )
