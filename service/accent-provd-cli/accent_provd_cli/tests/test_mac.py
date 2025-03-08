# Copyright 2023 Accent Communications

import unittest

from accent_provd_cli.mac import norm_mac


class TestNormMac(unittest.TestCase):
    def test_norm_mac(self):
        expected = '00:11:22:aa:bb:cc'
        macs = [
            '001122AABBCC',
            '00-11-22-aa-Bb-cc',
        ]

        for mac in macs:
            self.assertEqual(norm_mac(mac), expected)
