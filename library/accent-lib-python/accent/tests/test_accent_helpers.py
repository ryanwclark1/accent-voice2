# Copyright 2023 Accent Communications

import unittest

from accent import accent_helpers


class TestAccentHelpers(unittest.TestCase):
    PREFIX = '_*735.'

    def test_fkey_extension_unc_fwd_with_destination(self):
        arguments = ('123', '_*21.', '1002')

        result = accent_helpers.fkey_extension(self.PREFIX, arguments)

        self.assertEqual(result, '*735123***221*1002')

    def test_fkey_extension_unc_fwd_without_destination(self):
        arguments = ('123', '_*21.', '')

        result = accent_helpers.fkey_extension(self.PREFIX, arguments)

        self.assertEqual(result, '*735123***221')

    def test_fkey_extension_dnd(self):
        arguments = ('123', '*25', '')

        result = accent_helpers.fkey_extension(self.PREFIX, arguments)

        self.assertEqual(result, '*735123***225')


class TestPositionOfAsteriskPatternChar(unittest.TestCase):
    def test_position_of_asterisk_pattern_char(self):
        samples = [
            ('_418[1-5]XZ123', 4),
            ('418-123-5599', None),
            ('_NXXXXXXXXXX', 1),
            ('NXXXXXXXXXX', 0),
            ('_1XXXXXXXXXX', 2),
        ]

        for pattern, expected in samples:
            result = accent_helpers.position_of_asterisk_pattern_char(pattern)
            self.assertEqual(result, expected)
