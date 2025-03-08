# Copyright 2023 Accent Communications

from __future__ import annotations

from typing import TYPE_CHECKING

from accent_agid import agid, objects

if TYPE_CHECKING:
    from psycopg2.extras import DictCursor

    from accent_agid.agid import FastAGI


def check_diversion(agi: FastAGI, cursor: DictCursor, args: list[str]) -> None:
    queue_id = agi.get_variable('ACCENT_DSTID')
    try:
        queue = objects.Queue(agi, cursor, int(queue_id))
    except (ValueError, LookupError) as e:
        agi.dp_break(str(e))

    waiting_calls = int(agi.get_variable(f'QUEUE_WAITING_COUNT({queue.name})'))
    if _is_hold_time_overrun(agi, queue, waiting_calls):
        _set_diversion(agi, 'DIVERT_HOLDTIME', 'QWAITTIME')
    elif _is_agent_ratio_overrun(agi, queue, waiting_calls):
        _set_diversion(agi, 'DIVERT_CA_RATIO', 'QWAITRATIO')
    else:
        _set_diversion(agi, '', '')


def _is_hold_time_overrun(agi, queue, waiting_calls):
    if queue.waittime is None or waiting_calls == 0:
        return False

    holdtime = int(agi.get_variable('QUEUEHOLDTIME'))
    return holdtime > queue.waittime


def _is_agent_ratio_overrun(agi, queue, waiting_calls):
    if queue.waitratio is None or waiting_calls == 0:
        return False

    agents = int(agi.get_variable(f'QUEUE_MEMBER({queue.name},logged)'))
    if agents == 0:
        return True

    return (waiting_calls + 1.0) / agents > queue.waitratio


def _set_diversion(agi, event, dialaction):
    agi.set_variable('ACCENT_DIVERT_EVENT', event)
    agi.set_variable('ACCENT_FWD_TYPE', 'QUEUE_' + dialaction)


agid.register(check_diversion)
