# Copyright 2023 Accent Communications

from unittest import TestCase
from unittest.mock import Mock
from unittest.mock import sentinel as s

from ..bus_consume import ARINotFound, EventHandler
from ..services import DialMobileService


class TestEventHandler(TestCase):
    def setUp(self):
        self.service = Mock(DialMobileService)
        self.event_handler = EventHandler(self.service)

    def test_push_mobile_user_event(self):
        event = {
            'Event': 'UserEvent',
            'Privilege': 'user,all',
            'Channel': 'PJSIP/zcua59c9-00000015',
            'ChannelState': '4',
            'ChannelStateDesc': 'Ring',
            'CallerIDNum': '1005',
            'CallerIDName': 'Anastasia Romanov',
            'ConnectedLineNum': '1101',
            'ConnectedLineName': 'Alice WebRTC',
            'Language': 'fr_FR',
            'AccountCode': '',
            'Context': 'user',
            'Exten': 's',
            'Priority': '42',
            'Uniqueid': '1647612626.39',
            'Linkedid': '1647612626.39',
            'UserEvent': 'Pushmobile',
            'ACCENT_DST_UUID': '89554a93-3761-43d2-9b14-a9b094bcbf1d',
            'ACCENT_VIDEO_ENABLED': '0',
            'ACCENT_RING_TIME': '42',
            'ACCENT_TIMESTAMP': '2024-08-06T23:59:59+00:00',
            'ChanVariable': {
                'CHANNEL(linkedid)': '1647612626.39',
                'CHANNEL(videonativeformat)': '(nothing)',
                'ACCENT_ANSWER_TIME': '',
                'ACCENT_CALL_RECORD_ACTIVE': '',
                'ACCENT_CALL_RECORD_SIDE': 'caller',
                'ACCENT_CHANNEL_DIRECTION': 'to-accent',
                'ACCENT_DEREFERENCED_USERUUID': '',
                'ACCENT_ENTRY_CONTEXT': 'inside',
                'ACCENT_ENTRY_EXTEN': '1101',
                'ACCENT_LINE_ID': '83',
                'ACCENT_LOCAL_CHAN_MATCH_UUID': '',
                'ACCENT_SIP_CALL_ID': 'de9eb39fb7585796',
                'ACCENT_SWITCHBOARD_QUEUE': '',
                'ACCENT_SWITCHBOARD_HOLD': '',
                'ACCENT_TENANT_UUID': '2c34c282-433e-4bb8-8d56-fec14ff7e1e9',
                'ACCENT_BASE_EXTEN': '1101',
                'ACCENT_ON_HOLD': '',
                'ACCENT_USERUUID': 'def42192-837a-41e0-aa4e-86390e46eb17',
            },
        }

        self.event_handler._on_user_event(event)

        self.service.send_push_notification.assert_called_with(
            '2c34c282-433e-4bb8-8d56-fec14ff7e1e9',
            '89554a93-3761-43d2-9b14-a9b094bcbf1d',
            '1647612626.39',
            'de9eb39fb7585796',
            'Anastasia Romanov',
            '1005',
            False,
            '42',
            '1647612626.39',
            '2024-08-06T23:59:59+00:00',
        )

    def test_cancel_push_on_dial_end(self):
        event = {
            'CallerIDName': 'Anastasia Romanov',
            'CallerIDNum': '1005',
            'ChanVariable': {
                'CHANNEL(linkedid)': '1647871892.53',
                'CHANNEL(videonativeformat)': '(nothing)',
                'ACCENT_ANSWER_TIME': '',
                'ACCENT_CALL_RECORD_ACTIVE': '',
                'ACCENT_CALL_RECORD_SIDE': 'caller',
                'ACCENT_CHANNEL_DIRECTION': 'to-accent',
                'ACCENT_DEREFERENCED_USERUUID': '',
                'ACCENT_ENTRY_CONTEXT': 'inside',
                'ACCENT_ENTRY_EXTEN': '1101',
                'ACCENT_LINE_ID': '83',
                'ACCENT_LOCAL_CHAN_MATCH_UUID': '',
                'ACCENT_SIP_CALL_ID': 'cf31ee68cec261d9',
                'ACCENT_SWITCHBOARD_HOLD': '',
                'ACCENT_SWITCHBOARD_QUEUE': '',
                'ACCENT_TENANT_UUID': '2c34c282-433e-4bb8-8d56-fec14ff7e1e9',
                'ACCENT_BASE_EXTEN': '1101',
                'ACCENT_ON_HOLD': '',
                'ACCENT_USERUUID': 'def42192-837a-41e0-aa4e-86390e46eb17',
            },
            'Channel': 'PJSIP/zcua59c9-0000001b',
            'ChannelState': '4',
            'ChannelStateDesc': 'Ring',
            'ConnectedLineName': 'Alice WebRTC',
            'ConnectedLineNum': '1101',
            'Context': 'user',
            'DestAccountCode': '',
            'DestCallerIDName': 'Alice WebRTC',
            'DestCallerIDNum': 's',
            'DestChanVariable': 'ACCENT_USERUUID=',
            'DestChannel': 'Local/ycetqvtr@accent_wait_for_registration-0000000d;1',
            'DestChannelState': '5',
            'DestChannelStateDesc': 'Ringing',
            'DestConnectedLineName': 'Anastasia Romanov',
            'DestConnectedLineNum': '1005',
            'DestContext': 'accent_wait_for_registration',
            'DestExten': 's',
            'DestLanguage': 'en',
            'DestLinkedid': '1647871892.53',
            'DestPriority': '1',
            'DestUniqueid': '1647871892.54',
            'DialStatus': 'NOANSWER',
            'Event': 'DialEnd',
            'Exten': 's',
            'Language': 'fr_FR',
            'Linkedid': '1647871892.53',
            'Priority': '44',
            'Privilege': 'call,all',
            'Uniqueid': '1647871892.53',
        }

        self.event_handler._on_dial_end(event)

        self.service.cancel_push_mobile.assert_called_with('1647871892.53')

    def test_cancel_push_on_dial_end_answered(self):
        event = {
            'CallerIDName': 'Anastasia Romanov',
            'CallerIDNum': '1005',
            'ChanVariable': {
                'CHANNEL(linkedid)': '1647871892.53',
                'CHANNEL(videonativeformat)': '(nothing)',
                'ACCENT_ANSWER_TIME': '',
                'ACCENT_CALL_RECORD_ACTIVE': '',
                'ACCENT_CALL_RECORD_SIDE': 'caller',
                'ACCENT_CHANNEL_DIRECTION': 'to-accent',
                'ACCENT_DEREFERENCED_USERUUID': '',
                'ACCENT_ENTRY_CONTEXT': 'inside',
                'ACCENT_ENTRY_EXTEN': '1101',
                'ACCENT_LINE_ID': '83',
                'ACCENT_LOCAL_CHAN_MATCH_UUID': '',
                'ACCENT_SIP_CALL_ID': 'cf31ee68cec261d9',
                'ACCENT_SWITCHBOARD_HOLD': '',
                'ACCENT_SWITCHBOARD_QUEUE': '',
                'ACCENT_TENANT_UUID': '2c34c282-433e-4bb8-8d56-fec14ff7e1e9',
                'ACCENT_BASE_EXTEN': '1101',
                'ACCENT_ON_HOLD': '',
                'ACCENT_USERUUID': 'def42192-837a-41e0-aa4e-86390e46eb17',
            },
            'Channel': 'PJSIP/zcua59c9-0000001b',
            'ChannelState': '4',
            'ChannelStateDesc': 'Ring',
            'ConnectedLineName': 'Alice WebRTC',
            'ConnectedLineNum': '1101',
            'Context': 'user',
            'DestAccountCode': '',
            'DestCallerIDName': 'Alice WebRTC',
            'DestCallerIDNum': 's',
            'DestChanVariable': 'ACCENT_USERUUID=',
            'DestChannel': 'Local/ycetqvtr@accent_wait_for_registration-0000000d;1',
            'DestChannelState': '5',
            'DestChannelStateDesc': 'Ringing',
            'DestConnectedLineName': 'Anastasia Romanov',
            'DestConnectedLineNum': '1005',
            'DestContext': 'accent_wait_for_registration',
            'DestExten': 's',
            'DestLanguage': 'en',
            'DestLinkedid': '1647871892.53',
            'DestPriority': '1',
            'DestUniqueid': '1647871892.54',
            'DialStatus': 'ANSWER',  # Only important field for this test
            'Event': 'DialEnd',
            'Exten': 's',
            'Language': 'fr_FR',
            'Linkedid': '1647871892.53',
            'Priority': '44',
            'Privilege': 'call,all',
            'Uniqueid': '1647871892.53',
        }

        self.event_handler._on_dial_end(event)

        self.service.cancel_push_mobile.assert_not_called()

    def test_on_bridge_enter_not_a_dial_mobile_bridge(self):
        event = {
            'Event': 'BridgeEnter',
            'BridgeType': 'unknown',
            'BridgeUniqueid': '<UUID>',
        }

        self.event_handler._on_bridge_enter(event)

        self.service.cancel_push_mobile.assert_not_called()
        self.service.remove_pending_push_mobile.assert_not_called()

    def test_on_bridge_enter_ignore_not_pjsip(self):
        event = {
            'Event': 'BridgeEnter',
            'BridgeType': 'stasis',
            'Channel': 'Local/endpoint@accent-wait-for-mobile-9090832;1',
            'BridgeUniqueid': 'accent-dial-mobile-<UUID>',
        }

        self.event_handler._on_bridge_enter(event)

        self.service.cancel_push_mobile.assert_not_called()
        self.service.remove_pending_push_mobile.assert_not_called()

    def test_on_bridge_enter_not_answered_by_mobile(self):
        self.service.has_a_registered_mobile_and_pending_push.return_value = False

        event = {
            'Event': 'BridgeEnter',
            'BridgeType': 'stasis',
            'BridgeUniqueid': 'accent-dial-mobile-<UUID>',
            'Channel': 'PJSIP/myendpoint-000000213',
            'ChanVariable': {'ACCENT_USERUUID': s.user_uuid},
            'Linkedid': s.linkedid,
            'Uniqueid': s.uniqueid,
        }

        self.event_handler._on_bridge_enter(event)

        self.service.has_a_registered_mobile_and_pending_push.assert_called_once_with(
            s.linkedid,
            s.uniqueid,
            'myendpoint',
            s.user_uuid,
        )

        self.service.cancel_push_mobile.assert_called_once_with(s.linkedid)
        self.service.remove_pending_push_mobile.assert_not_called()

    def test_on_bridge_enter_answered_by_mobile(self):
        self.service.has_a_registered_mobile_and_pending_push.return_value = True

        event = {
            'Event': 'BridgeEnter',
            'BridgeType': 'stasis',
            'BridgeUniqueid': 'accent-dial-mobile-<UUID>',
            'Channel': 'PJSIP/myendpoint-000000213',
            'ChanVariable': {'ACCENT_USERUUID': s.user_uuid},
            'Linkedid': s.linkedid,
            'Uniqueid': s.uniqueid,
        }

        self.event_handler._on_bridge_enter(event)

        self.service.has_a_registered_mobile_and_pending_push.assert_called_once_with(
            s.linkedid,
            s.uniqueid,
            'myendpoint',
            s.user_uuid,
        )

        self.service.cancel_push_mobile.assert_not_called()
        self.service.remove_pending_push_mobile.assert_called_once_with(s.linkedid)

    def test_on_bridge_enter_caller_hung_up(self):
        self.service.has_a_registered_mobile_and_pending_push.side_effect = ARINotFound(
            Mock, Mock
        )

        event = {
            'Event': 'BridgeEnter',
            'BridgeType': 'stasis',
            'BridgeUniqueid': 'accent-dial-mobile-<UUID>',
            'Channel': 'PJSIP/myendpoint-000000213',
            'ChanVariable': {'ACCENT_USERUUID': s.user_uuid},
            'Linkedid': s.linkedid,
            'Uniqueid': s.uniqueid,
        }

        self.event_handler._on_bridge_enter(event)

        self.service.has_a_registered_mobile_and_pending_push.assert_called_once_with(
            s.linkedid,
            s.uniqueid,
            'myendpoint',
            s.user_uuid,
        )

        self.service.cancel_push_mobile.assert_called_once_with(s.linkedid)
        self.service.remove_pending_push_mobile.assert_not_called()
