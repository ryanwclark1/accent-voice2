# Copyright 2023 Accent Communications

from psycopg2.extras import DictCursor

from accent_agid import agid
from accent_agid.agid import FastAGI
from accent_agid.handlers.outgoing_callerid_formatter import CallerIDFormatter


def format_and_set_outgoing_caller_id(
    agi: FastAGI, cursor: DictCursor, args: list[str]
) -> None:
    handler = CallerIDFormatter(agi, cursor, args)
    handler.execute()


agid.register(format_and_set_outgoing_caller_id)
