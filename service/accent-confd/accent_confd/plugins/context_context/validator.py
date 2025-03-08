# Copyright 2023 Accent Communications

from accent_dao.helpers import errors

from accent_confd.helpers.validator import ValidationAssociation, ValidatorAssociation


class ContextContextAssociationValidator(ValidatorAssociation):
    def validate(self, context, contexts):
        self.validate_no_duplicate_context(contexts)
        self.validate_no_self_context(context, contexts)

    def validate_no_duplicate_context(self, contexts):
        if len(contexts) != len(set(contexts)):
            raise errors.not_permitted('Cannot include same context more than once')

    def validate_no_self_context(self, context, contexts):
        if context in contexts:
            raise errors.not_permitted('Cannot include context inside itself')


def build_validator():
    return ValidationAssociation(association=[ContextContextAssociationValidator()])
