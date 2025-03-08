# Copyright 2023 Accent Communications

from unittest import TestCase
from unittest.mock import patch
from uuid import uuid4

from hamcrest import assert_that, is_, none

from ..bus_consume import ConferencesBusEventHandler


class TestBusConsume(TestCase):
    @patch('accent_calld.plugins.conferences.bus_consume.Conference')
    def test_that_paging_events_are_ignored(self, ConferenceMock):
        ConferenceMock.from_id.side_effect = AssertionError('Should not get called')
        handler = ConferencesBusEventHandler(None, None, None)

        event = {'Conference': '13246546542897343.124566541'}
        result = handler._notify_participant_joined(event)

        assert_that(result, is_(none()))

        result = handler._notify_participant_left(event)

        assert_that(result, is_(none()))

    @patch('accent_calld.plugins.conferences.bus_consume.Conference')
    def test_that_meeting_events_are_ignored(self, ConferenceMock):
        ConferenceMock.from_id.side_effect = AssertionError('Should not get called')
        handler = ConferencesBusEventHandler(None, None, None)

        event = {'Conference': f'accent-meeting-{uuid4()}-confbridge'}
        result = handler._notify_participant_joined(event)

        assert_that(result, is_(none()))

        result = handler._notify_participant_left(event)

        assert_that(result, is_(none()))
