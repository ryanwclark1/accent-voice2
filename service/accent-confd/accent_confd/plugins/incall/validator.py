# Copyright 2023 Accent Communications

from accent_confd.helpers.destination import DestinationValidator
from accent_confd.helpers.validator import ValidationGroup, Validator


class IncallModelValidator(Validator):
    def __init__(self, destination_validator):
        self._destination_validator = destination_validator

    def validate(self, incall):
        self._destination_validator.validate(incall.destination)


def build_validator():
    incall_validator = IncallModelValidator(DestinationValidator())

    return ValidationGroup(create=[incall_validator], edit=[incall_validator])
