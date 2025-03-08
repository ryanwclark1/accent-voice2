# Copyright 2023 Accent Communications

from __future__ import annotations

import re

from accent_agid import agid
from accent_agid.dialplan_variables import CALL_OPTIONS

B_REGEX = re.compile(r'b\(([\-_0-9A-Za-z]+)\^?.*?\)')


def ignore_b_option(agi, cursor, args):
    """
    handler to detect and warn about usage of b option
    """
    call_options = agi.get_variable(CALL_OPTIONS)
    if not call_options:
        return

    match = B_REGEX.search(call_options)
    if not match:
        return

    to_remove = match.group(0)
    to_stack = match.group(1)

    agi.verbose(
        f'WARNING: deprecated usage of dialplan b option detected with subroutine: {to_stack}'
    )
    agi.verbose(
        'Option will be ignored. Accent pre-dial handlers should be used instead.'
    )

    pruned_call_options = call_options.replace(to_remove, '')
    agi.set_variable(CALL_OPTIONS, pruned_call_options)


agid.register(ignore_b_option)
