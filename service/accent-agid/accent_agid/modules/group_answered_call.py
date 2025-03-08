# Copyright 2023 Accent Communications

from __future__ import annotations

from psycopg2.extras import DictCursor

from accent_agid import agid
from accent_agid.handlers import group


def group_answered_call(agi: agid.FastAGI, cursor: DictCursor, args: list[str]) -> None:
    handler = group.AnswerHandler(agi, cursor, args)
    handler.execute()


agid.register(group_answered_call)
