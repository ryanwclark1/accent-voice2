# Copyright 2023 Accent Communications

from __future__ import annotations

from psycopg2.extras import DictCursor

from accent_agid import agid
from accent_agid.handlers.outgoingfeatures import OutgoingFeatures


def outgoing_user_set_features(
    agi: agid.FastAGI, cursor: DictCursor, args: list[str]
) -> None:
    outgoing_features_handler = OutgoingFeatures(agi, cursor, args)
    outgoing_features_handler.execute()


agid.register(outgoing_user_set_features)
