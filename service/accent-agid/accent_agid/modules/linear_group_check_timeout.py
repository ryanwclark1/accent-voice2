# Copyright 2023 Accent Communications

from __future__ import annotations

import logging
import time
from typing import TYPE_CHECKING

from accent_agid import agid

if TYPE_CHECKING:
    from psycopg2.extras import DictCursor

    from accent_agid.agid import FastAGI


logger = logging.getLogger(__name__)


def linear_group_check_timeout(
    agi: FastAGI, cursor: DictCursor, args: list[str]
) -> None:
    group_id = agi.get_variable('ACCENT_DSTID')

    if not (_group_timeout := agi.get_variable('ACCENT_GROUPTIMEOUT')):
        logger.info('ACCENT_GROUPTIMEOUT not set for group %s', group_id)
        group_timeout = 0
    else:
        group_timeout = int(_group_timeout)

    current_time = time.time()

    if not (_start_time := agi.get_variable('ACCENT_GROUP_START_TIME')):
        start_time = current_time
        agi.set_variable('ACCENT_GROUP_START_TIME', str(start_time))
    else:
        start_time = float(_start_time)

    if (current_time - start_time) >= group_timeout:
        agi.set_variable('ACCENT_GROUP_TIMEOUT_EXPIRED', '1')
        return

    if _user_timeout := agi.get_variable('ACCENT_GROUP_USER_TIMEOUT'):
        user_timeout = int(_user_timeout)
    else:
        user_timeout = group_timeout

    remaining_time = group_timeout - (current_time - start_time)
    next_dial_timeout = int(min(user_timeout, remaining_time))

    agi.set_variable('ACCENT_DIAL_TIMEOUT', str(next_dial_timeout))


agid.register(linear_group_check_timeout)
