# Copyright 2023 Accent Communications

from unittest import TestCase

from hamcrest import assert_that, calling, raises

from ..meeting import AsteriskMeeting, InvalidMeetingConfbridgeName


class TestBusConsume(TestCase):
    def test_confbridge_name(self):
        assert AsteriskMeeting('uuid').confbridge_name == 'accent-meeting-uuid-confbridge'

    def test_from_confbridge_name(self):
        assert_that(
            calling(AsteriskMeeting.from_confbridge_name).with_args(''),
            raises(InvalidMeetingConfbridgeName),
        )
        assert_that(
            calling(AsteriskMeeting.from_confbridge_name).with_args('something'),
            raises(InvalidMeetingConfbridgeName),
        )
        assert_that(
            calling(AsteriskMeeting.from_confbridge_name).with_args(
                'accent-meeting.uuid.confbridge'
            ),
            raises(InvalidMeetingConfbridgeName),
        )
        assert_that(
            calling(AsteriskMeeting.from_confbridge_name).with_args(
                'accent-meeting-uuid.confbridge'
            ),
            raises(InvalidMeetingConfbridgeName),
        )
        assert_that(
            calling(AsteriskMeeting.from_confbridge_name).with_args(
                'accent-meeting.uuid-confbridge'
            ),
            raises(InvalidMeetingConfbridgeName),
        )
        assert_that(
            calling(AsteriskMeeting.from_confbridge_name).with_args(
                'accent-meeting-uuid-confbridge.'
            ),
            raises(InvalidMeetingConfbridgeName),
        )
        assert_that(
            calling(AsteriskMeeting.from_confbridge_name).with_args(
                '.accent-meeting.uuid-confbridge'
            ),
            raises(InvalidMeetingConfbridgeName),
        )
        assert_that(
            calling(AsteriskMeeting.from_confbridge_name).with_args(
                'accent-meeting--confbridge'
            ),
            raises(InvalidMeetingConfbridgeName),
        )
        assert (
            AsteriskMeeting.from_confbridge_name('accent-meeting-uuid-confbridge').uuid
            == 'uuid'
        )
