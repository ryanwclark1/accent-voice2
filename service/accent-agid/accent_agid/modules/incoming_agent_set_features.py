# Copyright 2023 Accent Communications

from __future__ import annotations

from psycopg2.extras import DictCursor

from accent_agid import agid
from accent_agid.handlers.agentfeatures import AgentFeatures


def incoming_agent_set_features(
    agi: agid.FastAGI, cursor: DictCursor, args: list[str]
) -> None:
    agentfeatures_handler = AgentFeatures(agi, cursor, args)
    agentfeatures_handler.execute()


agid.register(incoming_agent_set_features)
