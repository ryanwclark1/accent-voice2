# Copyright 2023 Accent Communications

from __future__ import annotations

from typing import TYPE_CHECKING

from accent_agid import agid

if TYPE_CHECKING:
    from psycopg2.extras import DictCursor

    from accent_agid.agid import FastAGI


def callerid_extend(agi: FastAGI, cursor: DictCursor, args: list[str]) -> None:
    if 'agi_callington' in agi.env:
        agi.set_variable('ACCENT_SRCTON', agi.env['agi_callington'])


agid.register(callerid_extend)
