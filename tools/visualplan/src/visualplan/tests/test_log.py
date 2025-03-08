# Copyright 2023 Accent Communications

import unittest
from io import StringIO
from visualplan.log import LogParser


class TestLogParser(unittest.TestCase):
    def _parse_content(self, content):
        fobj = StringIO(content)
        parser = LogParser()
        return parser.parse(fobj)

    def test_parsed_line_is_marked_as_executed(self):
        content = '[Apr 19 16:12:44]     -- Executing [*971111@default:2] Set\n'

        parse_result = self._parse_content(content)

        self.assertTrue(parse_result.is_executed('default', '*971111', 2))

    def test_unparsed_line_is_marked_as_unexecuted(self):
        content = ''

        parse_result = self._parse_content(content)

        self.assertFalse(parse_result.is_executed('default', 's', 1))

    def test_parser_doesnt_choke_on_invalid_line(self):
        content = """\
[Apr 19 08:15:56]     -- AGI Script Executing Application: (Answer) Options: ()
[Apr 19 16:12:44]     -- Executing foobar
[Apr 19 16:12:44]     -- Executing [*971111@default:2] Set
"""
        parse_result = self._parse_content(content)

        self.assertTrue(parse_result.is_executed('default', '*971111', 2))

    def test_list_executed_extensions(self):
        content = """\
[Apr 19 16:12:44]     -- Executing [s@default:1] Set
"""

        parse_result = self._parse_content(content)

        self.assertEqual(['s'], parse_result.list_executed_extensions('default', 1))
        self.assertEqual([], parse_result.list_executed_extensions('default', 2))
        self.assertEqual([], parse_result.list_executed_extensions('foo', 1))
