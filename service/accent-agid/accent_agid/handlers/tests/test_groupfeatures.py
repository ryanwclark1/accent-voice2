# Copyright 2023 Accent Communications

import unittest
from unittest.mock import Mock, call, patch

from accent_agid.handlers.groupfeatures import GroupFeatures


class TestGroupFeatures(unittest.TestCase):
    def setUp(self):
        self._agi = Mock()
        self._cursor = Mock()
        self._args = Mock()
        self.group_features = GroupFeatures(self._agi, self._cursor, self._args)

    @patch('accent_agid.handlers.groupfeatures.GroupFeatures._set_members')
    @patch('accent_agid.handlers.groupfeatures.GroupFeatures._set_options')
    @patch('accent_agid.handlers.groupfeatures.GroupFeatures._set_vars')
    @patch('accent_agid.handlers.groupfeatures.GroupFeatures._set_preprocess_subroutine')
    @patch('accent_agid.handlers.groupfeatures.GroupFeatures._set_timeout')
    @patch('accent_agid.handlers.groupfeatures.GroupFeatures._set_dial_action')
    @patch('accent_agid.handlers.groupfeatures.GroupFeatures._set_schedule')
    @patch('accent_agid.handlers.groupfeatures.GroupFeatures._needs_rewrite_cid')
    @patch('accent_agid.handlers.groupfeatures.GroupFeatures._set_rewrite_cid')
    @patch('accent_agid.handlers.groupfeatures.GroupFeatures._set_call_record_side')
    def test_execute(
        self,
        _set_rewrite_cid,
        _needs_rewrite_cid,
        _set_schedule,
        _set_dial_action,
        _set_timeout,
        _set_preprocess_subroutine,
        _set_vars,
        _set_options,
        _set_members,
        _set_call_record_side,
    ):
        _needs_rewrite_cid.return_value = True

        self.group_features.execute()

        _set_members.assert_called_once_with()
        _set_options.assert_called_once_with()
        _set_vars.assert_called_once_with()
        _set_preprocess_subroutine.assert_called_once_with()
        _set_timeout.assert_called_once_with()
        _set_dial_action.assert_called_once_with()
        _set_schedule.assert_called_once_with()
        _set_rewrite_cid.assert_called_once_with()
        _set_call_record_side.assert_called_once_with()

    def test_referer_myself_needs_rewrite_cid(self):
        self.group_features._id = 3
        self.group_features._referer = "group:3"

        self.assertTrue(self.group_features._needs_rewrite_cid())

    def test_set_schedule(self):
        self.group_features._id = 34
        self._agi.get_variable.return_value = ''

        calls = [call('ACCENT_PATH', 'group'), call('ACCENT_PATH_ID', 34)]

        self.group_features._set_schedule()

        self._agi.set_variable.assert_has_calls(calls)

        self._agi.set_variable.assert_any_call('ACCENT_PATH', 'group')
        self._agi.set_variable.assert_any_call('ACCENT_PATH_ID', 34)
