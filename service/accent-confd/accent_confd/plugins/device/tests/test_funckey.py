# Copyright 2023 Accent Communications

import unittest
from unittest.mock import Mock

from accent_dao.alchemy.func_key_mapping import FuncKeyMapping as FuncKey
from accent_dao.alchemy.linefeatures import LineFeatures as Line
from hamcrest import assert_that, has_entries

from ..funckey import FuncKeyConverter


class FuncKeyTestConverter(FuncKeyConverter):
    def build(self, user, line, position, funckey):
        pass


class TestFuncKeyConverter(unittest.TestCase):
    def setUp(self):
        self.converter = FuncKeyTestConverter()

    def test_no_label_returns_empty_string(self):
        line = Mock(Line, device_slot=1)
        funckey = Mock(FuncKey, label=None, blf=True)

        converted = self.converter.provd_funckey(line, 1, funckey, '1234')
        assert_that(converted, has_entries({1: has_entries(label="")}))

    def test_invalid_chars_removed_from_label(self):
        line = Mock(Line, device_slot=1)
        funckey = Mock(FuncKey, label="\nhe;l\tlo\r", blf=True)

        converted = self.converter.provd_funckey(line, 1, funckey, '1234')
        assert_that(converted, has_entries({1: has_entries(label="hello")}))

    def test_invalid_chars_removed_from_value(self):
        line = Mock(Line, device_slot=1)
        funckey = Mock(FuncKey, blf=True, label=None)

        converted = self.converter.provd_funckey(line, 1, funckey, '\r1\t2;34\n')
        assert_that(converted, has_entries({1: has_entries(value="1234")}))
