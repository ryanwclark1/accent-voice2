# Copyright 2023 Accent Communications

from accent_dao.helpers import errors
from accent_dao.resources.meeting_authorization import dao

from accent_confd.helpers.validator import ValidationGroup, Validator


class MeetingAuthorizationMaxQuota(Validator):
    max_quota = 128

    def validate(self, model):
        meeting_uuid = model.meeting_uuid
        existing_authorizations = dao.find_all_by(meeting_uuid)
        if len(existing_authorizations) >= self.max_quota:
            raise errors.quota_exceeded('Meeting Authorization', self.max_quota)


def build_validator():
    return ValidationGroup(create=[MeetingAuthorizationMaxQuota()])
