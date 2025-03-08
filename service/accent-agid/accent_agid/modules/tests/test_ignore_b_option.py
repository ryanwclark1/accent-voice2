# Copyright 2023 Accent Communications

from __future__ import annotations

import unittest
from unittest.mock import Mock, call

from hamcrest import assert_that, contains_inanyorder

from accent_agid.fastagi import FastAGI

from ..ignore_b_option import ignore_b_option


class TestIgnoreBOption(unittest.TestCase):
    def setUp(self):
        self.agi = Mock(FastAGI)

    def test_no_call_options(self):
        self.agi.get_variable.return_value = ''

        ignore_b_option(self.agi, Mock(), Mock())

        self.agi.set_variable.assert_not_called()

    def test_no_b_option(self):
        variables = {'ACCENT_CALLOPTIONS': 'XB(foobar^s^1)'}
        self.agi.get_variable.side_effect = variables.get

        ignore_b_option(self.agi, Mock(), Mock())

        self.agi.set_variable.assert_not_called()

    def test_with_b_option_no_handlers(self):
        variables = {
            'ACCENT_CALLOPTIONS': 'Xb(foobaz^s^1)B(foobar^s^1)',
        }
        self.agi.get_variable.side_effect = variables.get

        ignore_b_option(self.agi, Mock(), Mock())

        assert_that(
            self.agi.set_variable.call_args_list,
            contains_inanyorder(
                call('ACCENT_CALLOPTIONS', 'XB(foobar^s^1)'),
            ),
        )
