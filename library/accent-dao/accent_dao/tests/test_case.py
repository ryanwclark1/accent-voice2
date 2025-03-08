# Copyright 2023 Accent Communications

import unittest


class TestCase(unittest.TestCase):

    def assertNotCalled(self, callee):
        self.assertEqual(
            callee.call_count,
            0,
            f"{callee} was called {callee.call_count:d} times"
        )
