# Copyright 2023 Accent Communications

import re


class LogParser:
    _EXECUTE_REGEX = re.compile(r'Executing \[([^@]+)@([a-zA-Z0-9_\-]+):(\d+)\]')

    def parse(self, fobj):
        result = _LogParseResult()
        for log_line in fobj:
            mo = self._EXECUTE_REGEX.search(log_line)
            if mo:
                extension = mo.group(1)
                context = mo.group(2)
                priority = int(mo.group(3))
                result._add(context, extension, priority)
        return result

    def parse_file(self, filename):
        with open(filename) as fobj:
            return self.parse(fobj)


class _LogParseResult:
    def __init__(self):
        self._contexts = {}

    def _add(self, context, extension, priority):
        self._contexts.setdefault(context, {}).setdefault(extension, set()).add(priority)

    def is_executed(self, context, extension, priority):
        extensions = self._contexts.get(context)
        if extensions:
            priorities = extensions.get(extension)
            if priorities:
                return priority in priorities
        return False

    def list_executed_extensions(self, context, priority):
        return [
            extension for extension, priorities in self._contexts.get(context, {}).items() if priority in priorities
        ]
