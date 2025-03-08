# Copyright 2023 Accent Communications

import unittest
from unittest.mock import Mock

from visualplan.analyzer import DialplanExecutionAnalyzer, _is_extension_match_pattern


class TestDialplanExecutionAnalyzer(unittest.TestCase):
    def test_analysis_has_right_filename(self):
        filename = 'extensions.conf'
        analyzer = DialplanExecutionAnalyzer()

        analysis = analyzer.analyze(self._new_dialplan_parse_result(filename=filename), Mock())

        self.assertEqual(filename, analysis.filename)

    def _new_dialplan_parse_result(self, filename='test', lines=None):
        if lines is None:
            lines = []
        dialplan_parse_result = Mock()
        dialplan_parse_result.filename = filename
        dialplan_parse_result.lines = lines
        return dialplan_parse_result

    def test_analysis_with_one_blank_line(self):
        line = self._new_line('', is_executable=False)

        self._assert_is_not_executable_line(line)

    def _new_line(self, content, **kwargs):
        line = Mock()
        line.content = content
        line.is_executable = False
        line.__dict__.update(kwargs)
        return line

    def _assert_is_not_executable_line(self, line):
        analyzer = DialplanExecutionAnalyzer()

        analysis = analyzer.analyze(self._new_dialplan_parse_result(lines=[line]), Mock())
        line_analysis = analysis.line_analyses[0]

        self.assertEqual(line.content, line_analysis.content)
        self.assertFalse(line_analysis.is_executable)
        self.assertFalse(line_analysis.is_executed)

    def test_analysis_with_one_comment_line(self):
        line = self._new_line('; this is a comment')

        self._assert_is_not_executable_line(line)

    def test_analysis_with_one_context_line(self):
        line = self._new_line('[default]')

        self._assert_is_not_executable_line(line)

    def test_analysis_with_one_executed_line(self):
        line1 = self._new_line('[default]')
        line2 = self._new_line('exten = s,1,NoOp()', extension='s', is_executable=True)

        self._assert_is_executed_line([line1, line2], index=1)

    def test_analysis_with_one_unexecuted_line(self):
        line1 = self._new_line('[default]')
        line2 = self._new_line('exten = s,1,NoOp()', extension='s', is_executable=True)

        self._assert_is_not_executed_line([line1, line2], index=1)

    def _assert_is_executed_line(self, lines, index):
        self._assert_executed_line(lines, index, is_executed=True)

    def _assert_is_not_executed_line(self, lines, index):
        self._assert_executed_line(lines, index, is_executed=False)

    def _assert_executed_line(self, lines, index, is_executed):
        analyzer = DialplanExecutionAnalyzer()

        analysis = analyzer.analyze(
            self._new_dialplan_parse_result(lines=lines), self._new_log_parse_result(is_executed)
        )
        line_analysis = analysis.line_analyses[index]

        self.assertEqual(lines[index].content, line_analysis.content)
        self.assertTrue(line_analysis.is_executable)
        if is_executed:
            self.assertTrue(line_analysis.is_executed)
        else:
            self.assertFalse(line_analysis.is_executed)

    def _new_log_parse_result(self, is_executed):
        log_parser_result = Mock()
        log_parser_result.is_executed.return_value = is_executed
        return log_parser_result

    def test_is_extension_match_pattern(self):
        test_cases = [
            ('0', 'X', True),
            ('9', 'X', True),
            ('*', 'X', False),
            ('a', 'X', False),
            ('55', 'X', False),
            ('0', 'Z', False),
            ('1', 'Z', True),
            ('9', 'Z', True),
            ('*', 'Z', False),
            ('a', 'Z', False),
            ('55', 'Z', False),
            ('0', 'N', False),
            ('1', 'N', False),
            ('2', 'N', True),
            ('9', 'N', True),
            ('*', 'N', False),
            ('a', 'N', False),
            ('55', 'N', False),
            ('1', '[15-7]', True),
            ('2', '[15-7]', False),
            ('5', '[15-7]', True),
            ('6', '[15-7]', True),
            ('7', '[15-7]', True),
            ('8', '[15-7]', False),
            ('*', '[15-7]', False),
            ('a', '[15-7]', False),
            ('55', '[15-7]', False),
            ('0', '.', True),
            ('9', '.', True),
            ('*', '.', True),
            ('a', '.', True),
            ('55', '.', True),
            ('1', 'X.', False),
            ('0', '!', True),
            ('9', '!', True),
            ('*', '!', True),
            ('a', '!', True),
            ('55', '!', True),
            ('1', '1', True),
            ('1', '2', False),
        ]

        for test_case in test_cases:
            extension, pattern, expected_result = test_case
            self.assertEqual(expected_result, _is_extension_match_pattern(extension, pattern), test_case)
