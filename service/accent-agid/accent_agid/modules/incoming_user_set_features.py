# Copyright 2023 Accent Communications

from __future__ import annotations

from psycopg2.extras import DictCursor

from accent_agid import agid
from accent_agid.handlers.userfeatures import UserFeatures


def incoming_user_set_features(
    agi: agid.FastAGI, cursor: DictCursor, args: list[str]
) -> None:
    userfeatures_handler = UserFeatures(agi, cursor, args)
    userfeatures_handler.execute()


agid.register(incoming_user_set_features)
