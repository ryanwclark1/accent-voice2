# Copyright 2023 Accent Communications

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from accent_agid import agid, objects

if TYPE_CHECKING:
    from psycopg2.extras import DictCursor

    from accent_agid.agid import FastAGI

logger = logging.getLogger(__name__)


def check_schedule(agi: FastAGI, cursor: DictCursor, args: list[str]) -> None:
    path = agi.get_variable('ACCENT_PATH')
    path_id = agi.get_variable('ACCENT_PATH_ID')

    if not path:
        return

    schedule = objects.ScheduleDataMapper.get_from_path(cursor, path, path_id)
    schedule_state = schedule.compute_state_for_now()

    agi.set_variable('ACCENT_SCHEDULE_STATUS', schedule_state.state)
    if schedule_state.state == 'closed':
        schedule_state.action.set_variables_in_agi(agi)

    # erase path for next schedule check
    agi.set_variable('ACCENT_PATH', '')


agid.register(check_schedule)
