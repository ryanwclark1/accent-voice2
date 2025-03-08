# Copyright 2023 Accent Communications

import re


class DialplanExecutionAnalyzer:
    def analyze(self, dialplan_parse_result, log_parse_result):
        line_analyses = self._do_lines_analyses(dialplan_parse_result, log_parse_result)
        return _Analysis(dialplan_parse_result.filename, line_analyses)

    def _do_lines_analyses(self, dialplan_parse_result, log_parse_result):
        line_analyses = []
        for line in dialplan_parse_result.lines:
            is_executed = self._is_line_executed(line, log_parse_result, dialplan_parse_result)
            line_analysis = _LineAnalysis(line.content, line.is_executable, is_executed)
            line_analyses.append(line_analysis)
        return line_analyses

    def _is_line_executed(self, line, log_parse_result, dialplan_parse_result):
        if not line.is_executable:
            return False
        elif line.extension.startswith('_'):
            pattern = line.extension[1:]
            for extension in log_parse_result.list_executed_extensions(line.context, line.priority):
                if not dialplan_parse_result.has_extension(line.context, extension) and _is_extension_match_pattern(
                    extension, pattern
                ):
                    return log_parse_result.is_executed(line.context, extension, line.priority)
            return False
        else:
            return log_parse_result.is_executed(line.context, line.extension, line.priority)


def _is_extension_match_pattern(extension, pattern):
    regex_pattern = _convert_ast_pattern_to_regex_pattern(pattern)
    if re.match(regex_pattern, extension):
        return True
    else:
        return False


def _convert_ast_pattern_to_regex_pattern(ast_pattern):
    regex_pattern_list = ['^']
    index = 0
    length = len(ast_pattern)
    while index < length:
        cur_char = ast_pattern[index]
        if cur_char == 'X':
            regex_pattern_list.append('[0-9]')
        elif cur_char == 'Z':
            regex_pattern_list.append('[1-9]')
        elif cur_char == 'N':
            regex_pattern_list.append('[2-9]')
        elif cur_char == '[':
            close_index = ast_pattern.find(']', index)
            regex_pattern_list.append(f'[{ast_pattern[index:close_index]}]')
            index += close_index
        elif cur_char == '.':
            regex_pattern_list.append('.+')
            break
        elif cur_char == '!':
            regex_pattern_list.append('.*')
            break
        else:
            regex_pattern_list.append(re.escape(cur_char))
        index += 1
    regex_pattern_list.append('$')
    return ''.join(regex_pattern_list)


class _Analysis:
    def __init__(self, filename, line_analyses):
        self.filename = filename
        self.line_analyses = line_analyses


class _LineAnalysis:
    def __init__(self, content, is_executable, is_executed):
        self.content = content
        self.is_executable = is_executable
        self.is_executed = is_executed
