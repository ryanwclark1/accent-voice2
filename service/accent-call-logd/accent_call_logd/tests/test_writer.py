# Copyright 2023 Accent Communications

from unittest import TestCase
from unittest.mock import Mock

from accent_call_logd.generator import CallLogsCreation
from accent_call_logd.writer import CallLogsWriter


class TestCallLogsWriter(TestCase):
    def setUp(self):
        self.dao = Mock()
        self.writer = CallLogsWriter(self.dao)

    def tearDown(self):
        pass

    def test_write(self):
        call_logs_creation = CallLogsCreation(
            new_call_logs=[Mock(recordings=[]), Mock(recordings=[])],
            call_logs_to_delete=None,
        )

        self.writer.write(call_logs_creation)

        self.dao.call_log.create_from_list.assert_called_once_with(
            call_logs_creation.new_call_logs
        )
        self.dao.call_log.delete_from_list.assert_called_once_with(
            call_logs_creation.call_logs_to_delete
        )
