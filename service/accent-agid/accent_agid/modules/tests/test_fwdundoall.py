# Copyright 2023 Accent Communications

from __future__ import annotations

import unittest
from unittest.mock import Mock

from accent_agid.modules.fwdundoall import fwdundoall


class TestFwdUndoAll(unittest.TestCase):
    def test_that_fwdundoall_call_confd(self):
        self._client = Mock().return_value
        user_id = 2
        agi = Mock()
        agi.get_variable.return_value = user_id
        agi.config = {'confd': {'client': self._client}}

        fwdundoall(agi, Mock(), [])

        disabled = {'enabled': False}
        expected_body = {
            'busy': disabled,
            'noanswer': disabled,
            'unconditional': disabled,
        }

        self._client.users(user_id).update_forwards.assert_called_once_with(
            expected_body
        )
