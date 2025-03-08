# Copyright 2023 Accent Communications

from __future__ import annotations

from typing import TYPE_CHECKING

from accent_agid import dialplan_variables

if TYPE_CHECKING:
    from psycopg2.extras import DictCursor

    from accent_agid.agid import FastAGI


class Handler:
    def __init__(self, agi: FastAGI, cursor: DictCursor, args: list[str]) -> None:
        self._agi = agi
        self._cursor = cursor
        self._args = args

    def _set_path(self, path_type: str, path_id: str) -> None:
        # schedule path
        path = self._agi.get_variable(dialplan_variables.PATH)
        if path is None or len(path) == 0:
            self._agi.set_variable(dialplan_variables.PATH, path_type)
            self._agi.set_variable(dialplan_variables.PATH_ID, path_id)
