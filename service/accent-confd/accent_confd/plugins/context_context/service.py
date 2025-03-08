# Copyright 2023 Accent Communications

from .notifier import build_notifier
from .validator import build_validator


class ContextContextService:
    def __init__(self, context_dao, notifier, validator):
        self.context_dao = context_dao
        self.notifier = notifier
        self.validator = validator

    def associate_contexts(self, context, contexts):
        self.validator.validate_association(context, contexts)
        self.context_dao.associate_contexts(context, contexts)
        self.notifier.associated_contexts(context, contexts)


def build_service(context_dao):
    return ContextContextService(context_dao, build_notifier(), build_validator())
