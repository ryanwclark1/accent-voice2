# Copyright 2023 Accent Communications

from accent_confd.helpers.destination import DestinationValidator
from accent_confd.helpers.validator import ValidationGroup, Validator


class GroupFallbackValidator(Validator):
    def __init__(self, destination_validator):
        self._destination_validator = destination_validator

    def validate(self, fallbacks):
        for fallback in fallbacks.values():
            if fallback is not None:
                self._destination_validator.validate(fallback)


def build_validator():
    fallbacks_validator = GroupFallbackValidator(DestinationValidator())

    return ValidationGroup(edit=[fallbacks_validator])
