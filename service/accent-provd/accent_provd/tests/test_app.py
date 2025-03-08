# Copyright 2023 Accent Communications

from __future__ import annotations

import unittest
from unittest.mock import Mock, sentinel

from hamcrest import assert_that, equal_to, is_

from accent_provd.app import ApplicationConfigureService
from accent_provd.services import InvalidParameterError


class TestAppConfigureService(unittest.TestCase):
    def setUp(self) -> None:
        self.app = Mock()
        self.service = ApplicationConfigureService(Mock(), {}, self.app)

    def test_get_nat(self) -> None:
        self.app.nat = sentinel.nat

        value = self.service.get('NAT')

        assert_that(value, is_(sentinel.nat))

    def test_set_nat_valid_values(self) -> None:
        for value in [0, 1]:
            self.service.set('NAT', str(value))
            assert_that(self.app.nat, equal_to(value))

    def test_set_nat_invalid_values(self) -> None:
        for value in ['-1', '2', 'foobar']:
            self.assertRaises(InvalidParameterError, self.service.set, 'NAT', value)

    def test_set_nat_to_none(self) -> None:
        self.service.set('NAT', None)
        assert_that(self.app.nat, equal_to(0))
