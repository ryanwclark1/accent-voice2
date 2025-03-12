# Copyright 2023 Accent Communications

import unittest

from hamcrest import (
    assert_that,
    equal_to,
)
from accent_dao.alchemy.feature_extension import FeatureExtension


class TestIsPattern(unittest.TestCase):

    def test_is_not_pattern(self):
        extension = FeatureExtension(exten='1000')
        assert_that(extension.is_pattern(), equal_to(False))

    def test_is_pattern(self):
        extension = FeatureExtension(exten='_XXXX')
        assert_that(extension.is_pattern(), equal_to(True))
