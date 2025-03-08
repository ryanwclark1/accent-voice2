# Copyright 2023 Accent Communications

from unittest import TestCase
from unittest.mock import Mock

from hamcrest import assert_that, has_properties, none
from requests.exceptions import HTTPError

from ..participant import find_participant, find_participant_by_uuid


def confd_mock(lines=None):
    lines = lines or []
    confd = Mock()
    confd.lines.list.return_value = {'items': lines}
    users = (
        {
            user['uuid']: dict(user, lines=[line])
            for line in lines
            for user in line['users']
        }
        if lines and lines[0].get('users')
        else {}
    )

    def confd_users_get(uuid):
        if uuid in users:
            return users[uuid]
        else:
            raise HTTPError(response=Mock(status_code=404, request=Mock()))

    confd.users.get.side_effect = confd_users_get
    return confd


class TestFindParticipant(TestCase):
    def test_find_participants_when_channame_is_not_parsable(self):
        confd = confd_mock()
        channame = 'something'

        result = find_participant(confd, channame)

        assert_that(result, none())

    def test_find_participants_when_no_lines(self):
        confd = confd_mock()
        channame = 'sip/something-suffix'

        result = find_participant(confd, channame)

        assert_that(result, none())

    def test_find_participants_when_line_has_no_user(self):
        lines = [{'id': 12, 'users': []}]
        confd = confd_mock(lines)
        channame = 'sip/something-suffix'

        result = find_participant(confd, channame)

        assert_that(result, none())

    def test_find_participants_when_line_has_user(self):
        user = {
            'uuid': 'user_uuid',
            'tenant_uuid': 'tenant_uuid',
            'userfield': 'user_userfield, toto',
        }
        lines = [{'id': 12, 'users': [user], 'extensions': []}]
        confd = confd_mock(lines)
        channame = 'sip/something-suffix'

        result = find_participant(confd, channame)

        assert_that(
            result,
            has_properties(
                uuid='user_uuid',
                tenant_uuid='tenant_uuid',
                line_id=12,
                tags=['user_userfield', 'toto'],
            ),
        )

    def test_find_participant_from_user_uuid(self):
        user = {
            'uuid': 'user_uuid',
            'tenant_uuid': 'tenant_uuid',
            'userfield': 'user_userfield, toto',
        }
        lines = [{'id': 12, 'users': [user], 'extensions': []}]
        user_uuid = user["uuid"]
        confd = confd_mock(lines)

        result = find_participant_by_uuid(confd, user_uuid=user_uuid)

        assert_that(
            result,
            has_properties(
                uuid='user_uuid',
                tenant_uuid='tenant_uuid',
                line_id=12,
                main_extension=None,
                tags=['user_userfield', 'toto'],
            ),
        )

    def test_find_participant_from_user_uuid_when_not_found(self):
        lines = [{'id': 12, 'users': [], 'extensions': []}]
        user_uuid = "phantom-user-uuid"
        confd = confd_mock(lines)

        result = find_participant_by_uuid(confd, user_uuid=user_uuid)

        assert_that(
            result,
            none(),
        )
