# Copyright 2023 Accent Communications

import signal
from unittest import TestCase
from unittest.mock import Mock

from ..controller import _signal_handler


class TestController(TestCase):
    def test_sigterm_handler(self) -> None:
        mock_controller = Mock()
        _signal_handler(mock_controller, signal.SIGTERM, Mock())
        mock_controller.stop.assert_called_once_with(reason="SIGTERM")
