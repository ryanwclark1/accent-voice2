# Copyright 2023 Accent Communications

from accent_dao.resources.extension import dao as extension_dao_module

from .notifier import build_notifier
from .validator import build_validator


class GroupExtensionService:
    def __init__(self, extension_dao, notifier, validator):
        self.extension_dao = extension_dao
        self.validator = validator
        self.notifier = notifier

    def associate(self, group, extension):
        if extension in group.extensions:
            return

        self.validator.validate_association(group, extension)
        self.extension_dao.associate_group(group, extension)
        self.notifier.associated(group, extension)

    def dissociate(self, group, extension):
        if extension not in group.extensions:
            return

        self.validator.validate_dissociation(group, extension)
        self.extension_dao.dissociate_group(group, extension)
        self.notifier.dissociated(group, extension)


def build_service():
    return GroupExtensionService(
        extension_dao_module, build_notifier(), build_validator()
    )
