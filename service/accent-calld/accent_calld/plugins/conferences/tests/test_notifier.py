# Copyright 2023 Accent Communications

from unittest import TestCase

from hamcrest import assert_that, contains_exactly, empty

from ..notifier import Participants


class TestNotifierParticipantsValidUserUUIDs(TestCase):
    def test_no_participants(self):
        participants = Participants()

        result = participants.valid_user_uuids()

        assert_that(list(result), empty())

    def test_two_participants(self):
        participants = Participants(
            {'user_uuid': 'uuid1'},
            {'user_uuid': 'uuid2'},
        )

        result = participants.valid_user_uuids()

        assert_that(result, contains_exactly('uuid1', 'uuid2'))

    def test_same_participant(self):
        participants = Participants(
            {'user_uuid': 'uuid1'},
            {'user_uuid': 'uuid1'},
        )

        result = participants.valid_user_uuids()

        assert_that(result, contains_exactly('uuid1'))

    def test_participant_without_user_uuid(self):
        participants = Participants(
            {'user_uuid': 'uuid1'},
            {'user_uuid': None},
        )

        result = participants.valid_user_uuids()

        assert_that(result, contains_exactly('uuid1'))
