# Copyright 2023 Accent Communications

import unittest

from accent_provd_cli import helpers


class TestHelpers(unittest.TestCase):
    def test_are_plugins_installed_missing(self):
        installed_plugins = set()

        res = helpers._are_plugins_installed(['foo'], installed_plugins)

        self.assertFalse(res)

    def test_are_plugins_installed(self):
        installed_plugins = {'foo'}

        res = helpers._are_plugins_installed(['foo'], installed_plugins)

        self.assertTrue(res)
