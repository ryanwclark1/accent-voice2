# Copyright 2023 Accent Communications

from unittest import TestCase
from unittest.mock import Mock, patch

from hamcrest import assert_that, equal_to

from ..services import CallsService


class TestServices(TestCase):
    def setUp(self):
        self.ari = Mock()
        self.services = CallsService(
            Mock(), Mock(), self.ari, Mock(), Mock(), Mock(), Mock()
        )

        self.example_to_fit: dict = {
            'type': 'ChannelDestroyed',
            'timestamp': '2021-06-15T11:06:46.331-0400',
            'cause': 3,
            'cause_txt': 'No route to destination',
            'channel': {
                'id': '1623769434.135',
                'name': 'PJSIP/HwnelF4k-00000075',
                'state': 'Up',
                'caller': {'name': 'Oxynor', 'number': '9000'},
                'connected': {'name': 'Xelanir', 'number': '9001'},
                'accountcode': '',
                'dialplan': {
                    'context': 'pickup',
                    'exten': 'my_pickup',
                    'priority': 3,
                    'app_name': '',
                    'app_data': '',
                },
                'creationtime': '2021-06-15T11:06' ':45.465-0400',
                'language': 'en_US',
                'channelvars': {
                    'CHANNEL(linkedid)': '1623743605.135',
                    'ACCENT_CALL_RECORD_ACTIVE': '',
                    'ACCENT_DEREFERENCED_USERUUID': '',
                    'ACCENT_ENTRY_CONTEXT': 'default-key-2354-internal',
                    'ACCENT_ENTRY_EXTEN': '9001',
                    'ACCENT_LINE_ID': '2',
                    'ACCENT_SIP_CALL_ID': 'coNsbzfk_Tcq2cffBi9g7Q..',
                    'ACCENT_SWITCHBOARD_QUEUE': '',
                    'ACCENT_SWITCHBOARD_HOLD': '',
                    'ACCENT_TENANT_UUID': '6345gd34-9ac7-4337-818d-d04e606d9f74',
                    'ACCENT_BASE_EXTEN': '9001',
                    'ACCENT_ON_HOLD': '',
                    'ACCENT_USERUUID': '76f7fmfh-a547-4324-a521-e2e04843cfee',
                    'ACCENT_LOCAL_CHAN_MATCH_UUID': '',
                    'ACCENT_CALL_RECORD_SIDE': 'caller',
                    'ACCENT_CHANNEL_DIRECTION': 'to-accent',
                },
            },
            'asterisk_id': '52:54:00:2a:da:g5',
            'application': 'callcontrol',
        }

    @patch(
        'accent_calld.plugins.calls.services.CallsService._get_connected_channel_ids_from_helper'
    )
    def test_given_no_chan_variables_when_make_call_from_stasis_event_then_call_has_none_values(
        self, channel_ids
    ):
        channel_ids.return_value = []
        event = self.example_to_fit
        event['channel']['channelvars'] = {}

        call = self.services.channel_destroyed_event(self.ari, event)

        assert_that(call.user_uuid, equal_to(None))
        assert_that(call.dialed_extension, equal_to(None))

    @patch(
        'accent_calld.plugins.calls.services.CallsService._get_connected_channel_ids_from_helper'
    )
    def test_given_accent_useruuid_when_make_call_from_stasis_event_then_call_has_useruuid(
        self, channel_ids
    ):
        channel_ids.return_value = []
        event = self.example_to_fit
        event['channel']['channelvars'] = {'ACCENT_USERUUID': 'new_useruuid'}

        call = self.services.channel_destroyed_event(self.ari, event)

        assert_that(call.user_uuid, equal_to('new_useruuid'))

    @patch(
        'accent_calld.plugins.calls.services.CallsService._get_connected_channel_ids_from_helper'
    )
    def test_given_accent_dereferenced_useruuid_when_make_call_from_stasis_event_then_override_accent_useruuid(
        self, channel_ids
    ):
        channel_ids.return_value = []
        event = self.example_to_fit
        event['channel']['channelvars'] = {
            'ACCENT_USERUUID': 'my-user-uuid',
            'ACCENT_DEREFERENCED_USERUUID': 'new-user-uuid',
        }

        call = self.services.channel_destroyed_event(self.ari, event)

        assert_that(call.user_uuid, equal_to('new-user-uuid'))

    @patch(
        'accent_calld.plugins.calls.services.CallsService._get_connected_channel_ids_from_helper'
    )
    def test_creation_time_from_channel_creation_to_call_on_hungup(self, channel_ids):
        channel_ids.return_value = []
        event = self.example_to_fit
        creation_time = event['channel']['creationtime']
        call = self.services.channel_destroyed_event(self.ari, event)

        assert_that(call.creation_time, equal_to(creation_time))

    @patch(
        'accent_calld.plugins.calls.services.CallsService._get_connected_channel_ids_from_helper'
    )
    def test_direction_of_call_to_who_is_caller(self, channel_ids):
        channel_ids.return_value = []
        event = self.example_to_fit
        call = self.services.channel_destroyed_event(self.ari, event)

        assert_that(call.is_caller, equal_to(True))

    def test_call_direction(self):
        inbound_channel = 'inbound'
        outbound_channel = 'outbound'
        internal_channel = 'internal'
        unknown_channel = 'unknown'

        direction = self.services._conversation_direction_from_directions

        assert_that(direction([]), equal_to(internal_channel))

        assert_that(direction([internal_channel]), equal_to(internal_channel))
        assert_that(direction([inbound_channel]), equal_to(inbound_channel))
        assert_that(direction([outbound_channel]), equal_to(outbound_channel))

        assert_that(
            direction([inbound_channel, inbound_channel]), equal_to(inbound_channel)
        )
        assert_that(
            direction([inbound_channel, outbound_channel]), equal_to(unknown_channel)
        )
        assert_that(
            direction([inbound_channel, internal_channel]), equal_to(inbound_channel)
        )
        assert_that(
            direction([outbound_channel, inbound_channel]), equal_to(unknown_channel)
        )
        assert_that(
            direction([outbound_channel, outbound_channel]), equal_to(outbound_channel)
        )
        assert_that(
            direction([outbound_channel, internal_channel]), equal_to(outbound_channel)
        )
        assert_that(
            direction([internal_channel, inbound_channel]), equal_to(inbound_channel)
        )
        assert_that(
            direction([internal_channel, outbound_channel]), equal_to(outbound_channel)
        )
        assert_that(
            direction([internal_channel, internal_channel]), equal_to(internal_channel)
        )

        assert_that(
            direction([inbound_channel, inbound_channel, inbound_channel]),
            equal_to(inbound_channel),
        )
        assert_that(
            direction([inbound_channel, outbound_channel, inbound_channel]),
            equal_to(unknown_channel),
        )
        assert_that(
            direction([inbound_channel, internal_channel, internal_channel]),
            equal_to(inbound_channel),
        )
        assert_that(
            direction([outbound_channel, inbound_channel, outbound_channel]),
            equal_to(unknown_channel),
        )
        assert_that(
            direction([outbound_channel, outbound_channel, outbound_channel]),
            equal_to(outbound_channel),
        )
        assert_that(
            direction([outbound_channel, internal_channel, internal_channel]),
            equal_to(outbound_channel),
        )
        assert_that(
            direction([internal_channel, inbound_channel, internal_channel]),
            equal_to(inbound_channel),
        )
        assert_that(
            direction([internal_channel, outbound_channel, internal_channel]),
            equal_to(outbound_channel),
        )
        assert_that(
            direction([internal_channel, internal_channel, internal_channel]),
            equal_to(internal_channel),
        )
