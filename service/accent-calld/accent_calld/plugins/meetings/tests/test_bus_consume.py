# Copyright 2023 Accent Communications

from unittest import TestCase
from unittest.mock import patch
from uuid import uuid4

from hamcrest import assert_that, is_, none

from ..bus_consume import MeetingsBusEventHandler


class TestBusConsume(TestCase):
    @patch('accent_calld.plugins.meetings.bus_consume.Meeting')
    def test_that_paging_events_are_ignored(self, MeetingMock):
        MeetingMock.from_uuid.side_effect = AssertionError('Should not get called')
        handler = MeetingsBusEventHandler(None, None, None)

        event = {'Conference': '13246546542897343.124566541'}
        result = handler._notify_participant_joined(event)

        assert_that(result, is_(none()))

        result = handler._notify_participant_left(event)

        assert_that(result, is_(none()))

    @patch('accent_calld.plugins.meetings.bus_consume.Meeting')
    def test_that_conference_events_are_ignored(self, MeetingMock):
        MeetingMock.from_uuid.side_effect = AssertionError('Should not get called')
        handler = MeetingsBusEventHandler(None, None, None)

        event = {'Conference': f'accent-conference-{uuid4()}'}
        result = handler._notify_participant_joined(event)

        assert_that(result, is_(none()))

        result = handler._notify_participant_left(event)

        assert_that(result, is_(none()))
