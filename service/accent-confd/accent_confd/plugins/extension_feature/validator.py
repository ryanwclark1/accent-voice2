# Copyright 2023 Accent Communications

from accent_dao.helpers import errors
from accent_dao.resources.feature_extension import dao as feature_extension_dao

from accent_confd.helpers.validator import ValidationGroup, Validator


class ExtenAvailableOnUpdateValidator(Validator):
    def __init__(self, dao):
        self.dao = dao

    def validate(self, extension):
        existing = self.dao.find_by(exten=extension.exten)
        if existing and existing.uuid != extension.uuid:
            raise errors.resource_exists('FeatureExtension', exten=extension.exten)


def build_validator():
    return ValidationGroup(
        edit=[ExtenAvailableOnUpdateValidator(feature_extension_dao)]
    )
