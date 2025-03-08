# Copyright 2023 Accent Communications

from accent_dao.resources.meeting import dao as meeting_dao
from accent_dao.resources.meeting_authorization import dao

from accent_confd.helpers.resource import CRUDService

from .validator import build_validator


class MeetingAuthorizationService(CRUDService):
    def search(self, parameters, meeting_uuid):
        return self.dao.search(meeting_uuid, **parameters)

    def create(self, meeting_authorization):
        self._set_status(meeting_authorization)
        return super().create(meeting_authorization)

    def _set_status(self, meeting_authorization):
        meeting = meeting_dao.get(meeting_authorization.meeting_uuid)
        meeting_authorization.status = (
            'pending' if meeting.require_authorization else 'accepted'
        )

    def get(self, meeting_uuid, authorization_uuid, **kwargs):
        return self.dao.get(meeting_uuid, authorization_uuid, **kwargs)

    def accept(self, meeting_authorization):
        meeting_authorization.status = 'accepted'
        model = self.dao.edit(meeting_authorization)
        self.notifier.edited(meeting_authorization)
        return model

    def reject(self, meeting_authorization):
        meeting_authorization.status = 'rejected'
        model = self.dao.edit(meeting_authorization)
        self.notifier.edited(meeting_authorization)
        return model


def build_service(notifier):
    return MeetingAuthorizationService(dao, build_validator(), notifier)
