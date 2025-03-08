# Copyright 2023 Accent Communications

from __future__ import annotations

from psycopg2.extras import DictCursor

from accent_agid import agid
from accent_agid.handlers.groupfeatures import GroupFeatures


def incoming_group_set_features(
    agi: agid.FastAGI, cursor: DictCursor, args: list[str]
) -> None:
    groupfeatures_handler = GroupFeatures(agi, cursor, args)
    groupfeatures_handler.execute()


agid.register(incoming_group_set_features)
