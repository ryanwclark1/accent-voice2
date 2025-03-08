# Copyright 2023 Accent Communications

from .notifier import build_notifier
from .validator import build_validator


class OutcallExtensionService:
    def __init__(self, notifier, validator):
        self.notifier = notifier
        self.validator = validator

    def associate(self, outcall, extension, outcall_extension):
        if extension in outcall.extensions:
            outcall.update_extension_association(extension, **outcall_extension)
            return

        self.validator.validate_association(outcall, extension)
        outcall.associate_extension(extension, **outcall_extension)
        self.notifier.associated(outcall, extension)

    def dissociate(self, outcall, extension):
        if extension not in outcall.extensions:
            return

        self.validator.validate_dissociation(outcall, extension)
        outcall.dissociate_extension(extension)
        self.notifier.dissociated(outcall, extension)


def build_service():
    return OutcallExtensionService(build_notifier(), build_validator())
