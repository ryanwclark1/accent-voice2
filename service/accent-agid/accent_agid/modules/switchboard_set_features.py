# Copyright 2023 Accent Communications

from __future__ import annotations

from psycopg2.extras import DictCursor

from accent_agid import agid
from accent_agid.handlers.switchboardfeatures import SwitchboardFeatures


def switchboard_set_features(
    agi: agid.FastAGI, cursor: DictCursor, args: list[str]
) -> None:
    switchboardfeatures_handler = SwitchboardFeatures(agi, cursor, args)
    switchboardfeatures_handler.execute()


agid.register(switchboard_set_features)
