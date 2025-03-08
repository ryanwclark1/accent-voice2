# Copyright 2023 Accent Communications

from __future__ import annotations

from unittest import TestCase
from unittest.mock import Mock, call, patch

from ..call_recording import record_caller


class TestRecordCaller(TestCase):
    def setUp(self):
        self.agi = Mock()
        self.agi.get_variable = Mock()
        self.cursor = Mock()

    @patch('accent_agid.modules.call_recording._start_mix_monitor')
    def test_record_caller_does_not_start_recording_when_already_recording(
        self, start_mix_monitor
    ):
        self.agi.get_variable.return_value = '1'

        record_caller(self.agi, self.cursor, [])

        start_mix_monitor.assert_not_called()

    @patch('accent_agid.modules.call_recording._start_mix_monitor')
    def test_record_caller_does_not_start_recording_when_no_user_id_or_uuid(
        self, start_mix_monitor
    ):
        agi_variables = {
            'ACCENT_CALL_RECORD_ACTIVE': '',
            'ACCENT_USERID': '',
            'ACCENT_USERUUID': '',
        }
        self.agi.get_variable.side_effect = agi_variables.get

        record_caller(self.agi, self.cursor, [])

        calls = [
            call('ACCENT_CALL_RECORD_ACTIVE'),
            call('ACCENT_USERUUID'),
            call('ACCENT_USERID'),
        ]
        self.agi.get_variable.assert_has_calls(calls)

        start_mix_monitor.assert_not_called()

    @patch('accent_agid.modules.call_recording._start_mix_monitor')
    @patch('accent_agid.objects.User')
    def test_record_caller_does_not_start_recording_fallback_to_user_id_when_no_uuid(
        self, user, start_mix_monitor
    ):
        agi_variables = {
            'ACCENT_CALL_RECORD_ACTIVE': '',
            'ACCENT_USERID': '1',
            'ACCENT_USERUUID': '',
        }
        self.agi.get_variable.side_effect = agi_variables.get

        record_caller(self.agi, self.cursor, [])

        calls = [call('ACCENT_CALL_RECORD_ACTIVE'), call('ACCENT_USERUUID')]
        self.agi.get_variable.assert_has_calls(calls)

        start_mix_monitor.assert_called_once()

    @patch('accent_agid.modules.call_recording._start_mix_monitor')
    @patch('accent_agid.objects.User')
    def test_record_caller_does_not_record_when_not_an_outcall(
        self, user, start_mix_monitor
    ):
        agi_variables = {
            'ACCENT_CALL_RECORD_ACTIVE': '',
            'ACCENT_USERUUID': 'the-users-uuid',
            'ACCENT_OUTCALLID': '',
        }
        self.agi.get_variable.side_effect = agi_variables.get
        user.return_value = Mock(
            call_record_outgoing_internal_enabled=False,
            call_record_outgoing_external_enabled=False,
        )

        record_caller(self.agi, self.cursor, [])

        calls = [
            call('ACCENT_CALL_RECORD_ACTIVE'),
            call('ACCENT_USERUUID'),
            call('ACCENT_OUTCALLID'),
        ]
        self.agi.get_variable.assert_has_calls(calls)

        start_mix_monitor.assert_not_called()

    @patch('accent_agid.modules.call_recording._start_mix_monitor')
    @patch('accent_agid.objects.User')
    def test_record_caller_does_not_record_when_an_outcall_but_disabled(
        self, user, start_mix_monitor
    ):
        agi_variables = {
            'ACCENT_CALL_RECORD_ACTIVE': '',
            'ACCENT_USERUUID': 'the-users-uuid',
            'ACCENT_OUTCALLID': '1',
        }
        self.agi.get_variable.side_effect = agi_variables.get
        user.return_value = Mock(
            call_record_outgoing_internal_enabled=False,
            call_record_outgoing_external_enabled=False,
        )

        record_caller(self.agi, self.cursor, [])

        calls = [
            call('ACCENT_CALL_RECORD_ACTIVE'),
            call('ACCENT_USERUUID'),
            call('ACCENT_OUTCALLID'),
        ]
        self.agi.get_variable.assert_has_calls(calls)

        start_mix_monitor.assert_not_called()

    @patch('accent_agid.modules.call_recording._start_mix_monitor')
    @patch('accent_agid.objects.User')
    def test_record_caller_records_when_an_outcall_and_enabled(
        self, user, start_mix_monitor
    ):
        agi_variables = {
            'ACCENT_CALL_RECORD_ACTIVE': '',
            'ACCENT_USERUUID': 'the-users-uuid',
            'ACCENT_OUTCALLID': '1',
        }
        self.agi.get_variable.side_effect = agi_variables.get
        user.return_value = Mock(
            call_record_outgoing_internal_enabled=False,
            call_record_outgoing_external_enabled=True,
        )

        record_caller(self.agi, self.cursor, [])

        calls = [
            call('ACCENT_CALL_RECORD_ACTIVE'),
            call('ACCENT_USERUUID'),
            call('ACCENT_OUTCALLID'),
        ]
        self.agi.get_variable.assert_has_calls(calls)

        start_mix_monitor.assert_called_once()

    @patch('accent_agid.modules.call_recording._start_mix_monitor')
    @patch('accent_agid.objects.User')
    def test_record_caller_does_not_record_when_an_outcall_but_internal_enabled(
        self, user, start_mix_monitor
    ):
        agi_variables = {
            'ACCENT_CALL_RECORD_ACTIVE': '',
            'ACCENT_USERUUID': 'the-users-uuid',
            'ACCENT_OUTCALLID': '1',
        }
        self.agi.get_variable.side_effect = agi_variables.get
        user.return_value = Mock(
            call_record_outgoing_internal_enabled=True,
            call_record_outgoing_external_enabled=False,
        )

        record_caller(self.agi, self.cursor, [])

        calls = [
            call('ACCENT_CALL_RECORD_ACTIVE'),
            call('ACCENT_USERUUID'),
            call('ACCENT_OUTCALLID'),
        ]
        self.agi.get_variable.assert_has_calls(calls)

        start_mix_monitor.assert_not_called()

    @patch('accent_agid.modules.call_recording._start_mix_monitor')
    @patch('accent_agid.objects.User')
    def test_record_caller_records_when_not_an_outcall_and_internal_enabled(
        self, user, start_mix_monitor
    ):
        agi_variables = {
            'ACCENT_CALL_RECORD_ACTIVE': '',
            'ACCENT_USERUUID': 'the-users-uuid',
            'ACCENT_OUTCALLID': '',
        }
        self.agi.get_variable.side_effect = agi_variables.get
        user.return_value = Mock(
            call_record_outgoing_internal_enabled=True,
            call_record_outgoing_external_enabled=False,
        )

        record_caller(self.agi, self.cursor, [])

        calls = [
            call('ACCENT_CALL_RECORD_ACTIVE'),
            call('ACCENT_USERUUID'),
            call('ACCENT_OUTCALLID'),
        ]
        self.agi.get_variable.assert_has_calls(calls)

        start_mix_monitor.assert_called_once()

    @patch('accent_agid.modules.call_recording._start_mix_monitor')
    @patch('accent_agid.objects.User')
    def test_record_caller_records_when_an_outcall_and_all_enabled(
        self, user, start_mix_monitor
    ):
        agi_variables = {
            'ACCENT_CALL_RECORD_ACTIVE': '',
            'ACCENT_USERUUID': 'the-users-uuid',
            'ACCENT_OUTCALLID': '1',
        }
        self.agi.get_variable.side_effect = agi_variables.get
        user.return_value = Mock(
            call_record_outgoing_internal_enabled=True,
            call_record_outgoing_external_enabled=True,
        )

        record_caller(self.agi, self.cursor, [])

        calls = [
            call('ACCENT_CALL_RECORD_ACTIVE'),
            call('ACCENT_USERUUID'),
            call('ACCENT_OUTCALLID'),
        ]
        self.agi.get_variable.assert_has_calls(calls)

        start_mix_monitor.assert_called_once()

    @patch('accent_agid.modules.call_recording._start_mix_monitor')
    @patch('accent_agid.objects.User')
    def test_record_caller_records_when_not_an_outcall_and_all_enabled(
        self, user, start_mix_monitor
    ):
        agi_variables = {
            'ACCENT_CALL_RECORD_ACTIVE': '',
            'ACCENT_USERUUID': 'the-users-uuid',
            'ACCENT_OUTCALLID': '',
        }
        self.agi.get_variable.side_effect = agi_variables.get
        user.return_value = Mock(
            call_record_outgoing_internal_enabled=True,
            call_record_outgoing_external_enabled=True,
        )

        record_caller(self.agi, self.cursor, [])

        calls = [
            call('ACCENT_CALL_RECORD_ACTIVE'),
            call('ACCENT_USERUUID'),
            call('ACCENT_OUTCALLID'),
        ]
        self.agi.get_variable.assert_has_calls(calls)

        start_mix_monitor.assert_called_once()
