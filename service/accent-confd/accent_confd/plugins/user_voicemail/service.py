# Copyright 2023 Accent Communications

from accent_dao.resources.user_voicemail import dao as user_voicemail_dao

from .notifier import build_notifier
from .validator import build_validator


class UserVoicemailService:
    def __init__(self, dao, validator, notifier):
        self.dao = dao
        self.validator = validator
        self.notifier = notifier

    def get_by(self, **criteria):
        return self.dao.get_by(**criteria)

    def find_by(self, **criteria):
        return self.dao.find_by(**criteria)

    def associate(self, user, voicemail):
        if voicemail is user.voicemail:
            return self.dao.get_by(user_id=user.id)

        self.validator.validate_association(user, voicemail)
        self.dao.associate(user, voicemail)
        self.notifier.associated(user, voicemail)
        return self.dao.get_by(user_id=user.id)

    def dissociate(self, user, voicemail):
        if voicemail is not user.voicemail:
            return

        self.validator.validate_dissociation(user, voicemail)
        self.dao.dissociate(user, voicemail)
        self.notifier.dissociated(user, voicemail)

    def dissociate_all_by_user(self, user):
        if user.voicemail:
            self.dissociate(user, user.voicemail)


def build_service():
    return UserVoicemailService(user_voicemail_dao, build_validator(), build_notifier())
