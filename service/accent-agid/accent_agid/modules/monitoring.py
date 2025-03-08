# Copyright 2023 Accent Communications

from __future__ import annotations

from psycopg2.extras import DictCursor

from accent_agid import agid


def monitoring(agi: agid.FastAGI, cursor: DictCursor, args: list[str]) -> None:
    agi.send_command("Status: OK")


agid.register(monitoring)
