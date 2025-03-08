# Copyright 2023 Accent Communications

from accent_dao.resources.voicemail_zonemessages import dao as voicemail_zonemessages_dao

from .notifier import build_notifier


class VoicemailZoneMessagesService:
    def __init__(self, dao, notifier):
        self.dao = dao
        self.notifier = notifier

    def list(self):
        return self.dao.find_all()

    def edit(self, resource):
        self.dao.edit_all(resource)
        self.notifier.edited(resource)


def build_service():
    return VoicemailZoneMessagesService(voicemail_zonemessages_dao, build_notifier())
