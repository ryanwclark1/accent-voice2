# Copyright 2023 Accent Communications
import signal
from unittest import TestCase
from unittest.mock import Mock

from ..controller import _signal_handler


class TestController(TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_sigterm_handler(self):
        controller_mock = Mock()
        _signal_handler(controller_mock, signal.SIGTERM, Mock())
        controller_mock.stop.assert_called_once_with(reason="SIGTERM")
