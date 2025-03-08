# Copyright 2023 Accent Communications

import unittest

from hamcrest import assert_that, equal_to, is_not

from ..permission import escape


class TestEscape(unittest.TestCase):
    def test_escape(self):
        assert_that(escape("my-id"), equal_to("my-id"))
        assert_that(escape("my.id"), is_not(equal_to("my.id")))
        assert_that(escape("my#id"), is_not(equal_to("my#id")))
        assert_that(escape("my*id"), is_not(equal_to("my*id")))
