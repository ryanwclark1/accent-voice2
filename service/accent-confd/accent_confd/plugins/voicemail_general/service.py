# Copyright 2023 Accent Communications

from accent_dao.resources.voicemail_general import dao as voicemail_general_dao

from .notifier import build_notifier


class VoicemailGeneralService:
    def __init__(self, dao, notifier):
        self.dao = dao
        self.notifier = notifier

    def list(self):
        return self.dao.find_all()

    def edit(self, resource):
        self.dao.edit_all(resource)
        self.notifier.edited(resource)


def build_service():
    return VoicemailGeneralService(voicemail_general_dao, build_notifier())
