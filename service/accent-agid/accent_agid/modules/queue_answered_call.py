# Copyright 2023 Accent Communications

from __future__ import annotations

from psycopg2.extras import DictCursor

from accent_agid import agid
from accent_agid.handlers import queue


def queue_answered_call(agi: agid.FastAGI, cursor: DictCursor, args: list[str]) -> None:
    handler = queue.AnswerHandler(agi, cursor, args)
    handler.execute()


agid.register(queue_answered_call)
