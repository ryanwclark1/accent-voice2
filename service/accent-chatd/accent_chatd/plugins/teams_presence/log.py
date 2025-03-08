# Copyright 2023 Accent Communications

import logging


class _TeamsPrefixLogAdapter(logging.LoggerAdapter):
    def process(self, msg, kwargs):
        return f'[Microsoft Teams Presence] {msg}', kwargs


def make_logger(name):
    return _TeamsPrefixLogAdapter(logging.getLogger(name), {})
